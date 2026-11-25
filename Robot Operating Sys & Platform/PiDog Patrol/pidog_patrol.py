#!/usr/bin/env python3
import os
import sys
import json
import time
import datetime
import cv2
import numpy as np
from pidog import Pidog
from vilib import Vilib

# --- Patrol Configuration Parameters ---
TURNAROUND_MARKER = 1
HOME_MARKER = 0
WALK_SPEED = 100
STEPS_QUEUED = 2
TURN_STEPS_180 = 8
STOP_DISTANCE_CM = 48
MARKER_TRIGGER_PX = 18
PHOTO_COOLDOWN_S = 15
PHOTO_START_PITCH = 20
AIM_TRIES = 10
AIM_GOOD_PX = 40
HEAD_YAW_LIMIT = 60
HEAD_PITCH_LIMIT = 35
FACE_CROP_MARGIN = 0.6
MAX_RUN_MINUTES = 45
LOW_BATTERY_V = 6.6
CENTER_EVERY_S = 5.0
HEAD_SETTLE_S = 0.1
HEAD_SIDE_YAW = 75
LEFT_IS_POSITIVE_YAW = True
CENTER_TOLERANCE_CM = 15
MAX_WALL_CM = 250
CORRECTION_STEPS = 1
ARUCO_DICT = 4  # cv2.aruco.DICT_5X5_50

LOG_DIR = "/home/user05/patrol_logs"
PHOTO_DIR = os.path.join(LOG_DIR, "patrol_photos")
os.makedirs(PHOTO_DIR, exist_ok=True)


class EmergencyStop(Exception):
    pass


class PatrolLogger:
    def __init__(self):
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        self.path = os.path.join(LOG_DIR, f"patrol_{ts}.jsonl")

    def event(self, name, **data):
        print(f"[{name}] {data}", flush=True)
        record = {"t": round(time.time(), 2), "event": name, **data}
        try:
            with open(self.path, "a") as f:
                f.write(json.dumps(record) + "\n")
        except Exception:
            pass


