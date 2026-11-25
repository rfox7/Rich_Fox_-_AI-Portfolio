"""Shows the agent learning: runs many episodes and saves a learning curve.

Each episode makes fresh files with random planted errors, runs the agent,
and records the average reward per fix. Early on the agent tries every
strategy; later it mostly picks the ones that work, so the average climbs.
Some episodes also simulate a database outage so the retry strategies learn too.

    py examples/train_bandit.py --episodes 60
    py examples/train_bandit.py --episodes 60 --fresh   (start learning from zero)

Output: examples/output/learning_curve.csv and learning_curve.png
Tip: run this on SQLite (DB_BACKEND=sqlite) to save Azure compute.
"""
import argparse
import csv
import random
import shutil
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src import config  # noqa: E402
from src.agent import PipelineAgent  # noqa: E402
from src.db import Database  # noqa: E402
from src.simulate import generate  # noqa: E402

OUT = ROOT / "examples" / "output"


def main():
    import logging
    logging.basicConfig(level=logging.ERROR)
    ap = argparse.ArgumentParser()
    ap.add_argument("--episodes", type=int, default=60)
    ap.add_argument("--outage-rate", type=float, default=0.2)
    ap.add_argument("--epsilon", type=float, default=0.15)
    ap.add_argument("--fresh", action="store_true", help="wipe the local SQLite learning state first")
    ap.add_argument("--seed", type=int, default=7)
    args = ap.parse_args()

    config.RETRY_BASE_SECONDS = 0.2  # keep training fast
    if args.fresh and config.DB_BACKEND == "sqlite" and config.SQLITE_DIR.exists():
        shutil.rmtree(config.SQLITE_DIR)

    db = Database()
    agent = PipelineAgent(db=db, epsilon=args.epsilon, seed=args.seed, verbose=False)
    rng = random.Random(args.seed)
    OUT.mkdir(parents=True, exist_ok=True)
    rows = []

    for ep in range(1, args.episodes + 1):
        generate(files=2, rows=120, seed=args.seed * 1000 + ep, start_id=ep * 1000)
        outage = rng.random() < args.outage_rate
        if outage:
            db.close()
            db.simulated_outage_until = time.time() + rng.uniform(0.3, 1.2)  # short "paused DB" window
        report = agent.run("Load the sales files and report what happened")
        db.simulated_outage_until = 0
        rewards = [r for etype, _, r in report.fix_rewards if etype != "db_unavailable"]
        avg = sum(rewards) / len(rewards) if rewards else 0.0
        rows.append({"episode": ep, "status": report.status, "avg_fix_reward": round(avg, 3),
                     "total_reward": report.total_reward, "rows_loaded": report.rows_loaded,
                     "rows_rejected": report.rows_rejected, "outage": int(outage)})
        print(f"episode {ep:3d}  {report.status:<8} avg fix reward {avg:+.2f}  loaded {report.rows_loaded:4d}  "
              f"rejected {report.rows_rejected:3d}{'  (outage)' if outage else ''}")

    with (OUT / "learning_curve.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f"\nSaved {OUT / 'learning_curve.csv'}")

    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        eps = [r["episode"] for r in rows]
        vals = [r["avg_fix_reward"] for r in rows]
        window = 5
        rolling = [sum(vals[max(0, i - window + 1):i + 1]) / len(vals[max(0, i - window + 1):i + 1]) for i in range(len(vals))]
        plt.figure(figsize=(8, 4))
        plt.plot(eps, vals, alpha=0.35, label="per episode")
        plt.plot(eps, rolling, linewidth=2, label=f"{window}-episode average")
        plt.xlabel("Episode")
        plt.ylabel("Average reward per fix")
        plt.title("PipelinePilot learning curve")
        plt.legend()
        plt.tight_layout()
        plt.savefig(OUT / "learning_curve.png", dpi=150)
        print(f"Saved {OUT / 'learning_curve.png'}")
    except ImportError:
        print("Install matplotlib to also save a chart.")

    print("\nLearned strategy scores:")
    for etype in ["bad_date", "type_mismatch", "missing_value", "duplicate_key", "missing_column", "db_unavailable"]:
        stats = agent.bandit.scores(etype)
        ranked = sorted(stats.items(), key=lambda kv: kv[1]["avg"], reverse=True)
        print(f"  {etype:<15} " + "  ".join(f"{s}={v['avg']:+.2f} (n={v['pulls']})" for s, v in ranked))


if __name__ == "__main__":
    main()
