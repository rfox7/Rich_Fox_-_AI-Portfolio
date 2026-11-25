-- Run ONCE as the server admin, connected to the pipelinepilot database (not master).
-- Creates the three schemas and a limited-permission login for the agent.
-- (Already done during setup; kept here so the repo documents the environment.)

CREATE SCHEMA staging;   -- scratch area the agent fully controls
GO
CREATE SCHEMA dw;        -- final tables: agent can read/insert/update, never delete or alter
GO
CREATE SCHEMA agent;     -- agent memory: run history, step log, strategy scores
GO

-- Contained database user (exists only inside this database)
CREATE USER agent_user WITH PASSWORD = '<<set a long strong password>>';
GO

GRANT CREATE TABLE TO agent_user;
GRANT ALTER, SELECT, INSERT, UPDATE, DELETE ON SCHEMA::staging TO agent_user;
GRANT SELECT, INSERT, UPDATE ON SCHEMA::dw TO agent_user;
GRANT SELECT, INSERT, UPDATE ON SCHEMA::agent TO agent_user;
GO