class HallwayPatrol:
    def __init__(self):
        self.log = PatrolLogger()
        self.dog = Pidog()
        time.sleep(0.5)

        Vilib.camera_start(vflip=False, hflip=False)
        Vilib.display(local=False, web=True)
        Vilib.human_detect_switch(True)
        Vilib.face_detect_switch(True)
        time.sleep(1.5)

        self.aruco_dict = cv2.aruco.getPredefinedDictionary(ARUCO_DICT)
        self.aruco_params = cv2.aruco.DetectorParameters()
        self.detector = cv2.aruco.ArucoDetector(self.aruco_dict, self.aruco_params)

        self.start_t = time.time()
        self.last_photo_t = 0.0
        self.last_progress_t = time.time()
        self.last_progress_d = 999.0

    def check_safety(self):
        if self.dog.dual_touch.read() != "N":
            raise EmergencyStop()
        if (time.time() - self.start_t) > MAX_RUN_MINUTES * 60:
            raise EmergencyStop()

    def act(self, action, step_count=1, speed=WALK_SPEED):
        self.check_safety()
        self.dog.do_action(action, step_count=step_count, speed=speed)
        self.dog.wait_all_done()

    def look_at(self, yaw=0, roll=0, pitch=0, speed=80):
        self.dog.head_move([[yaw, roll, pitch]], immediately=True, speed=speed)
        self.dog.wait_head_done()
        time.sleep(HEAD_SETTLE_S)

    def front_distance(self):
        try:
            d = float(self.dog.ultrasonic.read())
            return round(d, 2) if d > 0 else 999
        except Exception:
            return 999

    def scan_sides(self):
        left_yaw = HEAD_SIDE_YAW if LEFT_IS_POSITIVE_YAW else -HEAD_SIDE_YAW
        right_yaw = -left_yaw

        self.look_at(yaw=left_yaw, pitch=0)
        left_cm = self.front_distance()

        self.look_at(yaw=right_yaw, pitch=0)
        right_cm = self.front_distance()

        self.look_at(yaw=0, pitch=0)
        return left_cm, right_cm

    def stay_centered(self):
        left_cm, right_cm = self.scan_sides()
        if left_cm > MAX_WALL_CM or right_cm > MAX_WALL_CM:
            self.log.event("center", left=left_cm, right=right_cm, action="skip_open_side")
            return

        diff = left_cm - right_cm
        if abs(diff) <= CENTER_TOLERANCE_CM:
            self.log.event("center", left=left_cm, right=right_cm, action="ok")
        elif diff > CENTER_TOLERANCE_CM:
            self.log.event("center", left=left_cm, right=right_cm, action="turn_left")
            self.act("turn_left", step_count=CORRECTION_STEPS)
        else:
            self.log.event("center", left=left_cm, right=right_cm, action="turn_right")
            self.act("turn_right", step_count=CORRECTION_STEPS)

    def detect_markers(self):
        frame = getattr(Vilib, "img", None)
        if frame is None:
            return {}
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        corners, ids, _ = self.detector.detectMarkers(gray)
        found = {}
        if ids is not None:
            for c, mid in zip(corners, ids.flatten()):
                pts = c[0]
                width_px = float(np.linalg.norm(pts[0] - pts[1]))
                found[int(mid)] = round(width_px, 1)
        return found

    def maybe_photo(self):
        if time.time() - self.last_photo_t < PHOTO_COOLDOWN_S:
            return
        human_n = Vilib.detect_obj_parameter.get("human_n", 0)
        if human_n <= 0:
            return

        t0 = time.time()
        self.dog.body_stop()
        yaw, pitch = 0, PHOTO_START_PITCH
        self.look_at(yaw=yaw, pitch=pitch)

        face_found = False
        for _ in range(AIM_TRIES):
            if Vilib.detect_obj_parameter.get("face_n", 0) > 0:
                face_found = True
                fx = Vilib.detect_obj_parameter.get("face_x", 320)
                fy = Vilib.detect_obj_parameter.get("face_y", 240)
                err_x = fx - 320
                err_y = fy - 240
                if abs(err_x) <= AIM_GOOD_PX and abs(err_y) <= AIM_GOOD_PX:
                    break
                yaw = max(-HEAD_YAW_LIMIT, min(HEAD_YAW_LIMIT, yaw - int(err_x * 0.05)))
                pitch = max(-HEAD_PITCH_LIMIT, min(HEAD_PITCH_LIMIT, pitch - int(err_y * 0.05)))
                self.look_at(yaw=yaw, pitch=pitch)
            time.sleep(0.05)

        frame = getattr(Vilib, "img", None)
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = os.path.join(PHOTO_DIR, f"person_{ts}.jpg")
        closeup_path = None

        if frame is not None and frame.size > 0:
            cv2.imwrite(filepath, frame)
            if face_found:
                fx = int(Vilib.detect_obj_parameter.get("face_x", 320))
                fy = int(Vilib.detect_obj_parameter.get("face_y", 240))
                fw = int(Vilib.detect_obj_parameter.get("face_w", 100))
                fh = int(Vilib.detect_obj_parameter.get("face_h", 100))
                pad_x = int(fw * FACE_CROP_MARGIN)
                pad_y = int(fh * FACE_CROP_MARGIN)
                h, w = frame.shape[:2]
                x1, y1 = max(0, fx - fw // 2 - pad_x), max(0, fy - fh // 2 - pad_y)
                x2, y2 = min(w, fx + fw // 2 + pad_x), min(h, fy + fh // 2 + pad_y)
                if x2 > x1 and y2 > y1:
                    closeup_path = os.path.join(PHOTO_DIR, f"closeup_{ts}.jpg")
                    cv2.imwrite(closeup_path, frame[y1:y2, x1:x2])

        self.last_photo_t = time.time()
        self.look_at(yaw=0, pitch=0)
        self.log.event(
            "photo",
            file=filepath,
            closeup=closeup_path,
            face_found=face_found,
            seconds=round(time.time() - t0, 2)
        )

    def keep_walking(self):
        self.act("forward", step_count=STEPS_QUEUED, speed=WALK_SPEED)

    def run(self):
        params = {
            "TURNAROUND_MARKER": TURNAROUND_MARKER,
            "HOME_MARKER": HOME_MARKER,
            "WALK_SPEED": WALK_SPEED,
            "STEPS_QUEUED": STEPS_QUEUED,
            "TURN_STEPS_180": TURN_STEPS_180,
            "STOP_DISTANCE_CM": STOP_DISTANCE_CM,
            "MARKER_TRIGGER_PX": MARKER_TRIGGER_PX,
            "PHOTO_COOLDOWN_S": PHOTO_COOLDOWN_S,
            "PHOTO_START_PITCH": PHOTO_START_PITCH,
            "AIM_TRIES": AIM_TRIES,
            "AIM_GOOD_PX": AIM_GOOD_PX,
            "HEAD_YAW_LIMIT": HEAD_YAW_LIMIT,
            "HEAD_PITCH_LIMIT": HEAD_PITCH_LIMIT,
            "FACE_CROP_MARGIN": FACE_CROP_MARGIN,
            "MAX_RUN_MINUTES": MAX_RUN_MINUTES,
            "LOW_BATTERY_V": LOW_BATTERY_V,
            "CENTER_EVERY_S": CENTER_EVERY_S,
            "HEAD_SETTLE_S": HEAD_SETTLE_S,
            "HEAD_SIDE_YAW": HEAD_SIDE_YAW,
            "LEFT_IS_POSITIVE_YAW": LEFT_IS_POSITIVE_YAW,
            "CENTER_TOLERANCE_CM": CENTER_TOLERANCE_CM,
            "MAX_WALL_CM": MAX_WALL_CM,
            "CORRECTION_STEPS": CORRECTION_STEPS,
            "ARUCO_DICT": ARUCO_DICT,
        }
        try:
            batt = round(float(self.dog.get_battery_voltage()), 2)
        except Exception:
            batt = 0.0

        self.log.event("run_start", params=params, battery=batt)
        self.act("stand", speed=80)
        self.look_at(0, 0, 0)
        print("Patrol starting. Pat my head to stop.", flush=True)

        leg = "outbound"  # outbound -> far_end (Marker 1) -> home (Marker 0)
        next_center = time.time() + 1.0
        result = "running"

        try:
            while True:
                self.check_safety()

                # 1. Check ArUco target markers
                markers = self.detect_markers()
                if markers:
                    self.log.event("marker_seen", **markers)

                target_id = TURNAROUND_MARKER if leg == "outbound" else HOME_MARKER
                target_label = "far_end" if leg == "outbound" else "home"

                if target_id in markers and markers[target_id] >= MARKER_TRIGGER_PX:
                    elapsed = round(time.time() - self.start_t, 1)
                    self.log.event(
                        "marker",
                        id=target_id,
                        label=target_label,
                        width_px=markers[target_id],
                        elapsed=elapsed
                    )
                    # Approach marker up to ~22 cm
                    while self.front_distance() > 24.0:
                        self.act("forward", step_count=1, speed=WALK_SPEED)

                    if leg == "outbound":
                        print(f"[far_end_arrived] distance={self.front_distance()} cm", flush=True)
                        t_turn = time.time()
                        self.act("turn_right", step_count=TURN_STEPS_180, speed=WALK_SPEED)
                        self.log.event("turn_180", seconds=round(time.time() - t_turn, 2))
                        leg = "inbound"
                        next_center = time.time() + 1.5
                        continue
                    else:
                        t_turn = time.time()
                        self.act("turn_right", step_count=TURN_STEPS_180, speed=WALK_SPEED)
                        self.log.event("turn_180", seconds=round(time.time() - t_turn, 2))
                        result = "success"
                        break

                # 2. Ultrasonic obstacle check & softened bypass
                front_cm = self.front_distance()
                if front_cm <= STOP_DISTANCE_CM:
                    self.dog.body_stop()
                    self.log.event("obstacle_stop", distance=front_cm)
                    left_cm, right_cm = self.scan_sides()
                    evade_dir = "turn_right" if right_cm >= left_cm else "turn_left"
                    undo_dir = "turn_left" if evade_dir == "turn_right" else "turn_right"
                    turn_steps = 3

                    def _safe_forward(max_steps):
                        taken = 0
                        for _ in range(max_steps):
                            if self.front_distance() <= STOP_DISTANCE_CM:
                                break
                            self.act("forward", speed=WALK_SPEED)
                            taken += 1
                        return taken

                    # 1. Turn out toward open side & 2. Sidestep laterally
                    for _ in range(turn_steps):
                        self.act(evade_dir, speed=WALK_SPEED)
                    lat_out = _safe_forward(3)

                    # 3. Counter-rotate parallel to corridor & 4. Walk 7 steps past obstacle
                    for _ in range(turn_steps):
                        self.act(undo_dir, speed=WALK_SPEED)
                    pass_steps = _safe_forward(7)

                    # 5. Gently angle back toward centerline (half-turn) without over-rotating
                    return_steps = max(1, turn_steps // 2)
                    for _ in range(return_steps):
                        self.act(undo_dir, speed=WALK_SPEED)
                    lat_in = _safe_forward(max(1, lat_out - 1))

                    # 6. Counter-rotate back onto original hallway heading
                    for _ in range(return_steps):
                        self.act(evade_dir, speed=WALK_SPEED)

                    clear_ahead = self.front_distance()
                    self.log.event(
                        "obstacle_reroute",
                        left=left_cm,
                        right=right_cm,
                        action=evade_dir,
                        lat_out=lat_out,
                        pass_steps=pass_steps,
                        lat_in=lat_in,
                        clear_ahead=clear_ahead
                    )
                    self.last_progress_t = time.time()
                    self.last_progress_d = self.front_distance()
                    next_center = time.time() + 1.0
                    continue

                # 3. Person / face photo check
                self.maybe_photo()

                # 4. Periodic hallway wall centering
                if time.time() >= next_center:
                    self.stay_centered()
                    next_center = time.time() + CENTER_EVERY_S

                self.keep_walking()
                time.sleep(0.02)

        except EmergencyStop:
            result = "emergency_stop"
            print("[stop] head pat - stopping.", flush=True)
        except KeyboardInterrupt:
            result = "keyboard_stop"
            print("Stopped by keyboard.", flush=True)

        if result != "success":
            try:
                self.dog.body_stop()
            except Exception:
                pass

        try:
            self.dog.do_action("sit", speed=80)
            self.dog.wait_all_done()
            self.dog.close()
        except Exception:
            pass

        # Release lgpio chip so parent/subsequent scripts do not hit GPIO busy
        try:
            import lgpio
            from robot_hat.pin import Pin
            if getattr(Pin, "_chip", None) is not None:
                lgpio.gpiochip_close(Pin._chip)
                Pin._chip = None
        except Exception:
            pass


if __name__ == "__main__":
    patrol = HallwayPatrol()
    patrol.run()