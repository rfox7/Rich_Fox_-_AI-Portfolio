# PiDog Hallway Patrol

A SunFounder PiDog V2 patrols a school hallway on its own. It walks from our classroom (C145) to a
marker at the far end of the hallway, turns around, and walks back to a home marker. On the way it
stays near the middle of the hallway, stops for obstacles and people, steers around things in its
path, warns people out loud, takes their picture, and logs every decision to a CSV file.

Final project for ITAI 2374 (Robot Operating System & Platform), Houston City College.

**Team:** Team 5
* Rich Fox
* Sergio Sanchez
* Brandon Matias

**Report:** _[[Link to Report:](PiDog_Hallway_Patrol_Technical_Report.md)]_ · **Demo video:** _[[link to demo](https://drive.google.com/file/d/1qw8s8pYTEk8JYlpDaW2m0q1NxXwKjsUE/view?usp=sharing)]_

## Why plain Python and not ROS 2

The course checklist asks for ROS 2. ROS 2 doesn't install directly on Raspberry Pi OS, and running it
in Docker would have meant changing the SD card the whole team shares. We kept the project as one
Python program that uses only what the SunFounder setup already installed (`pidog`, `vilib`, OpenCV),
so it can't break anything teammates rely on. The program is still split the way ROS 2 nodes would be:
sensing, deciding, acting, and logging.

## Files

| File | What it does |
|---|---|
| `pidog_patrol.py` | The patrol program, test modes, and marker maker. All settings are at the top. |
| `analyze_runs.py` | Turns the log into one summary line per run plus a success rate. Runs on the dog or a laptop. |
| `pidog_markers.pdf` | The two markers to print: 0 = HOME, 1 = TURN AROUND (5×5 marker set) |

## How it works

The program runs one loop that reads the sensors, decides what to do in a fixed order, and acts.
Safety checks always come first: _[check this order matches the final code]_

1. **Head pat?** Stop and sit.
2. **Battery low?** Stop and sit.
3. **Marker close?** Turn 180°.
4. **Path blocked?** Stop, wait, and go around if it stays blocked.
5. **Face in view?** Stop, warn, aim, and take a photo.
6. **Every 5 seconds:** check both walls and steer back toward the middle.
7. **Otherwise:** keep walking.

**Navigation.** Marker 1 is taped on the wall at the far end of the hallway. Marker 0 (HOME) stands on a
small cardboard tent just behind the start spot. When a marker looks wide enough in the camera
(`MARKER_TRIGGER_PX`, 18 pixels), the dog turns around. When it sees HOME, it's back where it started.
_[describe what it does at home: turn around and celebrate, or just stop]_

**Smooth walking.** The next steps are always lined up, so the legs keep moving while the program checks
the camera and sensors.

**Staying centered.** Every few seconds, while still walking, the dog turns its head left and right,
measures the distance to each wall, and takes a small turn toward the middle if one side is closer. If one
side reads farther than 250 cm (an open door or side hall), it skips that check.

**Stopping.** The dog stops walking when anything is closer than `STOP_DISTANCE_CM` (48 cm) or when it sees
a face. Its lights turn yellow and it says _"Please clear the path, patrol coming through."_ It waits until
the way is clear before walking again.

**Going around obstacles.** If the path stays blocked, the dog looks left and right, picks the more open
side, steps out to that side, walks past, and steps back in.

**Getting unstuck.** 
- **Corner escape:** used when both sides are close (about 50–60 cm).
- **Stall recovery:** used when the dog isn't making progress.

**Photos.** When a face is in view, the dog stops, flashes white, and barks. It nudges its head until the
face is centered, then saves the full photo plus a close-up of the face (`..._face.jpg`). It waits
`PHOTO_COOLDOWN_S` (15 seconds) before taking another.

**Logging.** Every wall check, marker, turn, stop, reroute, photo, and the run result is written to
`~/patrol_logs/events.csv`.

## Safety

- **Pat the dog's head** to stop it and make it sit. Ctrl+C does the same.
- It stops before anything closer than 48 cm, and for people.
- It stops and sits if the battery drops below `LOW_BATTERY_V` (6.6 V).
- It gives up after `MAX_RUN_MINUTES` (45 minutes).
- A person walks beside the dog on every run.

## Setup

1. Make sure the normal SunFounder PiDog setup works (a demo runs and the dog moves).
2. Check that OpenCV can read markers:
   ```bash
   python3 -c "import cv2; print(cv2.__version__, hasattr(cv2, 'aruco'))"
   ```
   It should print a version number and `True`.
3. Copy this folder to the dog, for example to `~/pidog_python`.
4. Print the markers. If you change `ARUCO_DICT` in the settings, make new ones to match:
   ```bash
   python3 pidog_patrol.py --make-markers
   ```
   Print full-page on plain paper. Place them about 20–25 cm off the floor, facing straight down the hallway.

## Running it

```bash
cd ~/pidog_python
sudo python3 pidog_patrol.py --test-sensors   # check distance, faces, markers, battery, touch
sudo python3 pidog_patrol.py --test-walk      # walk straight 6 s to check speed
sudo python3 pidog_patrol.py --test-photo     # stand in front of it: aims at your face, saves photo + close-up
sudo python3 pidog_patrol.py --test-center    # check which way the head turns (LEFT_IS_POSITIVE_YAW)
sudo python3 pidog_patrol.py --test-turn      # tune TURN_STEPS_180
sudo python3 pidog_patrol.py                  # run a patrol
python3 analyze_runs.py                       # results for all runs so far
sudo python3 radar.py                         # radar page at http://<pidog-ip>:8000
```

Live camera view while the patrol runs: `http://<pidog-ip>:9000/mjpg`

Use `tmux` so a run keeps going if Wi-Fi drops: `tmux new -s patrol`, then start the program.

**Where files go:**

| What | Folder |
|---|---|
| Log | `~/patrol_logs/events.csv` |
| Results summary | `~/patrol_logs/run_summary.csv` (made by `analyze_runs.py`) |
| Photos | `~/patrol_logs/patrol_photos/` |

The program runs with `sudo`, so these files belong to root. To make them yours:
`sudo chown -R $USER:$USER ~/patrol_logs`

## Results

From 30 logged test runs on November 16 and 18, 2026 (full details in the report):

| Measure | Result |
|---|---|
| Reached the far marker | 7 runs |
| Full round trip | 2 runs (117 s and 140 s) |
| 180° turn | 11.6 s on average (7.2–15.6 s) |
| Typical distance when stopping for an obstacle | 43 cm with the 48 cm setting, compared to 17 cm with the old 30 cm setting |
| Times it tried to go around an obstacle | 17 |
| Photos taken / with face close-up | 24 / 3 |

**Known problems:** many wall checks are skipped because of open doors, the face finder used for aiming
often misses faces the camera already spotted, and runs stopped by unplugging the dog don't log an
ending.

## Ethics and privacy

The dog photographs people in a shared hallway, and some of them may be minors. We got permission before
running it. The dog warns people with a spoken message, a bark, and a white flash before every photo.
Photos stay on the dog and are deleted after the demo.

## AI assistance

Parts of this code and documentation were written with help from an AI assistant (Claude). Our team
tested, tuned, and extended the code on the robot (going around obstacles, corner escape, stall
recovery, spoken warnings) and ran all the tests. 
