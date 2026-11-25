#!/usr/bin/env python3
"""
PiDog V2 - Hallway Patrol (Team 5, ITAI 2374 final project)

Walks from C145 to a marker at the far end of the hallway, turns around, and walks back to
the HOME marker. On the way it stays centered in the hallway, stops for obstacles and people,
steers around things in its path, warns people out loud, photographs them, and logs every
decision to ~/patrol_logs/events.csv.

Run on the PiDog:
    sudo python3 pidog_patrol.py                  # run a patrol
    sudo python3 pidog_patrol.py --test-sensors   # print distance, people, markers, battery, touch for 20 s
    sudo python3 pidog_patrol.py --test-walk      # walk straight for 6 s (check speed)
    sudo python3 pidog_patrol.py --test-photo     # stand in front of it: warns, aims at your face, saves photos
    sudo python3 pidog_patrol.py --test-center    # look left/right and print wall distances (LEFT_IS_POSITIVE_YAW)
    sudo python3 pidog_patrol.py --test-turn      # one 180 turn (tune TURN_STEPS_180)
    python3 pidog_patrol.py --make-markers        # make printable markers (any computer)

Each time through the main loop it checks, in this order:
    1. Head pat?                      -> stop and sit
    2. Battery low?                   -> stop and sit
    3. Next marker close?             -> walk up to it and turn 180 (at HOME: turn, celebrate, sit)
    4. Path blocked (< 48 cm)?        -> stop and wait; if it stays blocked, go around it
                                         (or back out if both walls are too close: corner escape)
       Person in view?                -> stop, warn out loud, aim at their face, take a photo,
                                         and wait for them to move
    5. Every 5 s: check both walls    -> steer back toward the middle
    6. Not moving forward for a while -> back up and try a new angle (stall recovery)
    7. Otherwise                      -> keep walking

Safety: pat the head (or Ctrl+C) to stop and sit. It also stops and sits when the battery
drops below LOW_BATTERY_V, or after MAX_RUN_MINUTES. Someone walks with the dog on every run.
"""

import csv
import glob
import json
import os
import sys
import time
from datetime import datetime

import cv2

# ---------------------------------------------------------------------------
# SETTINGS
# ---------------------------------------------------------------------------
TURNAROUND_MARKER = 1      # marker on the wall at the far end of the hallway
HOME_MARKER = 0            # marker on the tent behind the start spot
ARUCO_DICT = 4             # cv2.aruco.DICT_5X5_50 - must match the printed markers
MARKER_TRIGGER_PX = 18     # marker must look this wide (pixels) before we head in to turn
MARKER_APPROACH_CM = 24    # then walk up until the wall is this close
TURN_STEPS_180 = 8         # turn_right steps for a full turnaround

WALK_SPEED = 100           # do_action speed (0-100)
STEPS_QUEUED = 2           # steps kept lined up so the legs keep moving between sensor checks

STOP_DISTANCE_CM = 48      # stop when anything is closer than this in front
OBSTACLE_WAIT_S = 3.0      # wait this long for the way to clear before going around
CLEAR_BEFORE_GO_S = 1.5    # the way must stay clear this long before walking again
CORNER_CM = 60             # both walls closer than this = no room to go around (corner escape)

PHOTO_COOLDOWN_S = 15      # don't photograph the same person over and over
PHOTO_START_PITCH = 20     # tilt the head up this much to look for faces
AIM_TRIES = 10             # small head moves to center the face
AIM_GOOD_PX = 40           # face center within this many pixels of the middle = good enough
HEAD_YAW_LIMIT = 60
HEAD_PITCH_LIMIT = 35
FACE_CROP_MARGIN = 0.6     # close-up = face box plus 60% on each side
CALLOUT_TEXT = "Please clear the path, patrol coming through."
PERSON_WAIT_MAX_S = 20     # if a "person" never moves away (a poster?), move on after this long...
PERSON_IGNORE_S = 10       # ...and ignore people for this long (it still stops for obstacles)

CENTER_EVERY_S = 5.0       # how often to check the walls
HEAD_SIDE_YAW = 75         # head angle for looking at a side wall
LEFT_IS_POSITIVE_YAW = True
HEAD_SETTLE_S = 0.1
CENTER_TOLERANCE_CM = 15   # don't correct if left/right differ by less than this
MAX_WALL_CM = 250          # farther than this = open door or side hall, skip that check
CORRECTION_STEPS = 1

