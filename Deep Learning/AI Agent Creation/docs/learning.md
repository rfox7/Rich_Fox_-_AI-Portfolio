# How PipelinePilot Learns

This is the reinforcement learning part of the project. In short: every time the agent fixes a problem, it gets a score. Over time it learns which fixes earn the best scores and uses them more often.

## The problem it's solving

Real data files come in messy. For each kind of problem there are several reasonable-sounding fixes, but not all of them are actually good:

| Problem | Fixes the agent can choose from |
|---|---|
| `missing_column`: columns have different names (e.g. `qty` instead of `quantity`) | `map_aliases`, `skip_file` |
| `bad_date`: dates in the wrong format (`03/15/2026`, `15-Mar-2026`, `TBD`) | `parse_multi_format`, `reject_rows`, `skip_file` |
| `type_mismatch`: text in number columns (`$12.50`, `1,200`, `twelve`) | `coerce_numeric`, `reject_rows`, `skip_file` |
| `missing_value`: blank sale ID or store ID | `reject_rows`, `fill_default`, `skip_file` |
| `duplicate_key`: the same sale ID twice (a voided row, then the correction) | `keep_last`, `keep_first`, `reject_all_dupes` |
| `db_unavailable`: the database is paused or unreachable | `retry_backoff`, `retry_immediate`, `abort` |

The agent is **not told** which fixes are good. Two of them are traps on purpose:

- **`fill_default`** fills blank IDs with placeholder values. The rows *look* complete, but the IDs are fake.
- **`keep_first`** keeps the first copy of a duplicate, which is the voided row with quantity 0, not the correction.

A rule-based pipeline would need someone to know this ahead of time. The agent works it out from the rewards.

## The reward

After each fix, `score_fix` in `src/tools/data_tool.py` compares the data before and after and gives a score from **-1 to +1**:

```
reward = (rows truly fixed - rows still broken - good rows thrown away) / rows affected
```

- **Truly fixed:** the affected row is still there and now passes the check. A placeholder ID doesn't count.
- **Still broken:** the affected row is still there but still fails, i.e. a fake fix.
- **Good rows thrown away:** rows that had nothing wrong with them but were lost anyway (what `skip_file` does).

Here's what that gives for a file where 4 dates are in the wrong format, one of them "TBD":

| Fix | What happens | Reward |
|---|---|---|
| `parse_multi_format` | 3 dates fixed, "TBD" rejected | (3 − 0 − 0) / 4 = **+0.75** |
| `reject_rows` | all 4 rows rejected | (0 − 0 − 0) / 4 = **0** (safe, but nothing saved) |
| `skip_file` | the whole 120-row file dropped | clipped to **−1** |

For `missing_column` it's simpler: **+1** if all the needed columns are there afterward, **−1** if not.

For database outages (`_with_db_recovery` in `src/agent/core.py`):

- **Recovered:** +1, minus a small penalty for time spent waiting (at most −0.5).
- **All retries failed:** −1.
- **Gave up right away (`abort`):** −0.5.

## The learner: an epsilon-greedy bandit

`src/agent/bandit.py` keeps a running **average reward** for every fix, per problem type. When a problem comes up:

1. **Anything never tried gets tried first,** so every option gets a fair chance.
2. **Most of the time, exploit:** pick the fix with the best average so far.
3. **Some of the time, explore:** pick a fix at random. This lets the agent notice if something changes, for example if a new kind of messy date shows up that its favorite fix can't handle.

How often it explores is called **epsilon**. It starts at 0.2 (1 in 5) and **shrinks with experience**:

```
epsilon = max(0.02, 0.2 × 20 / (20 + times this problem has been seen))
```

So a brand-new agent experiments a lot, and an experienced one only experiments about 2–4% of the time. That cuts down on wasted runs once it knows what works.

The agent explains each choice in its trace, for example:

```
Thought: sales_001.csv has bad_date (4 affected). Best so far for bad_date: 'parse_multi_format' (avg reward +0.81)
Thought: sales_002.csv has type_mismatch (4 affected). Exploring: random pick 'reject_rows' (epsilon=0.04)
```

## Memory: learning carries over

Scores are saved in the `agent.strategy_scores` table (`pulls` = times tried, `total_reward` = sum of rewards). Every new run starts from what earlier runs learned, which is the "policy improvement over time" requirement.

If the database itself is down, the bandit keeps working from an in-memory copy of its last known scores. It holds its new results in a queue and saves them once the database is back, so nothing learned during an outage is lost.

## User feedback

In interactive mode (`py main.py`), the agent asks **"Was this run good? [y/n]"** after each run. The answer nudges the score of every fix that run used by **±0.25** (`FEEDBACK_WEIGHT` in `.env`). This is the "feedback mechanism" requirement: a person can push the agent away from fixes that technically scored well but weren't what they wanted.

The nudge is added to the strategy's total, so it matters most while a strategy has only been tried a few times. Once the agent has a lot of evidence, one piece of feedback moves the average only a little, which keeps a single bad click from undoing what it learned.

## Seeing it learn

`examples/train_bandit.py` runs practice episodes. Each one generates fresh files with random problems, sometimes simulates a database outage, runs the agent, and records the average reward per fix. It saves `examples/output/learning_curve.csv` and a chart:

```
py examples/train_bandit.py --episodes 100 --fresh
```

What to expect:

- **Episodes 1–10:** average reward near 0, because the agent is trying everything, including the traps.
- **Episodes 10–20:** a sharp climb as it settles on the fixes that work.
- **After that:** a level around +0.4 to +0.5, with small dips when it explores.

The average can't reach +1, because some problems truly can't be fixed (a "TBD" date, the word "twelve"), and safely rejecting those scores 0. The best possible score depends on how many unfixable values the files contain.

The final results are in [results.md](results.md).
