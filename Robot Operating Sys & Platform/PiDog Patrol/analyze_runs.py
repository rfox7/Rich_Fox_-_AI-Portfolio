#!/usr/bin/env python3
"""
Summarize PiDog patrol runs (runs on the dog or any PC).

Reads every log in the log folder:
  - patrol_<date>_<time>.jsonl  one file per run (current pidog_patrol.py)
  - events.csv                  older test runs (earlier versions of the script)

  python3 analyze_runs.py                     # reads ~/patrol_logs
  python3 analyze_runs.py path/to/folder      # or a copy on your laptop
  python3 analyze_runs.py path/to/file.jsonl  # or a single log file

Prints one row per run plus a success rate, and saves run_summary.csv in the log folder.

The current script doesn't log how a run ended, so a run counts as "success" when the
dog reached the HOME marker, and "no end record" otherwise.
"""

import csv
import glob
import io
import json
import os
import statistics
import sys
from collections import OrderedDict

HOME_MARKER = 0


def load_jsonl(path):
    """One run per file. Run id = the date/time in the file name."""
    run_id = os.path.basename(path).replace("patrol_", "").replace(".jsonl", "")
    events = []
    with open(path, encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip().replace("\x00", "")
            if not line:
                continue
            try:
                rec = json.loads(line)
            except ValueError:
                continue                        # half-written line (power cut)
            t = rec.pop("t", None)
            name = rec.pop("event", "")
            events.append((t, name, rec))
    return {run_id: events} if events else {}


def load_events_csv(path):
    """Older format: many runs in one CSV. Empty bytes from power cuts are removed."""
    text = open(path, "rb").read().replace(b"\x00", b"").decode("utf-8", errors="replace")
    runs = OrderedDict()
    for row in csv.DictReader(io.StringIO(text)):
        try:
            t = float(row["timestamp"])
            data = json.loads(row["data_json"] or "{}")
        except (ValueError, KeyError, TypeError):
            continue
        runs.setdefault(row["run_id"], []).append((t, row["event"], data))
    return runs


def load_all(target):
    runs = OrderedDict()
    if os.path.isfile(target):
        files = [target]
    else:
        files = sorted(glob.glob(os.path.join(target, "events.csv"))) + \
                sorted(glob.glob(os.path.join(target, "patrol_*.jsonl")))
    for path in files:
        runs.update(load_events_csv(path) if path.endswith(".csv") else load_jsonl(path))
    return runs


def summarize(runs):
    rows = []
    for run_id, events in sorted(runs.items()):
        def of(name):
            return [d for _, e, d in events if e == name]

        centers = [d for d in of("center") if d.get("action") != "skip_open_side"]
        offsets = [abs(d["left"] - d["right"]) / 2 for d in centers
                   if isinstance(d.get("left"), (int, float)) and isinstance(d.get("right"), (int, float))]
        markers = of("marker")
        turns = [d["seconds"] for d in of("turn_180") if "seconds" in d]
        stops = [d["distance"] for d in of("obstacle_stop") if "distance" in d]
        times = [t for t, _, _ in events if isinstance(t, (int, float))]

        end = of("run_end")
        if end:
            result = end[0].get("result", "unknown")
        elif any(d.get("id") == HOME_MARKER for d in markers):
            result = "success"
        else:
            result = "no end record"

        rows.append({
            "run_id": run_id,
            "result": result,
            "seconds": round(max(times) - min(times), 1) if len(times) > 1 else "",
            "markers_reached": len(markers),
            "turns": len(turns),
            "avg_turn_s": round(statistics.mean(turns), 1) if turns else "",
            "obstacle_stops": len(stops),
            "median_stop_cm": round(statistics.median(stops), 1) if stops else "",
            "reroutes": len(of("obstacle_reroute")),
            "photos": len(of("photo")),
            "face_closeups": sum(1 for d in of("photo") if d.get("closeup")),
            "center_checks": len(of("center")),
            "corrections": sum(1 for d in centers if d.get("action") in ("turn_left", "turn_right")),
            "avg_off_center_cm": round(statistics.mean(offsets), 1) if offsets else "",
            "max_off_center_cm": round(max(offsets), 1) if offsets else "",
        })
    return rows


def main():
    home = os.path.expanduser("~" + os.environ.get("SUDO_USER", ""))
    target = sys.argv[1] if len(sys.argv) > 1 else os.path.join(home, "patrol_logs")
    rows = summarize(load_all(target))
    if not rows:
        print("No runs found in", target)
        return

    cols = list(rows[0].keys())
    widths = {c: max(len(c), *(len(str(r[c])) for r in rows)) for c in cols}
    print("  ".join(c.ljust(widths[c]) for c in cols))
    for r in rows:
        print("  ".join(str(r[c]).ljust(widths[c]) for c in cols))

    ok = sum(1 for r in rows if r["result"] == "success")
    far = sum(1 for r in rows if r["markers_reached"] >= 1)
    print(f"\nRuns: {len(rows)}   Reached far marker: {far}   Full round trips: {ok}   "
          f"Success rate: {ok / len(rows):.0%}")

    folder = target if os.path.isdir(target) else os.path.dirname(target) or "."
    out = os.path.join(folder, "run_summary.csv")
    with open(out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)
    print("Saved", out)


if __name__ == "__main__":
    main()
