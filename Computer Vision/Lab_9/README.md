# Lab 9 — AI Agents with Computer Vision (Perception-Reasoning-Action Loop)

> **Course:** Applied AI — Computer Vision (ITAI 1378)
> **Module:** 09 (Final Lab)
> **Type:** Lab / Hands-on Exercise + Reflection
> **Student:** Rich Fox
> **File:** `Lab09_RichFox_ITAI_1378.ipynb`

---

## Overview

In this culminating lab, we synthesized everything from Labs 1–8 into **AI agents** — systems that perceive their environment, reason about it, and take action. We implemented the foundational **Perception-Reasoning-Action (PRA) loop** using YOLO object detection on video streams. The lab required implementing a base agent (person detection), then extending it with a custom object (bird detection). Reflection questions pushed critical thinking about real-world challenges, complex reasoning, and practical applications.

---

## What I Learned

- **AI agents are fundamentally cyclical.** The PRA loop (Perception → Reasoning → Action) repeats continuously. Each cycle refines understanding and guides behavior. This is the core abstraction behind autonomous systems, from simple object monitors to self-driving cars.

- **Perception ≠ understanding.** YOLO detects "what's in the frame," but the agent must reason about what it means. Detection alone is perception; reasoning adds judgment (e.g., "person in restricted area at night = security threat").

- **Real-world perception is noisy.** YOLO struggles with odd viewpoints, lighting changes, distance, and occlusion. The notebook's bird detection example showed high miss rates at distance or unusual angles — a sobering reality check that lab accuracy doesn't transfer directly to deployment.

- **Reasoning scales from trivial to complex.** The base agent used if-then logic ("if person, then alert"). Real systems need nuance: location (which zone?), time (is this hour authorized?), context (is it a costume vs. real threat?), and confidence thresholds.

- **Actions are the agents' interface with the world.** Printing alerts, drawing bounding boxes, or sending security notifications are all "actions." The same perception-reasoning can trigger different actions in different contexts — flexibility is the strength.

---

## Challenges Faced

The main challenge was **bridging the lab-to-real-world gap**. In controlled lab settings, YOLO performs well. In actual video (ocean video for bird detection), the model missed many birds due to:
- **Distance:** Small objects are hard to distinguish
- **Unusual poses:** Birds at odd angles weren't recognized consistently
- **Lighting:** Changes in sun position, reflections on water
- **Speed:** Fast-moving objects may not be detected in every frame

This tension — between lab accuracy metrics and deployment reality — is the central challenge of AI in production. It motivates defensive engineering: frame skipping to save compute, confidence thresholds to reduce false positives, and human review for high-stakes decisions.

---

## The Perception-Reasoning-Action Loop

### Part 1: Perception

The agent uses YOLO to detect objects in every frame (or every Nth frame for efficiency):

```python
results = model(frame)  # YOLO inference
```

**Output:** Bounding boxes, class IDs, confidence scores.

**Limitation:** Detection is noisy — background objects, partially visible items, and unusual angles all confuse the model.

---

### Part 2: Reasoning

The agent examines detections and applies a decision rule:

```python
for result in results:
    for box in result.boxes:
        class_id = int(box.cls[0])
        if class_id == 0:  # Person class ID
            person_detected = True
```

**Base logic:** If person (class_id=0) is detected, set flag.

**More complex reasoning examples:**
- **Spatial:** Only alert if person is in zone 1 (screen region)
- **Temporal:** Only alert during restricted hours
- **Contextual:** Alert if person + no badge (requires additional detection)
- **Confidence-based:** Only alert if confidence > 0.7

---

### Part 3: Action

When reasoning triggers, the agent acts:

```python
if person_detected:
    print(f'Frame {frame_count}: Person detected!')
    # Optionally display annotated frame
```

**Actions in the base agent:**
- Print alert message
- Display annotated frame with bounding box

**Real-world actions might include:**
- Send notification to security
- Log event with timestamp
- Trigger alarm
- Take video clip for later review
- Unlock/lock doors
- Stop operations

---

## Student Challenge: Bird Detection

**Task:** Detect a different object (birds) in an ocean video.

**COCO Class ID for birds:** 14

**Implementation:** Modified the base agent to detect class_id=14 instead of 0.

**Results:** Bird detection worked but with limitations. Many birds at distance or moving quickly were missed — illustrating real-world detection challenges.

---

## Reflective Insights

### Perception-Reasoning-Action Implementation (Q1)

**Perception:** YOLO model analyzes frames every 10 seconds, extracting object locations and classes.

**Reasoning:** Check if target class exists in detections. For person detection: class_id == 0. For bird detection: class_id == 14.

**Action:** Print alert and display annotated frame when target is found.

---

### Complex Reasoning Rules (Q2)

Beyond simple "if person, then alert," real systems need:

- **Spatial reasoning:** "Alert only if person is in restricted zone 1 (top-left quadrant)"
- **Multi-object reasoning:** "Alert if person AND horse detected" → send hay
- **Confidence reasoning:** "Alert only if confidence > 0.75"
- **Temporal reasoning:** "Alert if person detected during off-hours (22:00-06:00)"
- **Context reasoning:** "Alert if person + unrecognized badge"

---

### Real-World Challenges (Q3)

