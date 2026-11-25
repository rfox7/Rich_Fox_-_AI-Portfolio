-- SQLite version of the tables (runs automatically on connect).
-- Keep this in sync with sql/02_create_tables_azure.sql.

CREATE TABLE IF NOT EXISTS staging.sales_clean (
    run_id       TEXT    NOT NULL,
    sale_id      INTEGER NOT NULL,
    sale_date    TEXT    NOT NULL,
    store_id     INTEGER NOT NULL,
    product_id   INTEGER,
    quantity     INTEGER NOT NULL,
    unit_price   REAL    NOT NULL,
    source_file  TEXT    NOT NULL
);

CREATE TABLE IF NOT EXISTS staging.sales_reject (
    run_id       TEXT NOT NULL,
    source_file  TEXT NOT NULL,
    row_num      INTEGER,
    reason       TEXT NOT NULL,
    raw_row      TEXT
);

CREATE TABLE IF NOT EXISTS dw.sales (
    sale_id      INTEGER PRIMARY KEY,
    sale_date    TEXT    NOT NULL,
    store_id     INTEGER NOT NULL,
    product_id   INTEGER,
    quantity     INTEGER NOT NULL,
    unit_price   REAL    NOT NULL,
    source_file  TEXT    NOT NULL,
    loaded_at    TEXT    NOT NULL
);

CREATE TABLE IF NOT EXISTS agent.run_log (
    run_id         TEXT PRIMARY KEY,
    started_at     TEXT NOT NULL,
    finished_at    TEXT,
    request        TEXT NOT NULL,
    status         TEXT NOT NULL,
    files_seen     INTEGER DEFAULT 0,
    rows_loaded    INTEGER DEFAULT 0,
    rows_rejected  INTEGER DEFAULT 0,
    total_reward   REAL    DEFAULT 0,
    user_feedback  INTEGER,
    reflection     TEXT
);

CREATE TABLE IF NOT EXISTS agent.step_log (
    run_id      TEXT    NOT NULL,
    step_no     INTEGER NOT NULL,
    step_name   TEXT    NOT NULL,
    status      TEXT    NOT NULL,
    error_type  TEXT,
    strategy    TEXT,
    explored    INTEGER,
    reward      REAL,
    detail      TEXT,
    logged_at   TEXT    NOT NULL
);

CREATE TABLE IF NOT EXISTS agent.strategy_scores (
    error_type    TEXT    NOT NULL,
    strategy      TEXT    NOT NULL,
    pulls         INTEGER NOT NULL DEFAULT 0,
    total_reward  REAL    NOT NULL DEFAULT 0,
    updated_at    TEXT,
    PRIMARY KEY (error_type, strategy)
);
