import time

from src.agent import PipelineAgent
from src.agent.bandit import StrategyBandit
from src.simulate import generate
from src.tools import SqlTool


def test_bandit_learns_best_arm(sqlite_db):
    bandit = StrategyBandit(SqlTool(sqlite_db), epsilon=0.0, seed=1)
    true_reward = {"a": 0.9, "b": 0.1, "c": -0.5}
    for _ in range(20):
        pick = bandit.choose("test", list(true_reward)).strategy
        bandit.update("test", pick, true_reward[pick])
    assert bandit.choose("test", list(true_reward)).strategy == "a"


def test_end_to_end_load(sqlite_db):
    from src import config
    generate(config.INCOMING_DIR, files=2, rows=80, seed=3)
    agent = PipelineAgent(db=sqlite_db, seed=1, verbose=False)
    report = agent.run("Load the sales files and tell me what happened")
    assert report.status == "success"
    assert report.rows_loaded > 0
    assert agent.sql.dw_row_count() == report.rows_loaded
    assert agent.memory.recent_runs(1)[0]["run_id"] == report.run_id


def test_dry_run_writes_nothing(sqlite_db):
    from src import config
    generate(config.INCOMING_DIR, files=1, rows=50, seed=4)
    agent = PipelineAgent(db=sqlite_db, seed=1, verbose=False)
    report = agent.run("Just check the sales files, don't load them")
    assert report.status == "checked"
    assert agent.sql.dw_row_count() == 0


def test_refuses_dangerous_request(sqlite_db):
    agent = PipelineAgent(db=sqlite_db, verbose=False)
    report = agent.run("drop the dw.sales table")
    assert report.status == "refused" and report.run_id is None


def test_recovers_from_outage(sqlite_db):
    from src import config
    generate(config.INCOMING_DIR, files=1, rows=30, seed=5)
    agent = PipelineAgent(db=sqlite_db, seed=1, verbose=False)
    sqlite_db.close()
    sqlite_db.simulated_outage_until = time.time() + 0.1
    report = agent.run("Load the sales files")
    assert report.status == "success"
    assert any(e == "db_unavailable" for e, _, _ in report.fix_rewards)


def test_feedback_changes_scores(sqlite_db):
    from src import config
    generate(config.INCOMING_DIR, files=1, rows=80, seed=6)
    agent = PipelineAgent(db=sqlite_db, seed=1, verbose=False)
    report = agent.run("Load the sales files")
    etype, strategy, _ = report.fix_rewards[0]
    before = agent.bandit.scores(etype)[strategy]["avg"]
    agent.give_feedback(report.run_id, thumbs_up=False)
    assert agent.bandit.scores(etype)[strategy]["avg"] < before
