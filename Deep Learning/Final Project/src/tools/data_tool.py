"""Data tool (pandas): profiles a file, finds problems, and applies fixes.

When the agent uses it: after a file is read, `profile` lists every problem
by error type. For each problem the agent picks a recovery strategy (that's
the learning part, see src/agent/bandit.py) and calls `apply_strategy`.
`score_fix` turns the before/after result into a reward.

Error types and the strategies the agent can choose from
-------------------------------------------------------
missing_column  map_aliases, skip_file
bad_date        parse_multi_format, reject_rows, skip_file
type_mismatch   coerce_numeric, reject_rows, skip_file
missing_value   reject_rows, fill_default, skip_file
duplicate_key   keep_last, keep_first, reject_all_dupes

Some strategies are traps on purpose (fill_default keeps rows that are
still invalid, keep_first keeps the bad copy of a corrected row). The agent
isn't told which ones are good; it has to learn that from the rewards.
"""
from __future__ import annotations

from datetime import datetime

import pandas as pd

from src.tools.base import ToolSpec


def _rows(n: int) -> str:
    return f"{n} row" if n == 1 else f"{n} rows"

REQUIRED_COLUMNS = ["sale_id", "sale_date", "store_id", "product_id", "quantity", "unit_price"]
KEY_COLUMNS = ["sale_id", "store_id"]
COLUMN_ALIASES = {
    "id": "sale_id", "saleid": "sale_id", "transaction_id": "sale_id",
    "date": "sale_date", "saledate": "sale_date", "txn_date": "sale_date",
    "store": "store_id", "storeid": "store_id", "branch_id": "store_id",
    "product": "product_id", "productid": "product_id", "sku": "product_id",
    "qty": "quantity", "units": "quantity",
    "price": "unit_price", "unitprice": "unit_price", "amount": "unit_price",
}
DATE_FORMATS = ["%Y-%m-%d", "%m/%d/%Y", "%d-%b-%Y", "%Y/%m/%d", "%m-%d-%Y", "%b %d %Y"]

ERROR_ORDER = ["missing_column", "bad_date", "type_mismatch", "missing_value", "duplicate_key"]

STRATEGIES = {
    "missing_column": ["map_aliases", "skip_file"],
    "bad_date": ["parse_multi_format", "reject_rows", "skip_file"],
    "type_mismatch": ["coerce_numeric", "reject_rows", "skip_file"],
    "missing_value": ["reject_rows", "fill_default", "skip_file"],
    "duplicate_key": ["keep_last", "keep_first", "reject_all_dupes"],
}


# ----------------------------------------------------------------- checks
def _is_iso_date(v) -> bool:
    """A real ISO date (YYYY-MM-DD) in a believable range (2000-2100)."""
    if pd.isna(v):
        return False
    try:
        d = datetime.strptime(str(v).strip(), "%Y-%m-%d")
        return 2000 <= d.year <= 2100
    except ValueError:
        return False


def _is_int(v) -> bool:
    try:
        return float(str(v).strip()) == int(float(str(v).strip()))
    except (ValueError, TypeError):
        return False


def _is_number(v) -> bool:
    try:
        float(str(v).strip())
        return str(v).strip().lower() not in ("nan", "inf", "-inf")
    except (ValueError, TypeError):
        return False


def valid_mask(df: pd.DataFrame) -> pd.Series:
    """True for rows that are ready to load. This is the agent's quality check."""
    if any(c not in df.columns for c in REQUIRED_COLUMNS):
        return pd.Series(False, index=df.index)
    sale_id_ok = df["sale_id"].apply(lambda v: _is_int(v) and int(float(v)) > 0)
    store_ok = df["store_id"].apply(lambda v: _is_int(v) and int(float(v)) > 0)
    date_ok = df["sale_date"].apply(_is_iso_date)
    qty_ok = df["quantity"].apply(lambda v: _is_int(v) and int(float(v)) > 0)
    price_ok = df["unit_price"].apply(lambda v: _is_number(v) and float(v) >= 0)
    unique_ok = ~df["sale_id"].duplicated(keep=False)
    return sale_id_ok & store_ok & date_ok & qty_ok & price_ok & unique_ok


def profile(df: pd.DataFrame) -> dict[str, list]:
    """Return {error_type: [row indexes]} for every problem found, in fix order."""
    issues: dict[str, list] = {}
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        issues["missing_column"] = missing  # column names, not row indexes
        return issues  # nothing else can be checked until the columns are fixed

    bad_date = df.index[df["sale_date"].notna() & ~df["sale_date"].apply(_is_iso_date)].tolist()
    num_cols = df[["quantity", "unit_price"]]
    type_bad = df.index[(num_cols.notna() & ~num_cols.map(_is_number)).any(axis=1)].tolist()
    missing_val = df.index[df[KEY_COLUMNS + ["sale_date"]].isna().any(axis=1)].tolist()
    dupes = df.index[df["sale_id"].notna() & df["sale_id"].duplicated(keep=False)].tolist()

    for name, rows in (("bad_date", bad_date), ("type_mismatch", type_bad),
                       ("missing_value", missing_val), ("duplicate_key", dupes)):
        if rows:
            issues[name] = rows
    return issues