Actual deployment faces:

1. **Lighting variation:** YOLO trained mostly on daytime/normal lighting
2. **Distance:** Small objects (birds far away) are missed
3. **Occlusion:** Objects hidden behind obstacles
4. **Unusual poses:** Birds upside-down, people lying down
5. **Speed:** Fast motion causes blur; detection misses frames
6. **Background clutter:** Crowded scenes confuse the model
7. **Weather:** Rain, fog, snow degrade performance
8. **Computational load:** Real-time processing on high-res video is expensive

---

### Real-World Application: Self-Driving Car

**Perception:** YOLO (or Faster R-CNN) detects pedestrians, vehicles, road signs, traffic lights.

**Reasoning:** 
- If pedestrian in path → stop
- If red light → stop
- If pedestrian on sidewalk → continue (safe)
- If car in adjacent lane + turn signal → avoid merge

**Action:**
- Stop (brake)
- Accelerate
- Turn (steering)
- Honk (alert)

---

## YOLO and Real-Time Detection

**YOLO (You Only Look Once):**
- Single-stage detector — predicts bounding boxes and classes in one pass
- Fast enough for video (30 FPS on modern hardware)
- Trades some accuracy for speed compared to two-stage detectors

**In the lab:**
- `yolov8n.pt` (nano) — very fast, ~5-10 ms/frame
- `yolov8m.pt` (medium) — balanced, ~20-30 ms/frame

**COCO Classes (80 total):** Person (0), car (2), dog (16), cat (17), bird (14), etc.

---

## Agent Architecture Decisions

| Decision | Rationale |
|---|---|
| Frame skipping (every 10th) | Reduce compute; still catch most events |
| Confidence threshold | Filter low-confidence detections; reduce false positives |
| Multiple classes | Detect people AND cars → richer reasoning |
| Video source | Real-world data reveals detection gaps |
| Human review | For high-stakes decisions (security, safety) |

---

## Scaling the Agent

### Small-scale (Single Video)
- Load model once
- Loop through frames
- Print alerts

### Medium-scale (Multiple Video Streams)
- Load model once (on GPU)
- Parallelize frame processing
- Queue alerts for review

### Large-scale (Real-time Monitoring)
- Distributed inference (multiple GPUs)
- Frame batching
- Database for event logging
- Feedback loop: humans label missed detections → retrain

---

## Ethical Considerations

Surveillance agents raise critical concerns:

1. **Privacy:** Continuous video recording of public spaces
2. **Consent:** Do people know they're being monitored?
3. **Bias:** YOLO trained on biased datasets; may misidentify or miss certain groups
4. **Accuracy:** False alarms cause unnecessary investigation; false negatives cause missed threats
5. **Accountability:** Who's responsible if the agent makes a mistake?
6. **Mission creep:** Systems built for one purpose (crowd safety) repurposed for tracking

**Responsible deployment requires:**
- Clear privacy policies
- Transparent use of AI
- Regular audits for bias
- Human-in-the-loop for high-stakes decisions
- Legal and ethical review

---

## Technologies Used

| Library | Purpose |
|---|---|
| **Ultralytics YOLO** | Pre-trained object detection |
| **OpenCV** | Video reading, frame manipulation |
| **Matplotlib** | Visualization of detections |
| **Requests** | Downloading video files |
| **NumPy/PIL** | Image processing |

---

## How to Run

```bash
cd "Computer Vision/Labs/Lab9"
jupyter notebook Lab09_RichFox_ITAI_1378.ipynb
```

1. Run setup cells to install libraries
2. Run base agent (person detection) to see PRA loop in action
3. Implement student challenge (bird detection or custom object)
4. Answer reflection questions
5. Submit notebook

### Dependencies

```bash
pip install ultralytics opencv-python requests matplotlib pillow numpy
```

---

## Summary of the Full Course

**Lab 1:** Image processing fundamentals  
**Lab 2:** Classical image features (HOG, LBP)  
**Lab 3:** Classical ML vs. Deep Learning trade-offs  
**Lab 4–5:** CNNs and transfer learning  
**Lab 6:** Object detection (SSD MobileNet, IoU metrics)  
**Lab 7:** Visual Language Models (CLIP, BLIP) — understanding images + text  
**Lab 8:** VLM applications, ethics, deployment  
**Lab 9:** Synthesizing everything into agents — the next frontier  

**The trajectory:** From low-level pixel manipulation → feature engineering → deep learning → multimodal reasoning → **autonomous agents that perceive, reason, and act.**

---

## Key Takeaway

Lab 9 is the capstone: you've moved from analyzing individual images to building systems that continuously perceive and respond. An AI agent is not just a model — it's a closed-loop system. This loop is the foundation of all autonomous systems, from simple security monitors to self-driving cars to robots.

The challenges you encountered (YOLO missing distant birds, lighting affecting detection) are **real**. They motivate the current frontier of AI: making perception robust enough, reasoning sophisticated enough, and actions responsible enough to work in the real world.

Your responsibility as an AI practitioner: ensure that when you close this loop, it serves human wellbeing, respects privacy, acknowledges limitations, and maintains human oversight over high-stakes decisions.

---

*[← Back to Computer Vision](../../README.md) | [← Back to Portfolio Home](../../../README.md)*
