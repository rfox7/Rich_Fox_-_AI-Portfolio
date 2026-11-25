#!/usr/bin/env python3
"""
Make the two printable ArUco markers that pidog_patrol.py looks for.

    python3 make_markers.py        # writes markers/marker_0.png, markers/marker_1.png and pidog_markers.pdf

Uses the same marker set as pidog_patrol.py (ARUCO_DICT = 4, the 5x5 set).
If you change ARUCO_DICT there, change it here too and print new markers.
Needs opencv-contrib-python (and Pillow for the PDF).
"""

import os

import cv2

ARUCO_DICT = 4          # cv2.aruco.DICT_5X5_50, same as pidog_patrol.py
MARKERS = {0: "HOME", 1: "TURN AROUND"}


def main(out_dir="markers", size_px=800):
    os.makedirs(out_dir, exist_ok=True)
    d = cv2.aruco.getPredefinedDictionary(ARUCO_DICT)
    paths = []
    for marker_id, label in MARKERS.items():
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
        print("Install Pillow to also get a PDF")
    print("Print full-page on plain paper. Place about 20-25 cm off the floor, facing down the hallway.")


if __name__ == "__main__":
    main()
