"""File tool: finds and reads CSV files, but only inside the incoming folder.

When the agent uses it: at the start of a load, to discover which files match
the request, and then to read each file into a DataFrame (all values as text,
so the data tool can decide how to clean them).
"""
from __future__ import annotations

import fnmatch
from pathlib import Path

import pandas as pd

from src import config
from src.safety.path_guard import safe_path
from src.tools.base import ToolSpec


def list_files(pattern: str = "*.csv", base: Path | None = None) -> list[str]:
    folder = safe_path(".", base) if base else safe_path(config.INCOMING_DIR, config.INCOMING_DIR)
    if not folder.exists():
        raise FileNotFoundError(f"Incoming folder not found: {folder}")
    return sorted(p.name for p in folder.iterdir() if p.is_file() and fnmatch.fnmatch(p.name.lower(), pattern.lower()))


def read_csv(name: str, base: Path | None = None) -> pd.DataFrame:
    path = safe_path(name, base or config.INCOMING_DIR)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {name}")
    df = pd.read_csv(path, dtype=str, keep_default_na=True, skipinitialspace=True)
    df.columns = [c.strip() for c in df.columns]
    return df


SPEC = ToolSpec(
    name="file_tool",
    description="Lists and reads CSV files from the incoming data folder only.",
    when_to_use="First step of every load request: discover matching files, then read each one.",
    functions={"list_files": list_files, "read_csv": read_csv},
)
