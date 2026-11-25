# PiDog Hallway Patrol

A SunFounder PiDog V2 patrols a school hallway on its own. It walks from our classroom (C145) to a
marker at the far end of the hallway, turns around, and walks back to a home marker. On the way it
stays near the middle of the hallway, stops for obstacles and steers around them, photographs people
it sees, and logs every decision to a file.

Final project for ITAI 2374 (Robot Operating System & Platform), Houston City College.

**Team 5:** Rich Fox, Sergio Sanchez, Brandon Matias

**Report:** [Technical report](PiDog_Hallway_Patrol_Technical_Report.md) · **Demo video:** [Watch the demo](https://drive.google.com/file/d/1qw8s8pYTEk8JYlpDaW2m0q1NxXwKjsUE/view?usp=sharing)

## Why plain Python and not ROS 2

The course checklist asks for ROS 2. ROS 2 doesn't install directly on Raspberry Pi OS, and running it
in Docker would have meant changing the SD card the whole team shares. We kept the project as one
Python program that uses only what the SunFounder setup already installed (`pidog`, `vilib`, OpenCV),
so it can't break anything teammates rely on. The program is still split the way ROS 2 nodes would be:
sensing, deciding, acting, and logging.

## Files

| File | What it does |
|---|---|
| `pidog_patrol.py` | The patrol program. All settings are at the top. |
| `analyze_runs.py` | Turns the logs into one summary line per run plus a success rate. Runs on the dog or a laptop. |
| `make_markers.py` | Makes the two printable markers (`pidog_markers.pdf`). |
| `pidog_markers.pdf` | The two markers to print: 0 = HOME, 1 = TURN AROUND (5×5 marker set) |
| `events.csv` | Log of our 30 test runs on November 16 and 18, used for the results in the report |
| `PiDog_Hallway_Patrol_Technical_Report.md` | The technical report (also as a Word file) |

## How it works

The program runs one loop. Each time through, it checks these in order:

1. **Head pat, or 45 minutes up?** Stop and sit.
2. **Next marker close?** Walk up to it and turn 180°.
3. **Something closer than 48 cm?** Stop and go around it.
4. **Person in view?** Stop, aim the head at their face, and take a photo.
5. **Every 5 seconds:** check both walls and steer back toward the middle.
6. **Otherwise:** take 2 more steps forward.

**Navigation.** Marker 1 is taped on the wall at the far end of the hallway. Marker 0 (HOME) stands on a
small cardboard tent just behind the start spot. When the marker it's heading for looks at least
`MARKER_TRIGGER_PX` (18 pixels) wide in the camera, the dog keeps stepping forward until the distance
sensor reads about 24 cm, then turns 180° (8 `turn_right` steps). At HOME it turns around once more,
so it ends facing the way it started, and sits down.

**Staying centered.** Every 5 seconds the dog turns its head 75° left and right and measures the
distance to each wall. If one wall is more than 15 cm closer than the other, it takes one small turn
away from it. If either side reads farther than 250 cm (an open door or side hall), it skips that check.

**Going around obstacles.** When anything is closer than `STOP_DISTANCE_CM` (48 cm), the dog stops and
looks left and right. It then:

1. Turns 3 steps toward the more open side and walks up to 3 steps out.
2. Turns back parallel to the hallway and walks up to 7 steps past the obstacle.
3. Angles back toward the middle, walks back in, and straightens out.

Before every forward step during the detour it checks the distance sensor again, and skips the step if
something is in the way.

**Photos.** When the camera detects a person, the dog stops, tilts its head up 20°, and nudges its head
up to 10 times to center their face. It saves the full photo, plus a close-up of the face when it found
one. It waits `PHOTO_COOLDOWN_S` (15 seconds) before taking another photo.

**Logging.** Each run writes its own file, `patrol_<date>_<time>.jsonl`, with one line per event: run
start (all settings and the battery voltage), markers seen, wall checks, obstacle stops and detours,
turns, and photos.

## Safety

- **Pat the dog's head** to stop it and make it sit. Ctrl+C does the same.
- It stops before anything closer than 48 cm.
- It stops and sits after `MAX_RUN_MINUTES` (45 minutes).
- A person walks beside the dog on every run.

The battery voltage is logged at the start of each run but not checked during the run, so watch the
battery. (`LOW_BATTERY_V` is in the settings but this version doesn't use it.)

## Setup

1. Make sure the normal SunFounder PiDog setup works (a demo runs and the dog moves).
2. Check that OpenCV can read markers:
   ```bash
   python3 -c "import cv2; print(cv2.__version__, hasattr(cv2, 'aruco'))"
   ```
   It should print a version number and `True`.
3. Copy this folder to the dog, for example to `~/pidog_python`.
4. The script saves logs and photos under `/home/user05/patrol_logs`. On a different login, change
   `LOG_DIR` at the top of `pidog_patrol.py`.
5. Print `pidog_markers.pdf` full-page on plain paper. Place the markers about 20–25 cm off the floor,
   facing straight down the hallway. If you change `ARUCO_DICT`, make new markers with
   `python3 make_markers.py` (after changing it there too).

## Running it

```bash
cd ~/pidog_python
sudo python3 pidog_patrol.py      # run a patrol
python3 analyze_runs.py           # results for all runs so far
```

Live camera view while the patrol runs: `http://<pidog-ip>:9000/mjpg`

Use `tmux` so a run keeps going if Wi-Fi drops: `tmux new -s patrol`, then start the program.

**Where files go:**

| What | Where |
|---|---|
| Logs | `/home/user05/patrol_logs/patrol_<date>_<time>.jsonl` (one per run) |
| Results summary | `/home/user05/patrol_logs/run_summary.csv` (made by `analyze_runs.py`) |
| Photos | `/home/user05/patrol_logs/patrol_photos/` (`person_...jpg` and `closeup_...jpg`) |

The program runs with `sudo`, so these files belong to root. To make them yours:
`sudo chown -R $USER:$USER ~/patrol_logs`

`analyze_runs.py` reads both the per-run log files and the older `events.csv`. The current script
doesn't log how a run ended, so a run counts as a success when the dog reached the HOME marker.

## Results

From 30 logged test runs on November 16 and 18, 2026, while we were developing the program (full
details in the report):

| Measure | Result |
|---|---|
| Reached the far marker | 7 runs |
| Full round trip | 2 runs (117 s and 140 s) |
| 180° turn | 11.6 s on average (7.2–15.6 s) |
| Typical distance when stopping for an obstacle | 43 cm with the 48 cm setting, compared to 17 cm with the old 30 cm setting |
| Times it tried to go around an obstacle | 17 |
| Photos taken / with face close-up | 24 / 3 |

**Known problems:**

- Many wall checks are skipped because of open doors and side halls.
- The photo step finds a face to aim at only rarely. It reads face data under `face_n` / `face_x`,
  which may not be the names SunFounder's camera library uses for faces.
- The log doesn't record how a run ended (finished, head pat, or Ctrl+C).
- No low-battery stop during a run.

## Ethics and privacy

The dog photographs people in a shared hallway from floor level. We only photographed classmates, a
team member walked with the dog the whole time, and we stopped the program when someone it shouldn't
photograph was in view. This version gives no warning (sound or light) before a photo.

## AI assistance

Parts of this code and documentation were written with help from an AI assistant (Claude). Our team
tested, tuned, and extended the code on the robot (including the obstacle detour) and ran all the
tests.
