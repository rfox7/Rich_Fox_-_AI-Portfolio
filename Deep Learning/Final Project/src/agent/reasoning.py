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

# Steps the agent knows how to run. The LLM can only choose from these.
STEP_LIBRARY = ["discover_files", "read_file", "profile", "fix_issues", "validate", "stage", "merge", "report"]
DEFAULT_PLAN = STEP_LIBRARY[:]


@dataclass
class Task:
    intent: str            # "load" | "status"
    file_pattern: str      # e.g. "sales_*.csv"
    dry_run: bool          # True = check and report, but don't write to dw
    notes: str = ""


def parse_request(text: str) -> Task:
    raw = llm.chat(
        "You turn data-pipeline requests into JSON with keys: intent ('load' or 'status'), "
        "file_pattern (a glob like 'sales_*.csv', default '*.csv'), dry_run (true if the user only "
        "wants a check or preview). Reply with JSON only.",
        text, max_tokens=120, json_mode=True,
    )
    if raw:
        try:
            d = json.loads(raw)
            intent = d.get("intent") if d.get("intent") in ("load", "status") else "load"
            pattern = str(d.get("file_pattern") or "*.csv")
            if not re.fullmatch(r"[\w\-\*\?\.]+", pattern):
                pattern = "*.csv"
            return Task(intent, pattern, bool(d.get("dry_run")), "parsed by LLM")
        except (ValueError, TypeError):
            pass
    return _parse_rules(text)


def _parse_rules(text: str) -> Task:
    t = text.lower()
    if re.search(r"\b(status|last run|history|what happened|previous)\b", t) and not re.search(r"\b(load|import)\b", t):
        return Task("status", "*.csv", False, "parsed by rules")
    m = re.search(r"([\w\-\*\?]+\.csv)", t)
    pattern = m.group(1) if m else ("sales_*.csv" if "sales" in t else "*.csv")
    dry = bool(re.search(r"\b(dry run|preview|just check|only check|don't load|do not load)\b", t))
    return Task("load", pattern, dry, "parsed by rules")


def make_plan(task: Task) -> list[str]:
    if task.intent == "status":
        return ["report"]
    plan = DEFAULT_PLAN[:]
    if task.dry_run:
        plan = [s for s in plan if s not in ("stage", "merge")]
    return plan


def reflect(run, past_notes: list[str]) -> str:
    """Write a short lesson-learned note about the run."""
    summary = {
        "status": run.status,
        "rows_loaded": run.rows_loaded,
        "rows_rejected": run.rows_rejected,
        "total_reward": run.total_reward,
        "fixes": [f"{s.error_type}->{s.strategy} ({s.reward:+.2f})" for s in run.steps if s.strategy],
        "failures": [f"{s.step_name}: {s.detail}" for s in run.steps if s.status in ("error", "blocked")],
    }
    note = llm.chat(
        "You review a data pipeline run. In 2-3 plain sentences, say what went wrong, what worked, "
        "and what to try next time. Use the past notes for context.",
        json.dumps({"run": summary, "past_notes": past_notes[:3]}), max_tokens=150,
    )
    if note:
        return note.strip()

    fixes = [(f"{s.error_type}->{s.strategy}", s.reward) for s in run.steps if s.strategy]
    good = sorted({name for name, r in fixes if r > 0})
    bad = sorted({name for name, r in fixes if r < 0})
    parts = [f"Run {run.status}: {run.rows_loaded} rows loaded, {run.rows_rejected} rejected."]
    if good:
        parts.append("Worked well: " + ", ".join(good) + ".")
    if bad:
        parts.append("Avoid next time: " + ", ".join(bad) + ".")
    if summary["failures"]:
        parts.append("Failures: " + "; ".join(summary["failures"]) + ".")
    return " ".join(parts)
