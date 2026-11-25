"""Database layer with two backends: Azure SQL and SQLite.

Both backends expose the same three schemas, so the rest of the code can use
names like `staging.sales_clean` and `dw.sales` everywhere:

* Azure SQL: real schemas (created by sql/01_setup_azure.sql).
* SQLite:    three database files ATTACHed as `staging`, `dw` and `agent`.

Both drivers use `?` for query parameters, so most SQL is shared. The few
places where the dialects differ (MERGE vs. INSERT ... ON CONFLICT) are handled
in src/tools/sql_tool.py.
"""
from __future__ import annotations

import logging
import sqlite3
import time
from pathlib import Path
from typing import Any, Iterable

from src import config

log = logging.getLogger(__name__)

SQLITE_SCHEMA_FILE = config.PROJECT_ROOT / "sql" / "sqlite_schema.sql"


class DatabaseUnavailable(Exception):
    """Raised when the database can't be reached (paused, network, firewall)."""


class Database:
    def __init__(self, backend: str | None = None, sqlite_dir: Path | None = None):
        self.backend = (backend or config.DB_BACKEND).lower()
        if self.backend not in ("azure", "sqlite"):
            raise ValueError(f"Unknown DB_BACKEND '{self.backend}' (use azure or sqlite)")
        self.sqlite_dir = Path(sqlite_dir or config.SQLITE_DIR)
        self._conn = None
        # Used by the demo/training scripts to simulate an outage, so the agent's
        # recovery strategies can be tested without breaking the real database.
        self.simulated_outage_until: float = 0.0

    # ------------------------------------------------------------------ connect
    def connect(self, timeout: int = 60):
        """Open one connection attempt. Retrying is the agent's decision, not ours."""
        if self._conn is not None:
            return self._conn
        if time.time() < self.simulated_outage_until:
            raise DatabaseUnavailable("Simulated outage: database is paused or unreachable")
        try:
            self._conn = self._connect_azure(timeout) if self.backend == "azure" else self._connect_sqlite()
        except DatabaseUnavailable:
            raise
        except Exception as exc:  # driver-specific errors -> one clear type
            raise DatabaseUnavailable(str(exc)) from exc
        return self._conn

    def _connect_azure(self, timeout: int):
        import pyodbc  # imported here so SQLite users don't need the ODBC driver

        c = config.AZURE_SQL
        missing = [k for k in ("server", "database", "user", "password") if not c[k]]
        if missing:
            raise DatabaseUnavailable(f"Missing Azure settings in .env: {', '.join(missing)}")
        conn_str = (
            f"Driver={{{c['driver']}}};Server=tcp:{c['server']},1433;Database={c['database']};"
            f"Uid={c['user']};Pwd={c['password']};Encrypt=yes;TrustServerCertificate=no;"
            f"Connection Timeout={timeout};"
        )
        return pyodbc.connect(conn_str, autocommit=False)

    def _connect_sqlite(self):
        self.sqlite_dir.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(self.sqlite_dir / "main.db")
        conn.row_factory = sqlite3.Row
        for schema in ("staging", "dw", "agent"):
            conn.execute(f"ATTACH DATABASE ? AS {schema}", (str(self.sqlite_dir / f"{schema}.db"),))
        conn.executescript(SQLITE_SCHEMA_FILE.read_text(encoding="utf-8"))
        conn.commit()
        return conn

    def close(self):
        if self._conn is not None:
            try:
                self._conn.close()
            finally:
                self._conn = None

    # ------------------------------------------------------------------ queries
    def execute(self, sql: str, params: Iterable[Any] = ()) -> int:
        conn = self.connect()
        cur = conn.cursor()
        cur.execute(sql, tuple(params))
        count = cur.rowcount
        conn.commit()
        return count

    def executemany(self, sql: str, rows: list[tuple]) -> int:
        if not rows:
            return 0
        conn = self.connect()
        cur = conn.cursor()
        if self.backend == "azure":
            cur.fast_executemany = True
        cur.executemany(sql, rows)
        conn.commit()
        return len(rows)

    def query(self, sql: str, params: Iterable[Any] = ()) -> list[dict]:
        conn = self.connect()
        cur = conn.cursor()
        cur.execute(sql, tuple(params))
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, row)) for row in cur.fetchall()]

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()
