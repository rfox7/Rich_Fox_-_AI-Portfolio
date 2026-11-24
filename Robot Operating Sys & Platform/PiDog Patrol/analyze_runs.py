#!/usr/bin/env python3
"""
Summarize patrol runs from ~/patrol_logs/events.csv (runs on the dog or any PC).

  python3 analyze_runs.py                         # reads ~/patrol_logs/events.csv
  python3 analyze_runs.py path/to/events.csv      # or a copy on your laptop

Prints one row per run plus overall totals, and writes run_summary.csv next to events.csv.
"""

import csv
import json
import os
import statistics
import sys
from collections import defaultdict


def summarize(events_path):
    runs = defaultdict(list)
    with open(events_path, newline="") as f:
        for row in csv.DictReader(f):
            runs[row["run_id"]].append((row["event"], json.loads(row["data_json"] or "{}")))

    rows = []
    for run_id, events in sorted(runs.items()):
        centers = [d for e, d in events if e == "center" and d.get("action") != "skip_open_side"]
        offsets = [abs(d["left"] - d["right"]) / 2 for d in centers]
        corrections = sum(1 for d in centers if d["action"] in ("turn_left", "turn_right"))
        end = next((d for e, d in events if e == "run_end"), {})
        turns = [d["seconds"] for e, d in events if e == "turn_180"]
        rows.append({
            "run_id": run_id,
            "result": end.get("result", "incomplete"),
            "seconds": end.get("seconds", ""),
            "markers_reached": sum(1 for e, _ in events if e == "marker"),
            "photos": sum(1 for e, _ in events if e == "photo"),
            "obstacle_stops": sum(1 for e, _ in events if e == "obstacle_stop"),
            "center_checks": len(centers),
            "corrections": corrections,
            "avg_off_center_cm": round(statistics.mean(offsets), 1) if offsets else "",
            "max_off_center_cm": round(max(offsets), 1) if offsets else "",
            "avg_turn_s": round(statistics.mean(turns), 1) if turns else "",
        })
    return rows


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.expanduser("~" + os.environ.get("SUDO_USER", "")), "patrol_logs", "events.csv")
    rows = summarize(path)
    if not rows:
        print("No runs found in", path)
        return

    cols = list(rows[0].keys())
    widths = {c: max(len(c), *(len(str(r[c])) for r in rows)) for c in cols}
    print("  ".join(c.ljust(widths[c]) for c in cols))
    for r in rows:
        print("  ".join(str(r[c]).ljust(widths[c]) for c in cols))

    done = [r for r in rows if r["result"] != "incomplete"]
    ok = sum(1 for r in done if r["result"] == "success")
    print(f"\nRuns: {len(done)}   Successful: {ok}   Success rate: {ok / len(done):.0%}" if done else "")

    out = os.path.join(os.path.dirname(path), "run_summary.csv")
    with open(out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)
    print("Saved", out)


if __name__ == "__main__":
    main()
