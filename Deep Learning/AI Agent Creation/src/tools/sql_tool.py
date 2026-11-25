"""SQL tool: the only way the agent talks to the warehouse.

When the agent uses it: to load cleaned rows into staging, write rejects,
merge staging into dw.sales, and read/write its own memory tables.

Every statement passes through the SQL guard (src/safety/sql_guard.py)
before it reaches the database. The few dialect differences between Azure
SQL and SQLite live here, so the agent code doesn't have to care.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone

import pandas as pd

from src.db import Database
from src.safety.sql_guard import enforce
from src.tools.base import ToolSpec


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")


class SqlTool:
    def __init__(self, db: Database):
        self.db = db

    # ---------------------------------------------------------- guarded basics
    def run(self, sql: str, params=()) -> int:
        enforce(sql)
        return self.db.execute(sql, params)

    def run_many(self, sql: str, rows: list[tuple]) -> int:
        enforce(sql)
        return self.db.executemany(sql, rows)

    def select(self, sql: str, params=()) -> list[dict]:
        enforce(sql)
        return self.db.query(sql, params)

    def ping(self) -> bool:
        self.db.close()
        self.db.connect()
        return bool(self.select("SELECT 1 AS ok"))

    # ---------------------------------------------------------- pipeline steps
    def stage_clean(self, run_id: str, df: pd.DataFrame, source_file: str) -> int:
        self.run("DELETE FROM staging.sales_clean WHERE run_id = ? AND source_file = ?", (run_id, source_file))
        rows = [
            (run_id, int(float(r.sale_id)), str(r.sale_date), int(float(r.store_id)),
             None if pd.isna(r.product_id) else int(float(r.product_id)),
             int(float(r.quantity)), round(float(r.unit_price), 2), source_file)
            for r in df.itertuples(index=False)
        ]
        return self.run_many(
            "INSERT INTO staging.sales_clean (run_id, sale_id, sale_date, store_id, product_id, "
            "quantity, unit_price, source_file) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            rows,
        )

    def stage_rejects(self, run_id: str, df: pd.DataFrame, source_file: str) -> int:
        if df is None or df.empty:
            return 0
        rows = []
        for idx, r in df.iterrows():
            raw = {k: (None if pd.isna(v) else str(v)) for k, v in r.items() if k != "_reason"}
            rows.append((run_id, source_file, int(idx) + 2, str(r.get("_reason", "rejected"))[:200], json.dumps(raw)))
        return self.run_many(
            "INSERT INTO staging.sales_reject (run_id, source_file, row_num, reason, raw_row) VALUES (?, ?, ?, ?, ?)",
            rows,
        )

    def merge_to_dw(self, run_id: str) -> int:
        now = utc_now()
        if self.db.backend == "azure":
            sql = (
                "MERGE INTO dw.sales AS t "
                "USING (SELECT sale_id, sale_date, store_id, product_id, quantity, unit_price, source_file "
                "       FROM staging.sales_clean WHERE run_id = ?) AS s "
                "ON t.sale_id = s.sale_id "
                "WHEN MATCHED THEN UPDATE SET t.sale_date = s.sale_date, t.store_id = s.store_id, "
                "  t.product_id = s.product_id, t.quantity = s.quantity, t.unit_price = s.unit_price, "
                "  t.source_file = s.source_file, t.loaded_at = ? "
                "WHEN NOT MATCHED THEN INSERT (sale_id, sale_date, store_id, product_id, quantity, unit_price, "
                "  source_file, loaded_at) VALUES (s.sale_id, s.sale_date, s.store_id, s.product_id, s.quantity, "
                "  s.unit_price, s.source_file, ?);"
            )
            return self.run(sql, (run_id, now, now))
        sql = (
            "INSERT INTO dw.sales (sale_id, sale_date, store_id, product_id, quantity, unit_price, source_file, loaded_at) "
            "SELECT sale_id, sale_date, store_id, product_id, quantity, unit_price, source_file, ? "
            "FROM staging.sales_clean WHERE run_id = ? AND true "
            "ON CONFLICT(sale_id) DO UPDATE SET sale_date = excluded.sale_date, store_id = excluded.store_id, "
            "product_id = excluded.product_id, quantity = excluded.quantity, unit_price = excluded.unit_price, "
            "source_file = excluded.source_file, loaded_at = excluded.loaded_at"
        )
        return self.run(sql, (now, run_id))

    def dw_row_count(self) -> int:
        return int(self.select("SELECT COUNT(*) AS n FROM dw.sales")[0]["n"])


SPEC = ToolSpec(
    name="sql_tool",
    description="Runs allow-listed SQL against the warehouse (Azure SQL or SQLite).",
    when_to_use="After data is cleaned: stage rows, store rejects, merge into dw, and read/write agent memory.",
)
