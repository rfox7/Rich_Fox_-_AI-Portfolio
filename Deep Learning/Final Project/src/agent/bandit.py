"""Reinforcement learning piece: an epsilon-greedy multi-armed bandit.

For each error type (bad_date, duplicate_key, db_unavailable, ...) the agent
has several recovery strategies ("arms"). Each time it uses one, it gets a
reward between -1 and +1. The bandit keeps a running average per strategy:

* With probability 1 - epsilon it EXPLOITS: picks the best average so far.
* With probability epsilon it EXPLORES: picks a random strategy, so it keeps
  learning and can notice if something changes. Epsilon shrinks as the
  agent gains experience (decay), so mature agents waste fewer runs.
* A strategy that has never been tried gets tried first.

Scores live in agent.strategy_scores, so learning carries over between runs.
That's the "policy improvement over time" requirement.
"""
from __future__ import annotations

import random
from dataclasses import dataclass

from src import config
from src.tools.sql_tool import SqlTool, utc_now


@dataclass
class Choice:
    strategy: str
    explored: bool
    reason: str


class StrategyBandit:
    def __init__(self, sql: SqlTool, epsilon: float | None = None, seed: int | None = None):
        self.sql = sql
        self.epsilon = config.BANDIT_EPSILON if epsilon is None else epsilon
        self.rng = random.Random(seed)
        # If the database itself is down, the bandit keeps working from its last
        # known scores and saves its updates once the database is back.
        self._cache: dict[str, dict[str, dict]] = {}
        self._pending: list[tuple[str, str, float]] = []

    def scores(self, error_type: str) -> dict[str, dict]:
        try:
            self.flush()
            stats = self._read(error_type)
            self._cache[error_type] = stats
            return stats
        except Exception:  # noqa: BLE001 - database down: use what we remember
            return self._cache.get(error_type, {})

    def _read(self, error_type: str) -> dict[str, dict]:
        rows = self.sql.select(
            "SELECT strategy, pulls, total_reward FROM agent.strategy_scores WHERE error_type = ?", (error_type,)
        )
        return {
            r["strategy"]: {"pulls": int(r["pulls"]), "avg": (float(r["total_reward"]) / r["pulls"]) if r["pulls"] else 0.0}
            for r in rows
        }

    def choose(self, error_type: str, strategies: list[str]) -> Choice:
        stats = self.scores(error_type)
        untried = [s for s in strategies if stats.get(s, {}).get("pulls", 0) == 0]
        if untried:
            pick = untried[0]
            return Choice(pick, True, f"'{pick}' hasn't been tried yet for {error_type}")
        eps = self.current_epsilon(stats)
        if self.rng.random() < eps:
            pick = self.rng.choice(strategies)
            return Choice(pick, True, f"Exploring: random pick '{pick}' (epsilon={eps:.2f})")
        pick = max(strategies, key=lambda s: stats[s]["avg"])
        return Choice(pick, False, f"Best so far for {error_type}: '{pick}' (avg reward {stats[pick]['avg']:+.2f})")

    def current_epsilon(self, stats: dict[str, dict]) -> float:
        """Explore less as experience grows: epsilon * 20 / (20 + tries), never below 0.02."""
        if self.epsilon <= 0:
            return 0.0  # exploration turned off (e.g. for a demo)
        tries = sum(v["pulls"] for v in stats.values())
        return max(0.02, self.epsilon * 20 / (20 + tries))

    def update(self, error_type: str, strategy: str, reward: float) -> None:
        # update the in-memory copy right away
        stats = self._cache.setdefault(error_type, {}).setdefault(strategy, {"pulls": 0, "avg": 0.0})
        stats["avg"] = (stats["avg"] * stats["pulls"] + reward) / (stats["pulls"] + 1)
        stats["pulls"] += 1
        self._pending.append((error_type, strategy, reward))
        try:
            self.flush()
        except Exception:  # noqa: BLE001 - saved later
            pass

    def flush(self) -> None:
        while self._pending:
            error_type, strategy, reward = self._pending[0]
            self._write(error_type, strategy, reward)
            self._pending.pop(0)

    def _write(self, error_type: str, strategy: str, reward: float) -> None:
        changed = self.sql.run(
            "UPDATE agent.strategy_scores SET pulls = pulls + 1, total_reward = total_reward + ?, updated_at = ? "
            "WHERE error_type = ? AND strategy = ?",
            (reward, utc_now(), error_type, strategy),
        )
        if not changed:
            self.sql.run(
                "INSERT INTO agent.strategy_scores (error_type, strategy, pulls, total_reward, updated_at) "
                "VALUES (?, ?, 1, ?, ?)",
                (error_type, strategy, reward, utc_now()),
            )

    def nudge(self, error_type: str, strategy: str, amount: float) -> None:
        """User feedback: shift a strategy's total without counting it as a new try."""
        self.sql.run(
            "UPDATE agent.strategy_scores SET total_reward = total_reward + ?, updated_at = ? "
            "WHERE error_type = ? AND strategy = ?",
            (amount, utc_now(), error_type, strategy),
        )