# ----------------------------------------------------------------- fixes
def _parse_date(v):
    for fmt in DATE_FORMATS:
        try:
            return datetime.strptime(str(v).strip(), fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    return None


def _coerce_number(v):
    text = str(v).strip().replace("$", "").replace(",", "")
    return text if _is_number(text) else None


def apply_strategy(df: pd.DataFrame, error_type: str, strategy: str, affected: list):
    """Apply one fix. Returns (cleaned_df, rejected_df, note)."""
    if strategy not in STRATEGIES.get(error_type, []):
        raise ValueError(f"'{strategy}' is not a valid strategy for {error_type}")

    df = df.copy()
    empty = df.iloc[0:0].copy()

    if strategy == "skip_file":
        return empty, df.assign(_reason=f"{error_type}: file skipped"), "Skipped the whole file"

    if error_type == "missing_column":
        renamed = {c: COLUMN_ALIASES[c.lower()] for c in df.columns if c.lower() in COLUMN_ALIASES}
        df = df.rename(columns=renamed)
        still_missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
        if still_missing:
            return empty, df.assign(_reason=f"missing columns {still_missing}"), f"Could not map {still_missing}"
        return df, empty, f"Renamed columns {renamed}"

    rows = [r for r in affected if r in df.index]

    if strategy == "reject_rows" or strategy == "reject_all_dupes":
        rejected = df.loc[rows].assign(_reason=error_type)
        return df.drop(index=rows), rejected, f"Rejected {_rows(len(rows))}"

    if strategy == "parse_multi_format":
        df.loc[rows, "sale_date"] = df.loc[rows, "sale_date"].apply(_parse_date)
        failed = [r for r in rows if pd.isna(df.at[r, "sale_date"])]
        rejected = df.loc[failed].assign(_reason="bad_date: unparseable")
        return df.drop(index=failed), rejected, f"Parsed {len(rows) - len(failed)} date(s), rejected {_rows(len(failed))}"

    if strategy == "coerce_numeric":
        for col in ("quantity", "unit_price"):
            df.loc[rows, col] = df.loc[rows, col].apply(lambda v: v if pd.isna(v) else _coerce_number(v))
        failed = [r for r in rows if df.loc[r, ["quantity", "unit_price"]].isna().any()]
        rejected = df.loc[failed].assign(_reason="type_mismatch: not numeric")
        return df.drop(index=failed), rejected, f"Converted {_rows(len(rows) - len(failed))}, rejected {len(failed)}"

    if strategy == "fill_default":
        df.loc[rows, "sale_id"] = df.loc[rows, "sale_id"].fillna("-1")
        df.loc[rows, "store_id"] = df.loc[rows, "store_id"].fillna("0")
        df.loc[rows, "sale_date"] = df.loc[rows, "sale_date"].fillna("1900-01-01")
        return df, empty, f"Filled defaults on {_rows(len(rows))}"

    if strategy in ("keep_last", "keep_first"):
        keep = "last" if strategy == "keep_last" else "first"
        dup_mask = df["sale_id"].duplicated(keep=keep) & df["sale_id"].notna()
        rejected = df[dup_mask].assign(_reason=f"duplicate_key: kept {keep}")
        return df[~dup_mask], rejected, f"Kept the {keep} copy of each duplicate, rejected {_rows(int(dup_mask.sum()))}"

    raise ValueError(f"No implementation for {strategy}")


def _row_ok(df: pd.DataFrame, error_type: str) -> pd.Series:
    """Is each row now free of this particular problem (and not faked)?"""
    if error_type == "bad_date":
        return df["sale_date"].apply(_is_iso_date)
    if error_type == "type_mismatch":
        return df["quantity"].apply(_is_number) & df["unit_price"].apply(_is_number)
    if error_type == "missing_value":
        return (df["sale_id"].apply(lambda v: _is_int(v) and int(float(v)) > 0)
                & df["store_id"].apply(lambda v: _is_int(v) and int(float(v)) > 0)
                & df["sale_date"].apply(_is_iso_date))
    if error_type == "duplicate_key":
        return (~df["sale_id"].duplicated(keep=False)
                & df["quantity"].apply(lambda v: _is_int(v) and int(float(v)) > 0))
    raise ValueError(error_type)


def score_fix(before: pd.DataFrame, after: pd.DataFrame, error_type: str, affected: list) -> float:
    """Reward for one fix, between -1 and +1.

    + affected rows that are still here and really fixed
    - affected rows that are still here but still broken (a fake fix)
    - unaffected rows that got thrown away (collateral damage)
    Rejecting the bad rows scores 0: safe, but nothing was saved.
    """
    if error_type == "missing_column":
        ok = len(after) > 0 and all(c in after.columns for c in REQUIRED_COLUMNS)
        return 1.0 if ok else -1.0

    n = max(len(affected), 1)
    kept = [r for r in affected if r in after.index]
    if kept:
        ok = _row_ok(after.loc[kept], error_type) if error_type != "duplicate_key" else _row_ok(after, error_type).loc[kept]
        fixed, still_bad = int(ok.sum()), int((~ok).sum())
    else:
        fixed = still_bad = 0
    affected_set = set(affected)
    lost_good = sum(1 for r in before.index if r not in affected_set and r not in after.index)
    reward = (fixed - still_bad - lost_good) / n
    return round(max(-1.0, min(1.0, reward)), 3)


SPEC = ToolSpec(
    name="data_tool",
    description="Profiles a DataFrame for data-quality problems and applies a chosen fix.",
    when_to_use="After every file read: profile it, then fix each problem type in order.",
    functions={"profile": profile, "apply_strategy": apply_strategy, "valid_mask": valid_mask},
)
