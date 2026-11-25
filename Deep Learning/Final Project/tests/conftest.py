import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src import config  # noqa: E402
from src.db import Database  # noqa: E402


@pytest.fixture
def sqlite_db(tmp_path, monkeypatch):
    """A throwaway SQLite warehouse plus an incoming folder, so tests never touch Azure."""
    incoming = tmp_path / "incoming"
    incoming.mkdir()
    monkeypatch.setattr(config, "INCOMING_DIR", incoming)
    monkeypatch.setattr(config, "RETRY_BASE_SECONDS", 0.05)
    db = Database(backend="sqlite", sqlite_dir=tmp_path / "sqlite")
    yield db
    db.close()
