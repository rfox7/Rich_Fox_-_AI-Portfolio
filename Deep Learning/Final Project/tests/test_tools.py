import pandas as pd

from src.tools import data_tool, safe_tool_call
from src.db import DatabaseUnavailable


def _df(rows):
    return pd.DataFrame(rows, columns=data_tool.REQUIRED_COLUMNS, dtype=str)


def test_safe_tool_call_never_raises():
    def boom():
        raise DatabaseUnavailable("paused")
    result = safe_tool_call(boom, fallback="cached")
    assert result.status == "error" and result.error_type == "db_unavailable" and result.fallback == "cached"


def test_profile_finds_each_problem():
    df = _df([
        ["1", "2026-11-01", "5", "1001", "2", "9.99"],
        ["2", "11/02/2026", "5", "1001", "2", "9.99"],   # bad_date
        ["3", "2026-11-03", "5", "1001", "two", "9.99"],  # type_mismatch
        [None, "2026-11-04", "5", "1001", "2", "9.99"],  # missing_value
        ["5", "2026-11-05", "5", "1001", "0", "9.99"],   # duplicate (voided)
        ["5", "2026-11-05", "5", "1001", "3", "9.99"],   # duplicate (correction)
    ])
    issues = data_tool.profile(df)
    assert issues["bad_date"] == [1]
    assert issues["type_mismatch"] == [2]
    assert issues["missing_value"] == [3]
    assert issues["duplicate_key"] == [4, 5]


def test_rewards_favor_real_fixes():
    df = _df([["1", "11/02/2026", "5", "1001", "2", "9.99"], ["2", "2026-11-03", "5", "1001", "2", "9.99"]])
    scores = {}
    for strategy in data_tool.STRATEGIES["bad_date"]:
        new, _, _ = data_tool.apply_strategy(df, "bad_date", strategy, [0])
        scores[strategy] = data_tool.score_fix(df, new, "bad_date", [0])
    assert scores["parse_multi_format"] > scores["reject_rows"] > scores["skip_file"]


def test_duplicate_trap():
    df = _df([["5", "2026-11-05", "5", "1001", "0", "9.99"], ["5", "2026-11-05", "5", "1001", "3", "9.99"]])
    last, _, _ = data_tool.apply_strategy(df, "duplicate_key", "keep_last", [0, 1])
    first, _, _ = data_tool.apply_strategy(df, "duplicate_key", "keep_first", [0, 1])
    assert data_tool.score_fix(df, last, "duplicate_key", [0, 1]) > data_tool.score_fix(df, first, "duplicate_key", [0, 1])


def test_fill_default_is_a_fake_fix():
    df = _df([[None, "2026-11-05", "5", "1001", "1", "9.99"]])
    filled, _, _ = data_tool.apply_strategy(df, "missing_value", "fill_default", [0])
    assert data_tool.score_fix(df, filled, "missing_value", [0]) < 0
