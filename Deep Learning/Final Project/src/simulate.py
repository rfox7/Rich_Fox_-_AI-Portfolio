"""Training environment: makes sales CSV files with planted data problems.

The agent never sees which problems were planted. It has to find them with
the data tool and learn which fixes work from the rewards. Run directly to
create a few sample files:

    py -m src.simulate --files 3
"""
from __future__ import annotations

import argparse
import csv
import random
from datetime import date, timedelta
from pathlib import Path

from src import config

HEADER = ["sale_id", "sale_date", "store_id", "product_id", "quantity", "unit_price"]
ALIASED_HEADER = ["id", "date", "store", "sku", "qty", "price"]  # triggers missing_column

DEFAULT_RATES = {
    "bad_date": 0.06,       # dates in the wrong format (most are fixable)
    "type_mismatch": 0.05,  # "$12.50", "1,200", the odd "twelve"
    "missing_value": 0.03,  # blank sale_id or store_id
    "duplicate_key": 0.04,  # a voided row (quantity 0) followed by its correction
}


def _bad_date(d: date, rng: random.Random) -> str:
    return rng.choice([
        d.strftime("%m/%d/%Y"), d.strftime("%d-%b-%Y"), d.strftime("%Y/%m/%d"),
        d.strftime("%m/%d/%Y"), "TBD",  # "TBD" can't be fixed and should be rejected
    ])


def make_rows(n: int, start_id: int, rng: random.Random, rates: dict | None = None) -> list[list[str]]:
    rates = {**DEFAULT_RATES, **(rates or {})}
    rows: list[list[str]] = []
    base = date(2026, 11, 1)
    sale_id = start_id
    while len(rows) < n:
        d = base + timedelta(days=rng.randint(0, 20))
        row = [str(sale_id), d.isoformat(), str(rng.randint(1, 87)), str(rng.randint(1000, 1999)),
               str(rng.randint(1, 12)), f"{rng.uniform(1, 250):.2f}"]

        if rng.random() < rates["bad_date"]:
            row[1] = _bad_date(d, rng)
        if rng.random() < rates["type_mismatch"]:
            col = rng.choice([4, 5])
            row[col] = rng.choice([f"${row[5]}", f"{int(row[4]):,}", "twelve"]) if col == 5 else rng.choice(
                [f"{int(row[4]) * 100:,}", "twelve", f" {row[4]} "])
        if rng.random() < rates["missing_value"]:
            row[rng.choice([0, 2])] = ""

        if rng.random() < rates["duplicate_key"] and row[0]:
            voided = row.copy()
            voided[4] = "0"
            rows.append(voided)
        rows.append(row)
        sale_id += 1
    return rows[:n]


def write_file(path: Path, rows: list[list[str]], aliased: bool = False) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(ALIASED_HEADER if aliased else HEADER)
        w.writerows(rows)
    return path


def generate(folder: Path | None = None, files: int = 3, rows: int = 200, seed: int | None = None,
             start_id: int = 100000, alias_rate: float = 0.25, clear: bool = True) -> list[Path]:
    folder = Path(folder or config.INCOMING_DIR)
    if clear and folder.exists():
        for old in folder.glob("sales_*.csv"):
            old.unlink()
    rng = random.Random(seed)
    out = []
    for i in range(files):
        data = make_rows(rows, start_id + i * rows * 2, rng)
        out.append(write_file(folder / f"sales_{i + 1:03d}.csv", data, aliased=rng.random() < alias_rate))
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Create sample sales CSVs with planted errors")
    ap.add_argument("--files", type=int, default=3)
    ap.add_argument("--rows", type=int, default=200)
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()
    for p in generate(files=args.files, rows=args.rows, seed=args.seed):
        print("wrote", p)
