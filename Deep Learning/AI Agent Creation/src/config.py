"""Central settings, read from the .env file in the project root.

Nothing secret is hard-coded here. If a value is missing from .env, a safe
default is used (SQLite backend, no LLM), so the project still runs for anyone
who clones the repo without credentials.
"""
import os
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(PROJECT_ROOT / ".env")

# --- Database -----------------------------------------------------------------
# "azure"  -> Azure SQL Database (needs the AZURE_SQL_* values and ODBC Driver 18)
# "sqlite" -> local files under data/sqlite (no setup needed)
DB_BACKEND = os.getenv("DB_BACKEND", "sqlite").strip().lower()

AZURE_SQL = {
    "server": os.getenv("AZURE_SQL_SERVER", ""),
    "database": os.getenv("AZURE_SQL_DATABASE", ""),
    "user": os.getenv("AZURE_SQL_USER", ""),
    "password": os.getenv("AZURE_SQL_PASSWORD", ""),
    "driver": os.getenv("AZURE_SQL_DRIVER", "ODBC Driver 18 for SQL Server"),
}

SQLITE_DIR = Path(os.getenv("SQLITE_DIR", PROJECT_ROOT / "data" / "sqlite"))

# --- Files --------------------------------------------------------------------
# The agent may only read files inside this folder (see src/safety/path_guard.py).
INCOMING_DIR = Path(os.getenv("INCOMING_DIR", PROJECT_ROOT / "data" / "incoming"))
MAX_FILE_MB = float(os.getenv("MAX_FILE_MB", "25"))

# --- LLM (optional) -----------------------------------------------------------
# Without a key the agent uses its rule-based parser, planner and reflection.
# Provider: "anthropic" (Claude), "openai" or "azure"; blank = first key found.
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "").strip().lower()
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL", "claude-haiku-5-5")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT", "")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY", "")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "2024-10-21")
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")

# --- Learning -----------------------------------------------------------------
BANDIT_EPSILON = float(os.getenv("BANDIT_EPSILON", "0.2"))  # chance of exploring
FEEDBACK_WEIGHT = float(os.getenv("FEEDBACK_WEIGHT", "0.25"))  # thumbs up/down size
# First wait when retrying a paused/unreachable database (doubles each retry).
# 5 seconds suits Azure SQL serverless wake-ups; the demo scripts lower it.
RETRY_BASE_SECONDS = float(os.getenv("RETRY_BASE_SECONDS", "5"))
