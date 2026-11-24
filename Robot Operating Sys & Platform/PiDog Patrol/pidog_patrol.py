#!/usr/bin/env python3
"""
PiDog V2 - "Hallway Patrol" (plain Python, no ROS 2, no Docker)

Walks down the hallway from C145, turns around at the far marker, walks back,
turns around again at the HOME marker, and celebrates. Along the way it:
  - keeps itself centered in the hallway (head sweeps + ultrasonic sensor)
  - stops for obstacles
  - stops and takes a photo when it sees a face
  - logs every decision to a CSV file for the results section of the report

Run on the PiDog:
    sudo python3 pidog_patrol.py                 # start the patrol
    sudo python3 pidog_patrol.py --test-center   # look left/right and print wall distances
    sudo python3 pidog_patrol.py --test-turn     # do one 180 turn (for tuning TURN_STEPS_180)
    sudo python3 pidog_patrol.py --test-sensors  # print distance, faces, markers, battery for 20 s
    sudo python3 pidog_patrol.py --test-walk     # walk straight 6 s (check speed / try WALK_GAIT)
    sudo python3 pidog_patrol.py --test-photo    # aim at a face and save a photo + face close-up
    python3 pidog_patrol.py --make-markers       # make printable markers (any computer)
    python3 analyze_runs.py                      # summarize all logged runs

ROUTE SETUP
        [Marker 0 tent]  DOG ->  .........hallway.........  [Marker 1 on far wall]
         (just behind                                        (facing the dog)
          the start spot)

SAFETY
  - Pat its head (touch sensor) at any time = emergency stop.
  - It stops if anything is closer than STOP_DISTANCE_CM in front of it.
  - It stops and sits if the battery runs low.
  - Someone should walk with it the whole time.

Nothing here installs or changes anything system-wide. It only uses the
SunFounder libraries (pidog, vilib) and OpenCV that the normal PiDog setup
already installed, and it only writes to ~/patrol_logs and ~/patrol_photos.

NOTE: All numbers marked TUNE need adjusting on your actual dog and floor.
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

WALK_GAIT = "forward"      # "forward" = normal walk; try "trot" for a faster gait on your floor
WALK_SPEED = 100           # do_action speed (0-100)
STEPS_QUEUED = 2           # steps kept lined up so the legs never pause between sensor checks
TURN_STEPS_180 = 8         # TUNE: how many turn_left steps = ~180 degrees
STOP_DISTANCE_CM = 30      # obstacle stop distance
MARKER_TRIGGER_PX = 90     # TUNE: marker must look this wide (pixels) = "close enough"
PHOTO_COOLDOWN_S = 15      # don't photograph the same person over and over
PHOTO_START_PITCH = 20     # TUNE: if no face is in view, tilt the head up this much and look again
                           #       (if the head tilts DOWN, use -20)
AIM_TRIES = 10             # how many small head moves to center the face
AIM_GOOD_PX = 40           # face center within this many pixels of the middle = good enough
HEAD_YAW_LIMIT = 60        # don't turn the head farther than this (degrees)
HEAD_PITCH_LIMIT = 35      # don't tilt the head farther than this (degrees)
FACE_CROP_MARGIN = 0.6     # close-up = face box plus 60% extra on each side
MAX_RUN_MINUTES = 45       # give up and stop after this long
LOW_BATTERY_V = 6.6        # TUNE: stop and sit below this voltage (0 = don't check)

# --- Hallway centering ---
CENTER_EVERY_S = 3.0         # how often (seconds) to look left/right while walking; 999 = off
HEAD_SETTLE_S = 0.15         # pause after a head move before reading the sensor
HEAD_SIDE_YAW = 75           # TUNE: head yaw (degrees) for looking at a side wall
LEFT_IS_POSITIVE_YAW = True  # TUNE: run --test-center; if "left" is really the right wall, set False
CENTER_TOLERANCE_CM = 15     # if left/right differ by less than this, don't correct
MAX_WALL_CM = 250            # farther than this = open doorway/side hall, skip that check
CORRECTION_STEPS = 1         # turn steps per correction (raise if it corrects too slowly)

# Photos and logs go in the real user's home folder, even when run with sudo
HOME = os.path.expanduser("~" + os.environ.get("SUDO_USER", ""))
PHOTO_DIR = os.path.join(HOME, "patrol_photos")
LOG_DIR = os.path.join(HOME, "patrol_logs")

ARUCO_DICT = cv2.aruco.DICT_4X4_50
MARKER_LABELS = {HOME_MARKER: "HOME", TURNAROUND_MARKER: "TURN AROUND"}


# ---------------------------------------------------------------------------
# MARKERS (works with old and new OpenCV)
# ---------------------------------------------------------------------------
class MarkerFinder:
    def __init__(self):
        d = cv2.aruco.getPredefinedDictionary(ARUCO_DICT)
        if hasattr(cv2.aruco, "ArucoDetector"):               # OpenCV 4.7+
            self.detector = cv2.aruco.ArucoDetector(d, cv2.aruco.DetectorParameters())
            self.old = None
        else:                                                 # OpenCV 4.6 and older
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
                found[int(i)] = float(max(pts[:, 0]) - min(pts[:, 0]))
        return found


def make_markers(out_dir="markers", size_px=800):
    os.makedirs(out_dir, exist_ok=True)
    d = cv2.aruco.getPredefinedDictionary(ARUCO_DICT)
    paths = []
    for marker_id, label in MARKER_LABELS.items():
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
    print("Print full-page. Place at the dog's eye level (~20-25 cm off the floor).")


# ---------------------------------------------------------------------------
# FACES (exact face boxes, used to aim the head and crop the close-up)
# ---------------------------------------------------------------------------
class FaceFinder:
    """OpenCV's built-in face detector. Looks for the detector file in the usual places."""

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


