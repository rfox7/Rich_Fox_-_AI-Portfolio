"""PipelineAgent: the main loop.

    request -> screen -> understand -> plan -> execute (with recovery) -> reflect -> report
                 |                                  |
            safety layer                 bandit picks a fix for each
                                         problem and learns from the reward

Every step is written to a trace in plain language (Thought / Action /
Observation, ReAct style), so the agent's reasoning is visible in the
console, the report and agent.step_log.
"""
from __future__ import annotations

import time
from dataclasses import dataclass, field

import pandas as pd

from src import config
from src.agent import reasoning
from src.agent.bandit import StrategyBandit
from src.agent.memory import LongTermMemory, RunMemory
from src.db import Database
from src.safety import CAPABILITIES, screen_request
from src.tools import SqlTool, data_tool, file_tool, safe_tool_call

DB_STRATEGIES = ["retry_backoff", "retry_immediate", "abort"]


@dataclass
class AgentReport:
    run_id: str | None
    status: str
    message: str
    rows_loaded: int = 0
    rows_rejected: int = 0
    total_reward: float = 0.0
    trace: list[str] = field(default_factory=list)
    fix_rewards: list[tuple[str, str, float]] = field(default_factory=list)  # (error_type, strategy, reward)

    def __str__(self) -> str:
        return self.message


