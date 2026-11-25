"""Reasoning: understand the request, make a plan, and reflect afterward.

Pattern: plan-then-execute (this file makes the plan, core.py runs it), with
ReAct-style recovery inside each step and a reflection note at the end.

Each function tries the LLM first and falls back to simple rules, so the
agent behaves the same way with or without an API key, just less flexibly.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass

from src.agent import llm
from src.tools.data_tool import STRATEGIES

# Steps the agent knows how to run. The LLM can only choose from these.
STEP_LIBRARY = ["discover_files", "read_file", "profile", "fix_issues", "validate", "stage", "merge", "report"]
DEFAULT_PLAN = STEP_LIBRARY[:]


@dataclass
class Task:
    intent: str            # "load" | "status"
    file_pattern: str      # e.g. "sales_*.csv"
    dry_run: bool          # True = check and report, but don't write to dw
    notes: str = ""


PARSE_PROMPT = (
    "You read requests sent to a data-pipeline agent and reply with JSON only, with these keys:\n"
    "- intent: 'load' if the request is about the incoming data files in any way (loading, checking, "
    "previewing, reviewing or looking at them); 'status' ONLY if it asks about past runs or history.\n"
    "- file_pattern: a glob for the files, e.g. 'sales_*.csv' (default '*.csv').\n"
    "- dry_run: true unless the user clearly asks to load/write the data into the warehouse; "
    "true for anything like check, preview, look at, review, or 'don't load yet'.\n"
    "Examples:\n"
    "'Load the sales files' -> {\"intent\":\"load\",\"file_pattern\":\"sales_*.csv\",\"dry_run\":false}\n"
    "'Can you peek at what came in today?' -> {\"intent\":\"load\",\"file_pattern\":\"*.csv\",\"dry_run\":true}\n"
    "'How did the last few runs go?' -> {\"intent\":\"status\",\"file_pattern\":\"*.csv\",\"dry_run\":false}"
)


def parse_request(text: str) -> Task:
    raw = llm.chat(PARSE_PROMPT, text, max_tokens=150, json_mode=True)
    if raw:
        try:
            d = json.loads(raw)
            intent = d.get("intent") if d.get("intent") in ("load", "status") else "load"
            pattern = str(d.get("file_pattern") or "*.csv")
            if not re.fullmatch(r"[\w\-\*\?\.]+", pattern):
                pattern = "*.csv"
            # Safety: if the LLM OR the fail-safe rule says "dry run", don't write.
            dry = bool(d.get("dry_run")) or (intent == "load" and wants_dry_run(text))
            return Task(intent, pattern, dry, f"parsed by {llm.name()}")
        except (ValueError, TypeError, AttributeError):
            task = _parse_rules(text)
            task.notes += " (LLM reply wasn't valid JSON)"
            return task
    task = _parse_rules(text)
    if llm.available():  # say why the LLM wasn't used (transparency)
        task.notes += f" (LLM call failed: {llm.last_error or 'empty reply'})"
    return task


WRITE_WORDS = r"\b(load|import|ingest|insert|write|put|push|merge)\b"
NEGATION = r"\b(don't|dont|do not|not yet|hold off|without|no need to|never|avoid)\b"
LOOK_WORDS = r"\b(dry run|preview|just check|only check|look at|take a look|have a look|review|inspect)\b"


def wants_dry_run(text: str) -> bool:
    """Fail safe: write to the warehouse only when the request clearly asks for it.

    Dry run if the request says not to (don't / hold off / not yet ...), only asks
    to look or preview, or never asks to load at all.
    """
    t = text.lower().replace("\u2019", "'")
    return bool(re.search(NEGATION, t) or re.search(LOOK_WORDS, t) or not re.search(WRITE_WORDS, t))


def _parse_rules(text: str) -> Task:
    t = text.lower()
    if re.search(r"\b(status|last run|history|what happened|previous)\b", t) and not re.search(r"\b(load|import)\b", t):
        return Task("status", "*.csv", False, "parsed by rules")
    m = re.search(r"([\w\-\*\?]+\.csv)", t)
    pattern = m.group(1) if m else ("sales_*.csv" if "sales" in t else "*.csv")
    return Task("load", pattern, wants_dry_run(text), "parsed by rules")


def make_plan(task: Task) -> list[str]:
    if task.intent == "status":
        return ["report"]
    plan = DEFAULT_PLAN[:]
    if task.dry_run:
        plan = [s for s in plan if s not in ("stage", "merge")]
    return plan


REFLECT_PROMPT = (
    "You write a 2-3 sentence lesson-learned note about one run of a data pipeline agent, in plain words.\n"
    "Facts to use correctly:\n"
    "- dry_run=true means the user asked only to check the files; loading 0 rows is EXPECTED, not a failure.\n"
    "- Each fix gets a reward from -1 to +1: positive = rows really repaired; 0 = bad rows safely rejected "
    "(correct when a value can't be honestly fixed, e.g. a missing ID); negative = a fake fix or good rows lost.\n"
    "- Rejected rows are bad data kept in a reject table with their reason; rejecting them is not a failure.\n"
    "- Only mention fixes from this list: " + ", ".join(sorted({s for v in STRATEGIES.values() for s in v})) + ". "
    "Never suggest inventing or imputing missing IDs.\n"
    "Say what worked, what (if anything) went wrong, and one concrete thing to watch next time."
)


def reflect(run, past_notes: list[str]) -> str:
    """Write a short lesson-learned note about the run."""
    summary = {
        "status": run.status,
        "dry_run": run.status == "checked",
        "files": run.files_seen,
        "rows_loaded": run.rows_loaded,
        "rows_ready_to_load": getattr(run, "rows_ready", 0),
        "rows_rejected": run.rows_rejected,
        "total_reward": run.total_reward,
        "fixes": [f"{s.error_type}->{s.strategy} ({s.reward:+.2f})" for s in run.steps if s.strategy],
        "failures": [f"{s.step_name}: {s.detail}" for s in run.steps if s.status in ("error", "blocked")],
    }
    note = llm.chat(REFLECT_PROMPT, json.dumps({"run": summary, "past_notes": past_notes[:3]}), max_tokens=400)
    if note:
        return note.strip() + f" [written by {llm.name()}]"
    failed = f" [LLM reflection failed: {llm.last_error or 'empty reply'}; rule-based note]" if llm.available() else ""

    fixes = [(f"{s.error_type}->{s.strategy}", s.reward) for s in run.steps if s.strategy]
    good = sorted({name for name, r in fixes if r > 0})
    bad = sorted({name for name, r in fixes if r < 0})
    if run.status == "checked":
        parts = [f"Dry run: {getattr(run, 'rows_ready', 0)} rows ready to load, {run.rows_rejected} rejected."]
    else:
        parts = [f"Run {run.status}: {run.rows_loaded} rows loaded, {run.rows_rejected} rejected."]
    if good:
        parts.append("Worked well: " + ", ".join(good) + ".")
    if bad:
        parts.append("Avoid next time: " + ", ".join(bad) + ".")
    if summary["failures"]:
        parts.append("Failures: " + "; ".join(summary["failures"]) + ".")
    return " ".join(parts) + failed
