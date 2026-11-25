"""Keeps file access inside the incoming data folder."""
from __future__ import annotations

from pathlib import Path

from src import config
from src.safety.sql_guard import SafetyViolation

ALLOWED_EXTENSIONS = {".csv"}


def safe_path(path: str | Path, base: Path | None = None) -> Path:
    """Return the resolved path, or raise SafetyViolation if it leaves the base folder."""
    base = Path(base or config.INCOMING_DIR).resolve()
    candidate = Path(path)
    resolved = (candidate if candidate.is_absolute() else base / candidate).resolve()

    if resolved != base and base not in resolved.parents:
        raise SafetyViolation(f"Path '{path}' is outside the allowed data folder")
    if resolved.is_file() or resolved.suffix:
        if resolved.suffix.lower() not in ALLOWED_EXTENSIONS:
            raise SafetyViolation(f"File type '{resolved.suffix}' is not allowed (CSV only)")
        if resolved.exists() and resolved.stat().st_size > config.MAX_FILE_MB * 1024 * 1024:
            raise SafetyViolation(f"File is larger than {config.MAX_FILE_MB} MB")
    return resolved