class PipelineAgent:
    def __init__(self, db: Database | None = None, epsilon: float | None = None,
                 seed: int | None = None, verbose: bool = True):
        self.db = db or Database()
        self.sql = SqlTool(self.db)
        self.bandit = StrategyBandit(self.sql, epsilon=epsilon, seed=seed)
        self.memory = LongTermMemory(self.sql)
        self.verbose = verbose
        self.trace: list[str] = []

    # ================================================================ public
    def run(self, request: str) -> AgentReport:
        self.trace = []

        # 1. Safety screen ---------------------------------------------------
        screen = screen_request(request)
        if not screen.allowed:
            self._say(f"Thought: screened the request -> {screen.category}, not running anything")
            return AgentReport(None, "refused", screen.reason, trace=self.trace)

        run = RunMemory(request=request)
        self._say(f"Run {run.run_id[:8]} started: \"{request}\"")

        # 2. Make sure the database is reachable (first tool use) ------------
        if not self._with_db_recovery(run, "connect", self.sql.ping):
            run.status = "failed"
            return self._finish(run, save=False)

        # 3. Understand + plan ------------------------------------------------
        task = reasoning.parse_request(request)
        run.plan = reasoning.make_plan(task)
        self._say(f"Thought: intent={task.intent}, files={task.file_pattern}, dry_run={task.dry_run} ({task.notes})")
        self._say(f"Plan: {' -> '.join(run.plan)}")

        if task.intent == "status":
            return self._status_report()

        # 4. Execute ------------------------------------------------------------
        found = safe_tool_call(file_tool.list_files, task.file_pattern, fallback=[])
        files = found.data if found.ok else []
        run.log("discover_files", "success" if found.ok else "error",
                detail=f"{len(files)} file(s)" if found.ok else found.error)
        if not files:
            self._say(f"Observation: no files match '{task.file_pattern}'. {found.error or ''}".strip())
            run.status = "no_files"
            return self._finish(run)
        self._say(f"Action: file_tool.list_files -> {files}")

        for name in files:
            self._process_file(run, name, dry_run=task.dry_run)

        if not task.dry_run and run.rows_loaded:
            merged = self._with_db_recovery(run, "merge", lambda: self.sql.merge_to_dw(run.run_id))
            if merged is False:
                run.status = "partial"
        run.status = run.status if run.status != "running" else ("checked" if task.dry_run else "success")

        # 5. Reflect + save ------------------------------------------------------
        return self._finish(run)

    def give_feedback(self, run_id: str, thumbs_up: bool) -> str:
        """User feedback on a whole run nudges every strategy that run used."""
        amount = config.FEEDBACK_WEIGHT if thumbs_up else -config.FEEDBACK_WEIGHT
        used = {(s["error_type"], s["strategy"]) for s in self.memory.run_steps(run_id) if s["strategy"]}
        for error_type, strategy in used:
            self.bandit.nudge(error_type, strategy, amount)
        self.memory.set_feedback(run_id, 1 if thumbs_up else -1)
        return f"Thanks. Adjusted {len(used)} strategy score(s) by {amount:+.2f}."

    # ================================================================ steps
    def _process_file(self, run: RunMemory, name: str, dry_run: bool) -> None:
        run.files_seen += 1
        read = safe_tool_call(file_tool.read_csv, name)
        if not read.ok:
            run.log("read_file", read.status, error_type=read.error_type, detail=f"{name}: {read.error}")
            self._say(f"Observation: couldn't read {name} ({read.error_type}): {read.error}")
            return
        df: pd.DataFrame = read.data
        self._say(f"Action: read {name} -> {len(df)} rows")
        rejected: list[pd.DataFrame] = []
        handled: set[str] = set()

        # ReAct loop: look at the data, pick a fix, check the result, repeat
        while True:
            issues = data_tool.profile(df) if len(df) else {}
            pending = [e for e in data_tool.ERROR_ORDER if e in issues and e not in handled]
            if not pending:
                break
            etype = pending[0]
            handled.add(etype)
            affected = issues[etype]
            choice = self.bandit.choose(etype, data_tool.STRATEGIES[etype])
            what = f"{len(affected)} columns to map" if etype == "missing_column" else f"{len(affected)} row(s) affected"
            self._say(f"Thought: {name} has {etype} ({what}). {choice.reason}")

            fix = safe_tool_call(data_tool.apply_strategy, df, etype, choice.strategy, affected)
            if not fix.ok:
                reward = -1.0
                run.log("fix_issues", "error", error_type=etype, strategy=choice.strategy,
                        explored=choice.explored, reward=reward, detail=fix.error)
                self.bandit.update(etype, choice.strategy, reward)
                continue
            new_df, rej, note = fix.data
            reward = data_tool.score_fix(df, new_df, etype, affected)
            self.bandit.update(etype, choice.strategy, reward)
            run.log("fix_issues", "success", error_type=etype, strategy=choice.strategy,
                    explored=choice.explored, reward=reward, detail=f"{name}: {note}")
            self._say(f"Observation: {note}. Reward {reward:+.2f}")
            df = new_df
            if len(rej):
                rejected.append(rej)
            if choice.strategy == "skip_file":
                break

        # Final quality gate: anything still invalid is rejected, never loaded
        if len(df):
            ok = data_tool.valid_mask(df)
            if (~ok).any():
                rejected.append(df[~ok].assign(_reason="failed final validation"))
                self._say(f"Observation: {int((~ok).sum())} row(s) still invalid -> rejected")
            df = df[ok]
        rej_df = pd.concat(rejected) if rejected else pd.DataFrame()
        run.log("validate", "success", detail=f"{name}: {len(df)} good, {len(rej_df)} rejected")

        run.rows_rejected += len(rej_df)
        if dry_run:
            self._say(f"Dry run: {name} would load {len(df)} rows")
            return
        staged = self._with_db_recovery(run, "stage", lambda: (self.sql.stage_clean(run.run_id, df, name),
                                                               self.sql.stage_rejects(run.run_id, rej_df, name)))
        if staged is not False:
            run.rows_loaded += len(df)
            self._say(f"Action: staged {len(df)} rows from {name}")

    def _with_db_recovery(self, run: RunMemory, step: str, fn):
        """Run a database step. If the database is down, let the bandit pick how to recover."""
        first = safe_tool_call(fn)
        if first.ok:
            run.log(step, "success")
            return first.data if first.data is not None else True
        if first.error_type != "db_unavailable":
            run.log(step, first.status, error_type=first.error_type, detail=first.error)
            self._say(f"Observation: {step} failed ({first.error_type}): {first.error}")
            return False

        choice = self.bandit.choose("db_unavailable", DB_STRATEGIES)
        self._say(f"Thought: database unavailable during {step}. {choice.reason}")
        waited, result = 0.0, first
        if choice.strategy != "abort":
            for attempt in range(1, 4):
                if choice.strategy == "retry_backoff":
                    pause = config.RETRY_BASE_SECONDS * (2 ** (attempt - 1))
                    time.sleep(pause)
                    waited += pause
                self.db.close()
                result = safe_tool_call(fn)
                self._say(f"Action: retry {attempt} ({choice.strategy}) -> {result.status}")
                if result.ok:
                    break

        if choice.strategy == "abort":
            reward = -0.5
        elif result.ok:
            reward = round(1.0 - min(waited / (config.RETRY_BASE_SECONDS * 14), 0.5), 3)
        else:
            reward = -1.0
        self.bandit.update("db_unavailable", choice.strategy, reward)
        run.log(step, "success" if result.ok else "error", error_type="db_unavailable",
                strategy=choice.strategy, explored=choice.explored, reward=reward, detail=result.error or "")
        return (result.data if result.data is not None else True) if result.ok else False

    # ================================================================ output
    def _finish(self, run: RunMemory, save: bool = True) -> AgentReport:
        past = []
        try:
            past = self.memory.recent_reflections()
        except Exception:  # noqa: BLE001
            pass
        run.reflection = reasoning.reflect(run, past)
        if save:
            saved = safe_tool_call(self.memory.save_run, run)
            if not saved.ok:
                self._say(f"Note: couldn't save run history ({saved.error_type})")
        self._say(f"Reflection: {run.reflection}")

        fixes = [s for s in run.steps if s.strategy]
        lines = [
            f"Run {run.run_id[:8]} - {run.status.upper()}",
            f"Files: {run.files_seen} | Rows loaded: {run.rows_loaded} | Rows rejected: {run.rows_rejected} "
            f"| Total reward: {run.total_reward:+.2f}",
        ]
        if fixes:
            lines.append("Fixes used:")
            lines += [f"  - {s.error_type}: {s.strategy}{' (exploring)' if s.explored else ''} "
                      f"-> reward {s.reward:+.2f}" for s in fixes]
        lines.append(f"What I learned: {run.reflection}")
        lines.append("Limits: sales CSVs from the incoming folder only; never deletes data, drops tables or shares credentials.")
        return AgentReport(run.run_id, run.status, "\n".join(lines), run.rows_loaded,
                           run.rows_rejected, run.total_reward, self.trace,
                           [(s.error_type, s.strategy, s.reward) for s in fixes])

    def _status_report(self) -> AgentReport:
        runs = self.memory.recent_runs(5)
        if not runs:
            return AgentReport(None, "status", "No runs recorded yet.", trace=self.trace)
        lines = ["Recent runs (times in UTC):"]
        for r in runs:
            lines.append(f"  {str(r['started_at'])[:19]}  {r['run_id'][:8]}  {r['status']:<8} "
                         f"loaded={r['rows_loaded']} rejected={r['rows_rejected']} reward={float(r['total_reward']):+.2f}")
        return AgentReport(None, "status", "\n".join(lines), trace=self.trace)

    def _say(self, text: str) -> None:
        self.trace.append(text)
        if self.verbose:
            print(text)
