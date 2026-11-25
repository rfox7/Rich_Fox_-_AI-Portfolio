-- Run as the server admin after 01_setup_azure.sql.
-- The admin owns the table definitions, so the agent can never change them.
-- Keep this in sync with sql/sqlite_schema.sql.

CREATE TABLE staging.sales_clean (
    run_id       VARCHAR(36)    NOT NULL,
    sale_id      INT            NOT NULL,
    sale_date    DATE           NOT NULL,
    store_id     INT            NOT NULL,
    product_id   INT            NULL,
    quantity     INT            NOT NULL,
    unit_price   DECIMAL(10,2)  NOT NULL,
    source_file  NVARCHAR(260)  NOT NULL
);

CREATE TABLE staging.sales_reject (
    run_id       VARCHAR(36)    NOT NULL,
    source_file  NVARCHAR(260)  NOT NULL,
    row_num      INT            NULL,
    reason       NVARCHAR(200)  NOT NULL,
    raw_row      NVARCHAR(MAX)  NULL
);

CREATE TABLE dw.sales (
    sale_id      INT            NOT NULL PRIMARY KEY,
    sale_date    DATE           NOT NULL,
    store_id     INT            NOT NULL,
    product_id   INT            NULL,
    quantity     INT            NOT NULL,
    unit_price   DECIMAL(10,2)  NOT NULL,
    source_file  NVARCHAR(260)  NOT NULL,
    loaded_at    DATETIME2(0)   NOT NULL
);

CREATE TABLE agent.run_log (
    run_id         VARCHAR(36)    NOT NULL PRIMARY KEY,
    started_at     DATETIME2(0)   NOT NULL,
    finished_at    DATETIME2(0)   NULL,
    request        NVARCHAR(1000) NOT NULL,
    status         VARCHAR(20)    NOT NULL,
    files_seen     INT            NOT NULL DEFAULT 0,
    rows_loaded    INT            NOT NULL DEFAULT 0,
    rows_rejected  INT            NOT NULL DEFAULT 0,
    total_reward   FLOAT          NOT NULL DEFAULT 0,
    user_feedback  INT            NULL,
    reflection     NVARCHAR(MAX)  NULL
);

CREATE TABLE agent.step_log (
    run_id      VARCHAR(36)    NOT NULL,
    step_no     INT            NOT NULL,
    step_name   VARCHAR(50)    NOT NULL,
    status      VARCHAR(20)    NOT NULL,
    error_type  VARCHAR(50)    NULL,
    strategy    VARCHAR(50)    NULL,
    explored    BIT            NULL,
    reward      FLOAT          NULL,
    detail      NVARCHAR(1000) NULL,
    logged_at   DATETIME2(0)   NOT NULL
);

CREATE TABLE agent.strategy_scores (
    error_type    VARCHAR(50)  NOT NULL,
    strategy      VARCHAR(50)  NOT NULL,
    pulls         INT          NOT NULL DEFAULT 0,
    total_reward  FLOAT        NOT NULL DEFAULT 0,
    updated_at    DATETIME2(0) NULL,
    CONSTRAINT PK_strategy_scores PRIMARY KEY (error_type, strategy)
);
GO

-- Guardrail check (run while logged in as agent_user). Both should FAIL with
-- a permission error -- screenshot them for the report's safety section:
   CREATE TABLE dw.test (id INT);
   DELETE FROM dw.sales;