STALL_CHECK_S = 8.0        # if the distance ahead hasn't changed in this long while walking...
STALL_CHANGE_CM = 3.0      # ...by more than this, the dog is probably stuck (stall recovery)

LOW_BATTERY_V = 6.6        # stop and sit below this (0 = don't check)
BATTERY_CHECK_S = 10
MAX_RUN_MINUTES = 45

# Logs and photos go in the real user's home folder, even when run with sudo
HOME = os.path.expanduser("~" + os.environ.get("SUDO_USER", ""))
LOG_DIR = os.path.join(HOME, "patrol_logs")
PHOTO_DIR = os.path.join(LOG_DIR, "patrol_photos")


# ---------------------------------------------------------------------------
# LOGGING - one line per decision in ~/patrol_logs/events.csv (read by analyze_runs.py)
# ---------------------------------------------------------------------------
class RunLog:
    def __init__(self):
        os.makedirs(LOG_DIR, exist_ok=True)
        self.path = os.path.join(LOG_DIR, "events.csv")
        self.run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        if not os.path.exists(self.path):
            with open(self.path, "w", newline="") as f:
                csv.writer(f).writerow(["timestamp", "run_id", "event", "data_json"])

    def event(self, name, **data):
        print(f"[{name}] {data}", flush=True)
        try:
            with open(self.path, "a", newline="") as f:
                csv.writer(f).writerow([f"{time.time():.3f}", self.run_id, name, json.dumps(data)])
                f.flush()
                os.fsync(f.fileno())        # saved right away, so a power cut loses at most one line
        except Exception:
            pass


# ---------------------------------------------------------------------------
# MARKERS AND FACES
# ---------------------------------------------------------------------------
class MarkerFinder:
    def __init__(self):
        d = cv2.aruco.getPredefinedDictionary(ARUCO_DICT)
        if hasattr(cv2.aruco, "ArucoDetector"):               # OpenCV 4.7+
            self.detector = cv2.aruco.ArucoDetector(d, cv2.aruco.DetectorParameters())
            self.old = None
        else:
            self.detector = None
            self.old = (d, cv2.aruco.DetectorParameters_create())

    def find(self, frame):
        """Return {marker_id: width_in_pixels} for every marker in view."""
        if frame is None:
            return {}
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) if frame.ndim == 3 else frame
        if self.detector:
            corners, ids, _ = self.detector.detectMarkers(gray)
        else:
            corners, ids, _ = cv2.aruco.detectMarkers(gray, self.old[0], parameters=self.old[1])
        found = {}
        if ids is not None:
            for c, i in zip(corners, ids.flatten()):
                pts = c[0]
                found[int(i)] = round(float(max(pts[:, 0]) - min(pts[:, 0])), 1)
        return found


class FaceFinder:
    """OpenCV's built-in face detector, used to aim the head and crop the close-up."""

    def __init__(self):
        self.detector = None
        places = []
        try:
            places.append(os.path.join(cv2.data.haarcascades, "haarcascade_frontalface_default.xml"))
        except AttributeError:
            pass
        places += ["/usr/share/opencv4/haarcascades/haarcascade_frontalface_default.xml",
                   "/usr/share/opencv/haarcascades/haarcascade_frontalface_default.xml"]
        try:
            import vilib
            places += glob.glob(os.path.join(os.path.dirname(vilib.__file__), "**", "*frontalface*.xml"),
                                recursive=True)
        except Exception:
            pass
        places += glob.glob("/opt/vilib/**/*frontalface*.xml", recursive=True)
        for path in places:
            if os.path.exists(path):
                d = cv2.CascadeClassifier(path)
                if not d.empty():
                    self.detector = d
                    break

    def biggest(self, frame):
        """Return (x, y, w, h) of the biggest face in the frame, or None."""
        if self.detector is None or frame is None:
            return None
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) if frame.ndim == 3 else frame
        faces = self.detector.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(40, 40))
        if len(faces) == 0:
            return None
        return tuple(int(v) for v in max(faces, key=lambda f: f[2] * f[3]))


