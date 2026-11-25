"""Shared tool plumbing: the safe wrapper every tool call goes through.

`safe_tool_call` never lets an exception escape. It always returns a
ToolResult, and it sorts failures into an `error_type` the agent can learn
from (for example `db_unavailable`), instead of crashing the run.
"""
from __future__ import annotations

import logging
import time
from dataclasses import dataclass, field
from typing import Any, Callable

from src.db import DatabaseUnavailable
from src.safety.sql_guard import SafetyViolation

log = logging.getLogger(__name__)


@dataclass
class ToolResult:
    status: str  # "success" | "error" | "blocked"
    data: Any = None
    error: str | None = None
    error_type: str | None = None
    fallback: Any = None
    seconds: float = 0.0

    @property
    def ok(self) -> bool:
        return self.status == "success"


@dataclass
class ToolSpec:
    """Describes a tool so the planner (and the report) know when to use it."""
    name: str
    description: str
    when_to_use: str
    functions: dict[str, Callable] = field(default_factory=dict)


def classify_error(exc: Exception) -> str:
    if isinstance(exc, SafetyViolation):
        return "blocked"
    if isinstance(exc, DatabaseUnavailable):
        return "db_unavailable"
    name = type(exc).__name__.lower()
    text = str(exc).lower()
    if "operationalerror" in name or "timeout" in text or "login timeout" in text:
        return "db_unavailable"
    if isinstance(exc, FileNotFoundError):
        return "file_missing"
    if isinstance(exc, (ValueError, TypeError, KeyError)):
        return "bad_input"
    return "tool_error"


def safe_tool_call(
    fn: Callable,
    *args,
    validate: Callable[[Any], bool] | None = None,
    fallback: Any = None,
    **kwargs,
) -> ToolResult:
    start = time.perf_counter()
    try:
        result = fn(*args, **kwargs)
        if validate is not None and not validate(result):
            return ToolResult("error", error="Tool returned an invalid result", error_type="invalid_result",
                              fallback=fallback, seconds=time.perf_counter() - start)
        return ToolResult("success", data=result, seconds=time.perf_counter() - start)
    except Exception as exc:  # noqa: BLE001 - the whole point is to catch everything
        etype = classify_error(exc)
        log.warning("Tool %s failed (%s): %s", getattr(fn, "__name__", fn), etype, exc)
        return ToolResult("blocked" if etype == "blocked" else "error", error=str(exc), error_type=etype,
                          fallback=fallback, seconds=time.perf_counter() - start)
