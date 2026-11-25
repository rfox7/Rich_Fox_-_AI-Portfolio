"""Memory system.

Short-term (RunMemory): everything about the run in progress: the plan,
each step, errors hit, strategies used and rewards. Lives in Python.

Long-term (LongTermMemory): run history, step logs and reflection notes,
saved in the agent schema so later runs (and the status command) can use
them. Strategy scores are long-term memory too; see bandit.py.
"""
from __future__ import annotations

import uuid
from dataclasses import dataclass, field

from src.tools.sql_tool import SqlTool, utc_now


@dataclass
class Step:
    step_no: int
    step_name: str
    status: str
    error_type: str | None = None
    strategy: str | None = None
    explored: bool | None = None
    reward: float | None = None
    detail: str = ""


@dataclass
class RunMemory:
    request: str
    run_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    started_at: str = field(default_factory=utc_now)
    plan: list[str] = field(default_factory=list)
    steps: list[Step] = field(default_factory=list)
    files_seen: int = 0
    rows_loaded: int = 0
    rows_rejected: int = 0
    status: str = "running"
    reflection: str = ""

    def log(self, step_name: str, status: str, **kwargs) -> Step:
        step = Step(len(self.steps) + 1, step_name, status, **kwargs)
        self.steps.append(step)
        return step

    @property
    def total_reward(self) -> float:
        return round(sum(s.reward for s in self.steps if s.reward is not None), 3)

    def strategies_used(self) -> list[tuple[str, str]]:
        return [(s.error_type, s.strategy) for s in self.steps if s.strategy]


class LongTermMemory:
    def __init__(self, sql: SqlTool):
        self.sql = sql

    def save_run(self, run: RunMemory) -> None:
        self.sql.run(
            "INSERT INTO agent.run_log (run_id, started_at, finished_at, request, status, files_seen, "
            "rows_loaded, rows_rejected, total_reward, reflection) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (run.run_id, run.started_at, utc_now(), run.request[:1000], run.status, run.files_seen,
             run.rows_loaded, run.rows_rejected, run.total_reward, run.reflection),
        )
        self.sql.run_many(
            "INSERT INTO agent.step_log (run_id, step_no, step_name, status, error_type, strategy, explored, "
            "reward, detail, logged_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            [(run.run_id, s.step_no, s.step_name, s.status, s.error_type, s.strategy,
              None if s.explored is None else int(s.explored), s.reward, s.detail[:1000], utc_now())
             for s in run.steps],
        )

    def recent_runs(self, limit: int = 5) -> list[dict]:
        rows = self.sql.select(
            "SELECT run_id, started_at, status, files_seen, rows_loaded, rows_rejected, total_reward, "
            "user_feedback, reflection FROM agent.run_log ORDER BY started_at DESC"
        )
        return rows[:limit]

    def recent_reflections(self, limit: int = 3) -> list[str]:
        return [r["reflection"] for r in self.recent_runs(limit) if r.get("reflection")]

    def run_steps(self, run_id: str) -> list[dict]:
        return self.sql.select(
            "SELECT step_no, step_name, status, error_type, strategy, reward FROM agent.step_log "
            "WHERE run_id = ? ORDER BY step_no", (run_id,)
        )

    def set_feedback(self, run_id: str, value: int) -> None:
        self.sql.run("UPDATE agent.run_log SET user_feedback = ? WHERE run_id = ?", (value, run_id))