def crop_face(frame, box, margin=FACE_CROP_MARGIN):
    x, y, w, h = box
    mx, my = int(w * margin), int(h * margin)
    H, W = frame.shape[:2]
    return frame[max(0, y - my):min(H, y + h + my), max(0, x - mx):min(W, x + w + mx)]


def make_markers(out_dir="markers", size_px=800):
    os.makedirs(out_dir, exist_ok=True)
    d = cv2.aruco.getPredefinedDictionary(ARUCO_DICT)
    paths = []
    for marker_id, label in ((HOME_MARKER, "HOME"), (TURNAROUND_MARKER, "TURN AROUND")):
        if hasattr(cv2.aruco, "generateImageMarker"):
            img = cv2.aruco.generateImageMarker(d, marker_id, size_px)
        else:
            img = cv2.aruco.drawMarker(d, marker_id, size_px)
        img = cv2.copyMakeBorder(img, 100, 160, 100, 100, cv2.BORDER_CONSTANT, value=255)
        cv2.putText(img, f"PiDog marker {marker_id}: {label}", (100, img.shape[0] - 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.6, 0, 3)
        path = os.path.join(out_dir, f"marker_{marker_id}.png")
        cv2.imwrite(path, img)
        paths.append(path)
        print("saved", path)
    try:
        from PIL import Image
        imgs = [Image.open(p).convert("RGB") for p in paths]
        imgs[0].save("pidog_markers.pdf", save_all=True, append_images=imgs[1:], resolution=150)
        print("saved pidog_markers.pdf")
    except ImportError:
        pass
    print("Print full-page on plain paper. Place about 20-25 cm off the floor, facing down the hallway.")


class EmergencyStop(Exception):
    pass


class LowBattery(Exception):
    pass


class TimeLimit(Exception):
    pass


# ---------------------------------------------------------------------------
# THE PATROL
# ---------------------------------------------------------------------------
class HallwayPatrol:
    def __init__(self):
        from pidog import Pidog
        from vilib import Vilib
        self.Vilib = Vilib
        self.log = RunLog()
        os.makedirs(PHOTO_DIR, exist_ok=True)
        self.dog = Pidog()
        time.sleep(0.5)

        Vilib.camera_start(vflip=False, hflip=False)
        Vilib.display(local=False, web=True)          # live view at http://<pidog-ip>:9000/mjpg
        try:
            Vilib.human_detect_switch(True)
        except Exception:
            pass
        Vilib.face_detect_switch(True)
        time.sleep(1.5)

        self.markers = MarkerFinder()
        self.faces = FaceFinder()
        if self.faces.detector is None:
            print("Note: no face-detector file found - photos won't be aimed or cropped.", flush=True)
        self.tts = None
        try:
            from robot_hat import TTS
            self.tts = TTS()
            self.tts.lang("en-US")
        except Exception:
            pass

        self.start_t = time.time()
        self.next_battery = 0.0
        self.last_photo_t = -1e9                       # so the first person can be photographed right away
        self.photo_count = 0
        self.ignore_people_until = 0.0
        self.refill_at = 0

    # --- safety -----------------------------------------------------------
    def check_safety(self):
        try:
            if self.dog.dual_touch.read() != "N":
                raise EmergencyStop()
        except EmergencyStop:
            raise
        except Exception:
            pass
        if time.time() - self.start_t > MAX_RUN_MINUTES * 60:
            raise TimeLimit()
        if LOW_BATTERY_V and time.time() >= self.next_battery:
            self.next_battery = time.time() + BATTERY_CHECK_S
            volts = self.battery()
            if volts is not None and 0 < volts < LOW_BATTERY_V:
                self.log.event("low_battery", volts=volts)
                raise LowBattery()

    def battery(self):
        try:
            return round(float(self.dog.get_battery_voltage()), 2)
        except Exception:
            pass
        try:
            from robot_hat.utils import get_battery_voltage
            return round(float(get_battery_voltage()), 2)
        except Exception:
            return None

    # --- body -------------------------------------------------------------
    def act(self, action, step_count=1, speed=WALK_SPEED):
        self.check_safety()
        self.dog.do_action(action, step_count=step_count, speed=speed)
        self.dog.wait_all_done()

    def look_at(self, yaw=0, pitch=0, speed=80):
        self.dog.head_move([[yaw, 0, pitch]], immediately=True, speed=speed)
        try:
            self.dog.wait_head_done()
        except Exception:
            time.sleep(0.3)
        time.sleep(HEAD_SETTLE_S)

    def lights(self, mode, color, bps=1):
        try:
            self.dog.rgb_strip.set_mode(mode, color, bps=bps)
        except Exception:
            pass

    def sound(self, name, volume=80):
        try:
            self.dog.speak(name, volume)
        except Exception:
            pass

    def say(self, text):
        try:
            if self.tts:
                self.tts.say(text)
                return
        except Exception:
            pass
        print(f"(say) {text}", flush=True)

    def front_distance(self):
        try:
            d = float(self.dog.ultrasonic.read())
        except Exception:
            try:
                d = float(self.dog.read_distance())
            except Exception:
                return 999.0
        return round(d, 2) if d > 0 else 999.0

    def steady_distance(self):
        """Middle value of three readings, to ignore one-off bad readings."""
        readings = []
        for _ in range(3):
            readings.append(self.front_distance())
            time.sleep(0.04)
        return sorted(readings)[1]

    # --- smooth walking ---------------------------------------------------
    def leg_queue_len(self):
        try:
            return len(self.dog.legs_action_buffer)
        except AttributeError:
            pass
        try:
            return 0 if self.dog.is_legs_done() else 1
        except AttributeError:
            return None

    def keep_walking(self):
        """Keep the next steps lined up so the legs don't pause while we check sensors."""
        self.check_safety()
        before = self.leg_queue_len()
        if before is None:                           # library can't tell us: walk, then check
            self.act("forward", step_count=STEPS_QUEUED)
            return
        if before <= self.refill_at:
            self.dog.do_action("forward", step_count=STEPS_QUEUED, speed=WALK_SPEED)
            added = (self.leg_queue_len() or 0) - before
            self.refill_at = max(self.refill_at, added // 2)

    def halt(self):
        """Stop the legs right away and drop any lined-up steps."""
        try:
            self.dog.legs_action_buffer.clear()
        except Exception:
            pass
        for stop in ("legs_stop", "body_stop"):
            try:
                getattr(self.dog, stop)()
                break
            except AttributeError:
                continue
        try:
            self.dog.wait_legs_done()
        except Exception:
            self.dog.wait_all_done()

    # --- seeing -----------------------------------------------------------
    def frame(self):
        return getattr(self.Vilib, "img", None)

    def person_in_view(self):
        if time.time() < self.ignore_people_until:
            return False
        p = self.Vilib.detect_obj_parameter
        return (p.get("human_n", 0) or 0) > 0 or (p.get("face_n", 0) or 0) > 0

    def scan_sides(self):
        left_yaw = HEAD_SIDE_YAW if LEFT_IS_POSITIVE_YAW else -HEAD_SIDE_YAW
        self.look_at(yaw=left_yaw)
        left = self.steady_distance()
        self.look_at(yaw=-left_yaw)
        right = self.steady_distance()
        self.look_at(yaw=0)
        return left, right

    # --- staying centered -------------------------------------------------
    def stay_centered(self):
        left, right = self.scan_sides()
        if left > MAX_WALL_CM or right > MAX_WALL_CM:
            self.log.event("center", left=left, right=right, action="skip_open_side")
            return
        diff = left - right   # positive = more room on the left = too close to the right wall
        if abs(diff) <= CENTER_TOLERANCE_CM:
            self.log.event("center", left=left, right=right, action="ok")
            return
        direction = "turn_left" if diff > 0 else "turn_right"
        self.log.event("center", left=left, right=right, action=direction)
        self.dog.do_action(direction, step_count=CORRECTION_STEPS, speed=WALK_SPEED)

    # --- people and photos ------------------------------------------------
    def aim_at_face(self):
        """Tilt up and nudge the head until the biggest face is near the middle of the picture.
        Which way the head moves is learned on the fly (a nudge that makes it worse is flipped)."""
        yaw, pitch = 0.0, float(PHOTO_START_PITCH)
        self.look_at(yaw, pitch)
        frame = self.frame()
        box = self.faces.biggest(frame)
        if box is None:                                  # not up there: try level
            yaw, pitch = 0.0, 0.0
            self.look_at(yaw, pitch)
            frame = self.frame()
            box = self.faces.biggest(frame)
        sign = {"yaw": 1, "pitch": 1}
        for _ in range(AIM_TRIES):
            if box is None or frame is None:
                break
            H, W = frame.shape[:2]
            ex = (box[0] + box[2] / 2) - W / 2
            ey = (box[1] + box[3] / 2) - H / 2
            if abs(ex) <= AIM_GOOD_PX and abs(ey) <= AIM_GOOD_PX:
                break
            axis = "yaw" if abs(ex) >= abs(ey) else "pitch"
            err = ex if axis == "yaw" else ey
            step = max(-15, min(15, sign[axis] * 0.08 * err))
            new_yaw = max(-HEAD_YAW_LIMIT, min(HEAD_YAW_LIMIT, yaw - step)) if axis == "yaw" else yaw
            new_pitch = max(-HEAD_PITCH_LIMIT, min(HEAD_PITCH_LIMIT, pitch - step)) if axis == "pitch" else pitch
            self.look_at(new_yaw, new_pitch)
            new_frame = self.frame()
            new_box = self.faces.biggest(new_frame)
            if new_box is None:                          # lost it: wrong way. Flip and go back.
                sign[axis] *= -1
                self.look_at(yaw, pitch)
                frame = self.frame()
                box = self.faces.biggest(frame)
                continue
            new_err = ((new_box[0] + new_box[2] / 2) - W / 2) if axis == "yaw" \
                else ((new_box[1] + new_box[3] / 2) - H / 2)
            if abs(new_err) > abs(err) + 10:
                sign[axis] *= -1
            yaw, pitch, frame, box = new_yaw, new_pitch, new_frame, new_box
        return box, frame

    def take_photo(self):
        """Flash and bark, aim at the face, save the full photo plus a face close-up."""
        t0 = time.time()
        self.lights("boom", "white", bps=3)              # flash = "picture being taken"
        self.sound("single_bark_1")
        box, frame = self.aim_at_face()
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = os.path.join(PHOTO_DIR, f"person_{ts}.jpg")
        closeup = None
        if frame is not None and frame.size > 0:
            cv2.imwrite(path, frame)
            if box is not None:
                closeup = os.path.join(PHOTO_DIR, f"person_{ts}_face.jpg")
                cv2.imwrite(closeup, crop_face(frame, box))
        else:
            path = None
        self.look_at(0, 0)
        self.photo_count += 1
        self.last_photo_t = time.time()
        self.log.event("photo", file=path, closeup=closeup, face_found=box is not None,
                       seconds=round(time.time() - t0, 2))

    def handle_person(self):
        """Stop, warn, photograph, and wait for the person to move out of the way."""
        t0 = time.time()
        self.halt()
        self.act("stand", speed=100)
        self.look_at(0, 0)
        self.lights("breath", "yellow", bps=2)
        self.log.event("person_stop", distance=self.front_distance())
        self.log.event("person_callout", text=CALLOUT_TEXT)
        self.say(CALLOUT_TEXT)
        clear_since, why = None, "clear"
        while True:
            self.check_safety()
            if time.time() - self.last_photo_t >= PHOTO_COOLDOWN_S and self.person_in_view():
                self.take_photo()
                self.lights("breath", "yellow", bps=2)
            if self.person_in_view() or self.front_distance() < STOP_DISTANCE_CM:
                clear_since = None
                if time.time() - t0 > PERSON_WAIT_MAX_S:
                    self.ignore_people_until = time.time() + PERSON_IGNORE_S
                    why = "person_wait_limit"
                    break
            else:
                clear_since = clear_since or time.time()
                if time.time() - clear_since >= CLEAR_BEFORE_GO_S:
                    break
            time.sleep(0.1)
        self.log.event("resume", after="person", why=why, waited=round(time.time() - t0, 1))
        self.lights("breath", "cyan")

    # --- obstacles ----------------------------------------------------------
    def safe_forward(self, max_steps):
        taken = 0
        for _ in range(max_steps):
            if self.front_distance() <= STOP_DISTANCE_CM:
                break
            self.act("forward")
            taken += 1
        return taken

    def corner_escape(self, left, right):
        """Both walls too close to go around: back out, then angle toward the more open side."""
        self.log.event("corner_escape", left=left, right=right)
        self.act("backward", step_count=3)
        open_dir = "turn_left" if left > right else "turn_right"
        self.act(open_dir, step_count=2)

    def go_around(self, left, right):
        """Step out to the more open side, walk past, and step back in."""
        evade = "turn_right" if right >= left else "turn_left"
        undo = "turn_left" if evade == "turn_right" else "turn_right"
        turn_steps = 3
        self.act(evade, step_count=turn_steps)
        lat_out = self.safe_forward(3)                   # out to the side
        self.act(undo, step_count=turn_steps)
        pass_steps = self.safe_forward(7)                # past the obstacle
        back = max(1, turn_steps // 2)
        self.act(undo, step_count=back)
        lat_in = self.safe_forward(max(1, lat_out - 1))  # back toward the middle
        self.act(evade, step_count=back)
        self.log.event("obstacle_reroute", left=left, right=right, action=evade, lat_out=lat_out,
                       pass_steps=pass_steps, lat_in=lat_in, clear_ahead=self.front_distance())

    def handle_obstacle(self):
        """Stop and wait. If it's still blocked, go around it (or back out of a tight spot)."""
        t0 = time.time()
        self.halt()
        self.act("stand", speed=100)
        self.look_at(0, 0)
        self.lights("breath", "yellow", bps=2)
        self.log.event("obstacle_stop", distance=self.front_distance())
        clear_since = None
        while time.time() - t0 < OBSTACLE_WAIT_S:
            self.check_safety()
            if self.front_distance() >= STOP_DISTANCE_CM:
                clear_since = clear_since or time.time()
                if time.time() - clear_since >= CLEAR_BEFORE_GO_S:
                    self.log.event("resume", after="obstacle", why="clear", waited=round(time.time() - t0, 1))
                    self.lights("breath", "cyan")
                    return
            else:
                clear_since = None
            time.sleep(0.1)
        left, right = self.scan_sides()
        if left < CORNER_CM and right < CORNER_CM:
            self.corner_escape(left, right)
        else:
            self.go_around(left, right)
        self.log.event("resume", after="obstacle", why="went_around", waited=round(time.time() - t0, 1))
        self.lights("breath", "cyan")

    def stall_recovery(self, distance):
        """Legs moving but the distance ahead isn't changing: back up and try a new angle."""
        self.halt()
        self.log.event("stall_recovery", distance=distance)
        self.act("backward", step_count=2)
        left, right = self.scan_sides()
        self.act("turn_left" if left > right else "turn_right", step_count=1)

    # --- markers ------------------------------------------------------------
    def turn_around(self):
        t0 = time.time()
        self.halt()
        self.act("stand", speed=100)
        self.act("turn_right", step_count=TURN_STEPS_180)
        self.log.event("turn_180", seconds=round(time.time() - t0, 2))

    def approach_marker(self):
        """Walk up to the marker wall (until it's about MARKER_APPROACH_CM away)."""
        self.halt()
        for _ in range(15):
            if self.front_distance() <= MARKER_APPROACH_CM:
                break
            self.act("forward")

    def celebrate(self):
        self.lights("boom", "green", bps=2)
        self.sound("woohoo")
        self.act("wag_tail", step_count=5, speed=100)

    # --- main loop ----------------------------------------------------------
    def run(self):
        settings = {k: v for k, v in globals().items()
                    if k.isupper() and isinstance(v, (int, float, bool, str)) and k not in ("HOME",)}
        self.log.event("run_start", params=settings, battery=self.battery())
        result = "unknown"
        legs = [(TURNAROUND_MARKER, "far_end"), (HOME_MARKER, "home")]
        leg = 0
        next_center = time.time() + 1.0
        last_progress_t, last_progress_d = time.time(), self.front_distance()

        try:
            self.lights("breath", "cyan")
            self.act("stand", speed=80)
            self.look_at(0, 0)
            print("Patrol starting. Pat my head to stop.", flush=True)

            while True:
                self.check_safety()                               # 1-2: head pat, battery, time

                target, label = legs[leg]                         # 3: marker
                seen = self.markers.find(self.frame())
                if seen.get(target, 0) >= MARKER_TRIGGER_PX:
                    self.log.event("marker", id=target, label=label, width_px=seen[target],
                                   elapsed=round(time.time() - self.start_t, 1))
                    self.approach_marker()
                    self.turn_around()
                    leg += 1
                    if leg == len(legs):
                        self.celebrate()
                        result = "success"
                        break
                    next_center = time.time() + 1.5
                    last_progress_t, last_progress_d = time.time(), self.front_distance()
                    continue

                front = self.front_distance()                     # 4: blocked?
                if front < STOP_DISTANCE_CM and self.front_distance() < STOP_DISTANCE_CM:
                    self.handle_obstacle()
                    next_center = time.time() + 1.0
                    last_progress_t, last_progress_d = time.time(), self.front_distance()
                    continue
                if self.person_in_view():
                    self.handle_person()
                    next_center = time.time() + 1.0
                    last_progress_t, last_progress_d = time.time(), self.front_distance()
                    continue

                if time.time() >= next_center:                    # 5: walls
                    self.stay_centered()
                    next_center = time.time() + CENTER_EVERY_S
                    continue

                if time.time() - last_progress_t >= STALL_CHECK_S:  # 6: stuck?
                    if front < MAX_WALL_CM and abs(front - last_progress_d) < STALL_CHANGE_CM:
                        self.stall_recovery(front)
                    last_progress_t, last_progress_d = time.time(), self.front_distance()

                self.keep_walking()                               # 7: walk
                time.sleep(0.02)

        except EmergencyStop:
            result = "emergency_stop"
            print("[stop] head pat - stopping.", flush=True)
        except LowBattery:
            result = "low_battery"
            self.lights("breath", "red")
        except TimeLimit:
            result = "timeout"
        except KeyboardInterrupt:
            result = "keyboard_stop"
            print("Stopped by keyboard.", flush=True)

        try:
            if result != "success":
                self.halt()
            self.dog.do_action("sit", speed=80)
            self.dog.wait_all_done()
        except Exception:
            pass
        self.log.event("run_end", result=result, seconds=round(time.time() - self.start_t, 1),
                       photos=self.photo_count)
        print(f"Run {self.log.run_id}: {result}. Photos: {self.photo_count}. Log: {self.log.path}", flush=True)

    # --- test modes -----------------------------------------------------------
    def test_sensors(self, seconds=20):
        end = time.time() + seconds
        while time.time() < end:
            p = self.Vilib.detect_obj_parameter
            print(f"distance={self.front_distance():.0f} cm  people={p.get('human_n', 0)}  "
                  f"markers={self.markers.find(self.frame())}  battery={self.battery()}  "
                  f"touch={'yes' if self.dog.dual_touch.read() != 'N' else 'no'}", flush=True)
            time.sleep(0.5)

    def shutdown(self):
        try:
            self.Vilib.camera_close()
        except Exception:
            pass
        try:
            self.dog.close()
        except Exception:
            pass
        # Release the GPIO chip so the next script doesn't hit "GPIO busy"
        try:
            import lgpio
            from robot_hat.pin import Pin
            if getattr(Pin, "_chip", None) is not None:
                lgpio.gpiochip_close(Pin._chip)
                Pin._chip = None
        except Exception:
            pass


if __name__ == "__main__":
    if "--make-markers" in sys.argv:
        make_markers()
        sys.exit(0)

    patrol = HallwayPatrol()
    try:
        if "--test-sensors" in sys.argv:
            patrol.test_sensors()
        elif "--test-walk" in sys.argv:
            patrol.act("stand", speed=100)
            end = time.time() + 6
            while time.time() < end:
                patrol.keep_walking()
                time.sleep(0.02)
            patrol.halt()
            patrol.act("stand", speed=100)
        elif "--test-photo" in sys.argv:
            patrol.act("stand", speed=100)
            patrol.say(CALLOUT_TEXT)
            patrol.take_photo()
        elif "--test-center" in sys.argv:
            patrol.act("stand", speed=100)
            for _ in range(5):
                left, right = patrol.scan_sides()
                print(f"left={left:.0f} cm   right={right:.0f} cm", flush=True)
                time.sleep(1)
        elif "--test-turn" in sys.argv:
            patrol.act("stand", speed=100)
            patrol.turn_around()
        else:
            patrol.run()
    except (KeyboardInterrupt, EmergencyStop, LowBattery, TimeLimit):
        print("Stopped.", flush=True)
    finally:
        patrol.shutdown()