# ---------------------------------------------------------------------------
# LOGGING (same CSV format analyze_runs.py reads)
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
        print(f"[{name}] {data}")
        with open(self.path, "a", newline="") as f:
            csv.writer(f).writerow([f"{time.time():.3f}", self.run_id, name, json.dumps(data)])


class EmergencyStop(Exception):
    pass


# ---------------------------------------------------------------------------
# THE PATROL
# ---------------------------------------------------------------------------
class Patrol:
    def __init__(self):
        from pidog import Pidog
        from vilib import Vilib
        self.Vilib = Vilib
        self.dog = Pidog()
        self.markers = MarkerFinder()
        self.face_finder = FaceFinder()
        if self.face_finder.detector is None:
            print("Note: no face-detector file found - photos won't be aimed or cropped.")
        self.aim_sign = {"yaw": 1, "pitch": 1}   # learned automatically while aiming
        self.log = RunLog()
        self.last_photo = 0.0
        self.photo_count = 0
        os.makedirs(PHOTO_DIR, exist_ok=True)

        Vilib.camera_start(vflip=False, hflip=False)
        Vilib.display(local=False, web=True)   # live view at http://<pidog-ip>:9000/mjpg
        Vilib.face_detect_switch(True)
        time.sleep(1)

    # --- helpers ----------------------------------------------------------
    def check_estop(self):
        if self.head_patted():
            raise EmergencyStop()

    def act(self, name, steps=1, speed=WALK_SPEED):
        self.check_estop()
        self.dog.do_action(name, step_count=steps, speed=speed)
        self.dog.wait_all_done()

    def head(self, yaw, pitch=0):
        self.dog.head_move([[yaw, 0, pitch]], immediately=True, speed=90)
        try:
            self.dog.wait_head_done()
        except Exception:
            time.sleep(0.3)

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

    def head_patted(self):
        try:
            return self.dog.dual_touch.read() != "N"
        except Exception:
            return False

    def front_distance(self):
        try:
            d = self.dog.read_distance()
            return d if d and d > 0 else 999
        except Exception:
            return 999

    def steady_distance(self):
        """Median of a few readings - the sensor needs a moment after the head moves."""
        time.sleep(HEAD_SETTLE_S)
        readings = []
        for _ in range(3):
            readings.append(self.front_distance())
            time.sleep(0.05)
        return sorted(readings)[1]

    # --- smooth walking ---------------------------------------------------
    def leg_queue_len(self):
        """How much leg movement is still lined up. None = this library can't tell us."""
        try:
            return len(self.dog.legs_action_buffer)
        except AttributeError:
            pass
        try:
            return 0 if self.dog.is_legs_done() else 1
        except AttributeError:
            return None

    def keep_walking(self):
        """Top up the step queue without waiting, so the legs keep moving while we check sensors."""
        self.check_estop()
        before = self.leg_queue_len()
        if before is None:                      # old library: walk, then check (the slow way)
            self.act(WALK_GAIT, steps=STEPS_QUEUED)
            return
        if before <= self.refill_at:
            self.dog.do_action(WALK_GAIT, step_count=STEPS_QUEUED, speed=WALK_SPEED)
            added = (self.leg_queue_len() or 0) - before
            self.refill_at = max(self.refill_at, added // 2)   # refill when half used up

    def halt(self):
        """Stop the legs right away (drop any queued steps)."""
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

    def battery(self):
        try:
            return float(self.dog.get_battery_voltage())
        except Exception:
            pass
        try:
            from robot_hat.utils import get_battery_voltage
            return float(get_battery_voltage())
        except Exception:
            return None

    def faces(self):
        return int(self.Vilib.detect_obj_parameter.get("human_n", 0) or 0)

    # --- hallway centering ------------------------------------------------
    def measure_sides(self, walking=False):
        """Look left, look right, look forward again. Returns (left_cm, right_cm).
        With walking=True the legs keep going while the head looks around."""
        left_yaw = HEAD_SIDE_YAW if LEFT_IS_POSITIVE_YAW else -HEAD_SIDE_YAW
        if walking:
            self.keep_walking()
        self.head(left_yaw)
        left = self.steady_distance()
        if walking:
            self.keep_walking()
        self.head(-left_yaw)
        right = self.steady_distance()
        self.head(0)
        return left, right

    def stay_centered(self):
        left, right = self.measure_sides(walking=True)
        if left >= MAX_WALL_CM or right >= MAX_WALL_CM:
            self.log.event("center", left=left, right=right, action="skip_open_side")
            return
        diff = left - right   # positive = more room on the left = too close to the right wall
        if abs(diff) < CENTER_TOLERANCE_CM:
            self.log.event("center", left=left, right=right, action="ok")
            return
        direction = "turn_left" if diff > 0 else "turn_right"
        self.log.event("center", left=left, right=right, action=direction)
        # Line the correction up behind the current steps - no stop
        self.dog.do_action(direction, step_count=CORRECTION_STEPS, speed=WALK_SPEED)

    # --- behaviors --------------------------------------------------------
    def aim_at_face(self):
        """Tilt up, then nudge the head until the biggest face is near the middle of the picture.
        Returns (face_box, frame) from the final look, or (None, frame) if no face was found.
        Which way is 'up' and 'left' for the head is learned on the fly: if a nudge makes the
        face farther from the middle, that direction gets flipped."""
        # Start where the dog saw the face (head level). If it's not there now, tilt up and look.
        yaw, pitch = 0.0, 0.0
        self.head(yaw, pitch)
        time.sleep(0.2)
        frame = self.Vilib.img
        box = self.face_finder.biggest(frame)
        if box is None and PHOTO_START_PITCH:
            pitch = float(PHOTO_START_PITCH)
            self.head(yaw, pitch)
            time.sleep(0.3)
            frame = self.Vilib.img
            box = self.face_finder.biggest(frame)
        for _ in range(AIM_TRIES):
            if box is None or frame is None:
                break
            H, W = frame.shape[:2]
            ex = (box[0] + box[2] / 2) - W / 2          # + = face is right of center
            ey = (box[1] + box[3] / 2) - H / 2          # + = face is below center
            if abs(ex) <= AIM_GOOD_PX and abs(ey) <= AIM_GOOD_PX:
                break
            # Move ONE direction at a time (whichever is farther off), so a wrong guess about
            # which way the head turns is caught and flipped for just that direction.
            # About 0.08 degrees per pixel; each nudge is capped at 15 degrees.
            axis = "yaw" if abs(ex) >= abs(ey) else "pitch"
            err = ex if axis == "yaw" else ey
            step = max(-15, min(15, self.aim_sign[axis] * 0.08 * err))
            if axis == "yaw":
                new_yaw, new_pitch = max(-HEAD_YAW_LIMIT, min(HEAD_YAW_LIMIT, yaw - step)), pitch
            else:
                new_yaw, new_pitch = yaw, max(-HEAD_PITCH_LIMIT, min(HEAD_PITCH_LIMIT, pitch - step))
            self.head(new_yaw, new_pitch)
            time.sleep(0.25)
            new_frame = self.Vilib.img
            new_box = self.face_finder.biggest(new_frame)
            if new_box is None:
                # Lost the face: that direction was backwards. Flip it, go back, try again.
                self.aim_sign[axis] *= -1
                self.head(yaw, pitch)
                time.sleep(0.25)
                frame = self.Vilib.img
                box = self.face_finder.biggest(frame)
                continue
            new_err = ((new_box[0] + new_box[2] / 2) - W / 2) if axis == "yaw" \
                else ((new_box[1] + new_box[3] / 2) - H / 2)
            if abs(new_err) > abs(err) + 10:
                self.aim_sign[axis] *= -1                # got farther off: flip that direction
            yaw, pitch, frame, box = new_yaw, new_pitch, new_frame, new_box
        return box, frame

    def take_picture(self):
        """Aim at the face, then save the full photo and a close-up of the face."""
        t0 = time.time()
        self.lights("boom", "white", bps=3)    # flash = "picture being taken"
        self.sound("single_bark_1")
        box, frame = self.aim_at_face()
        name = datetime.now().strftime("person_%Y%m%d_%H%M%S")
        self.Vilib.take_photo(photo_name=name, path=PHOTO_DIR)
        closeup = None
        if box is not None and frame is not None:
            closeup = os.path.join(PHOTO_DIR, name + "_face.jpg")
            cv2.imwrite(closeup, crop_face(frame, box))
        self.head(0, 0)
        return {"file": os.path.join(PHOTO_DIR, name + ".jpg"), "closeup": closeup,
                "face_found": box is not None, "seconds": round(time.time() - t0, 2)}

    def maybe_photo(self):
        """If a face is in view (and cooldown is over), stop and take a photo."""
        if time.time() - self.last_photo < PHOTO_COOLDOWN_S or self.faces() < 1:
            return
        self.halt()
        self.act("stand", speed=100)
        info = self.take_picture()
        self.photo_count += 1
        self.last_photo = time.time()
        self.log.event("photo", **info)
        self.act("wag_tail", steps=3, speed=90)
        self.lights("breath", "cyan")

    def marker_close(self, marker_id):
        width = self.markers.find(self.Vilib.img).get(marker_id, 0.0)
        return width >= MARKER_TRIGGER_PX, width

    def turn_around(self):
        t0 = time.time()
        self.halt()
        self.act("stand", speed=100)
        self.act("turn_left", steps=TURN_STEPS_180, speed=WALK_SPEED)
        self.log.event("turn_180", seconds=round(time.time() - t0, 2))

    def celebrate(self):
        self.lights("boom", "green", bps=2)
        self.sound("woohoo")
        self.act("wag_tail", steps=5, speed=100)
        self.act("sit", speed=60)

    # --- main loop --------------------------------------------------------
    def run(self):
        start = time.time()
        targets = [(TURNAROUND_MARKER, "far_end"), (HOME_MARKER, "home")]
        leg, result = 0, "unknown"
        self.refill_at = 0
        next_center = time.time() + 1.0
        next_battery = 0.0
        settings = {k: v for k, v in globals().items() if k.isupper() and isinstance(v, (int, float, bool))}
        self.log.event("run_start", params=settings, battery=self.battery())

        try:
            self.lights("breath", "cyan")
            self.act("stand", speed=80)
            self.head(0)
            print("Patrol starting. Pat my head to stop.")

            while True:
                self.check_estop()
                if time.time() - start > MAX_RUN_MINUTES * 60:
                    result = "timeout"
                    break
                if time.time() >= next_battery:          # battery changes slowly: every 10 s
                    next_battery = time.time() + 10
                    volts = self.battery()
                    if LOW_BATTERY_V and volts is not None and 0 < volts < LOW_BATTERY_V:
                        self.log.event("low_battery", volts=volts)
                        self.lights("breath", "red")
                        result = "low_battery"
                        break

                # Markers first: the far wall reads as an "obstacle" when we get close
                marker_id, label = targets[leg]
                close, width = self.marker_close(marker_id)
                if close:
                    self.log.event("marker", id=marker_id, label=label, width_px=width,
                                   elapsed=round(time.time() - start, 1))
                    self.turn_around()
                    next_center = time.time()          # re-center right after turning
                    leg += 1
                    if leg == len(targets):
                        result = "success"
                        self.celebrate()
                        break
                    continue

                if self.front_distance() < STOP_DISTANCE_CM:
                    self.log.event("obstacle_stop", distance=self.front_distance())
                    self.halt()
                    self.act("stand", speed=100)
                    self.lights("breath", "yellow", bps=2)
                    self.maybe_photo()
                    time.sleep(1)
                    continue

                self.maybe_photo()

                if time.time() >= next_center:
                    self.stay_centered()
                    next_center = time.time() + CENTER_EVERY_S

                self.keep_walking()
                time.sleep(0.02)

        except EmergencyStop:
            result = "emergency_stop"
            print("[stop] head pat - stopping.")
        except KeyboardInterrupt:
            result = "keyboard_stop"
            print("Stopped by keyboard.")

        if result != "success":
            try:
                self.dog.do_action("sit", speed=60)
                self.dog.wait_all_done()
            except Exception:
                pass
        self.log.event("run_end", result=result, seconds=round(time.time() - start, 1),
                       photos=self.photo_count)
        print(f"Run {self.log.run_id}: {result}. Photos: {self.photo_count} in {PHOTO_DIR}. "
              f"Log: {self.log.path}")

    # --- test modes -------------------------------------------------------
    def test_sensors(self, seconds=20):
        end = time.time() + seconds
        while time.time() < end:
            print(f"distance={self.front_distance():.0f} cm  faces={self.faces()}  "
                  f"markers={self.markers.find(self.Vilib.img)}  battery={self.battery()}  "
                  f"touch={'yes' if self.head_patted() else 'no'}")
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


if __name__ == "__main__":
    if "--make-markers" in sys.argv:
        make_markers()
        sys.exit(0)

    patrol = Patrol()
    try:
        if "--test-center" in sys.argv:
            patrol.act("stand", speed=80)
            for _ in range(5):
                l, r = patrol.measure_sides()
                print(f"left={l:.0f} cm   right={r:.0f} cm")
                time.sleep(1)
        elif "--test-turn" in sys.argv:
            patrol.act("stand", speed=80)
            patrol.turn_around()
        elif "--test-sensors" in sys.argv:
            patrol.test_sensors()
        elif "--test-photo" in sys.argv:
            # Stand still, aim at the nearest face, and save both photos. Stand in front of it!
            patrol.act("stand", speed=100)
            print(patrol.take_picture())
        elif "--test-walk" in sys.argv:
            # Walk straight for 6 seconds the smooth way (no sensors, no stops). Hold onto it!
            patrol.refill_at = 0
            patrol.act("stand", speed=100)
            end = time.time() + 6
            while time.time() < end:
                patrol.keep_walking()
                time.sleep(0.02)
            patrol.halt()
            patrol.act("stand", speed=100)
        else:
            patrol.run()
    except (KeyboardInterrupt, EmergencyStop):
        print("Stopped.")
    finally:
        patrol.shutdown()
