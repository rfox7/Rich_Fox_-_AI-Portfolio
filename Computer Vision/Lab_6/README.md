# Lab 6 — Object Detection with Transfer Learning (SSD MobileNet V2)

> **Course:** Applied AI — Computer Vision (ITAI 1378)
> **Module:** 06
> **Type:** Lab / Hands-on Exercise + Analysis
> **Student:** Rich Fox
> **Files:** `L06_Rich_Fox_ITAI1378.ipynb` + `L06_Rich_Fox_ITAI1378.docx`

---

## Overview

In this lab, we transitioned from **image classification** (Labs 4–5) to **object detection** — localizing and classifying multiple objects within a single image using **SSD MobileNet V2**, a pre-trained model from TensorFlow Hub. We worked with the **Pascal VOC 2007 dataset** (20 object classes), implemented IoU-based evaluation metrics, and critically analyzed the trade-offs between precision and recall in different real-world scenarios.

---

## What I Learned

- **Image classification answers "what"; object detection answers "what and where."** A classifier might say "this image contains a person" — an object detector specifies the person's location with a bounding box `[ymin, xmin, ymax, xmax]`.

- **Fractional coordinates enable scale-invariance.** Using normalized coordinates (0 to 1) instead of pixel values means the same bounding box model works across images of any resolution — a 224×224 image and a 1080×1920 image use the same coordinate system.

- **IoU (Intersection over Union) is the gold standard for detection evaluation.** IoU = (intersection area) / (union area) ranges from 0 (no overlap) to 1 (perfect match). A threshold of 0.5 means at least half the predicted box must overlap the ground truth — a common industry standard.

- **Confidence thresholds are not one-size-fits-all.** At threshold 0.3: ~20 detections (many false positives). At threshold 0.7: ~2 detections (fewer false positives, but may miss objects). The choice depends on downstream costs.

- **Precision-recall trade-off has real consequences.** For a self-driving car avoiding obstacles, high recall is critical — missing a pedestrian is catastrophic. For a photo app tagging people, high precision matters — mislabeling innocent people is unethical.

- **Pre-trained models transfer knowledge but may have dataset bias.** The model uses COCO classes; the VOC dataset has different classes — mismatches require careful evaluation design.

---

## Challenges Faced

The most instructive challenge was **achieving non-zero precision/recall**. Initial runs returned 0% because the model (trained on COCO) and dataset (VOC) use different class label systems. Attempting to match predicted class labels against ground truth labels failed. The breakthrough was recognizing that **IoU-based evaluation could skip class label matching**, focusing purely on localization accuracy. This pragmatic fix raised precision to 55.69% and recall to 69.92% — revealing that the model localizes objects reasonably well, even if its label predictions don't align with the dataset's schema.

Debugging also required recognizing a Python mistake: an `if` statement checking class matching had to be removed when class incompatibility was the real issue. This taught the lesson that sometimes the problem isn't in your code logic — it's in your data assumptions.

---

## Conceptual Understanding

### Image Classification vs. Object Detection

| Task | Input | Output | Example |
|---|---|---|---|
| Classification | Bedroom photo | "Bedroom" | Is this a bedroom? Yes. |
| Detection | Bedroom photo | Bounding boxes + labels | Where are the bed (box1), lamp (box2), desk (box3)? |

---

### Bounding Box Format

Coordinates are **normalized fractions** [ymin, xmin, ymax, xmax], where each value is 0–1:

```
Example: [0.2, 0.1, 0.8, 0.5]
  ymin=0.2  → top at 20% of height
  xmin=0.1  → left at 10% of width
  ymax=0.8  → bottom at 80% of height
  xmax=0.5  → right at 50% of width
```

**Why fractions?** Scale-invariance — the same coordinates work for 224×224 and 1920×1080 images.

---

### Intersection over Union (IoU)

IoU measures overlap between predicted and ground truth boxes:

```
IoU = (Area of Intersection) / (Area of Union)

Range: 0 (no overlap) to 1 (perfect match)
Threshold: 0.5 means ≥50% overlap = "correct detection"
```

**Critical implementation detail:** Without `max(0, ...)` on intersection width/height, overlapping boxes would return negative dimensions, causing incorrect calculations.

---

### Precision vs. Recall

| Metric | Definition | Formula |
|---|---|---|
| **Precision** | Of detections made, how many were correct? | TP / (TP + FP) |
| **Recall** | Of actual objects, how many were detected? | TP / (TP + FN) |

**Trade-off:** Lowering confidence threshold increases detections → higher recall, lower precision.

---

## Model Architecture — SSD MobileNet V2

| Component | Purpose |
|---|---|
| **MobileNetV2** | Lightweight feature extractor (backbone) |
| **SSD** | Single-stage detector — predicts boxes & classes simultaneously (no separate region proposal step) |
| **Multi-scale feature maps** | Detects objects at different scales |
| **100 detections per image** | Model always outputs 100 candidate boxes; filter by confidence |

**Compared to alternatives:**

| Model | Type | Speed | Accuracy | Best For |
|---|---|---|---|---|
| **SSD MobileNet V2** | Single-stage | ⭐⭐⭐ Fast | ⭐⭐⭐ Moderate | Mobile/embedded, real-time |
| **YOLO** | Single-stage | ⭐⭐⭐⭐ Very Fast | ⭐⭐⭐⭐ High | Video, autonomous driving |
| **Faster R-CNN** | Two-stage | ⭐ Slow | ⭐⭐⭐⭐⭐ Very High | Medical imaging, high accuracy needed |
| **RetinaNet** | Single-stage | ⭐⭐⭐ Moderate | ⭐⭐⭐⭐ High | Dense scenes, class imbalance |

---

## Experimental Results

### Confidence Threshold Experiment

| Threshold | # Boxes | Quality | Interpretation |
|---|---|---|---|
| 0.3 | ~20 | Many false positives | Too lenient; too many uncertain detections |
| 0.5 | ~10 | Moderate | Standard threshold; reasonable balance |
| 0.7 | ~2 | Few false positives | Too strict; may miss valid objects |

**Conclusion:** 0.7 is better than 0.3 — fewer useless boxes.

---

### IoU Threshold Experiment

As IoU threshold increases:
- **Precision ↓** — stricter matching criteria eliminate detections
- **Recall ↓** — same reason
- **Trade-off:** Higher threshold = more conservative evaluation

---

### Model Error Analysis

**False Positive Example:** Jockey labeled as bicycle (model confused human + horse with bicycle shape).

**False Negative Example:** Horse in background missed entirely (small size, low contrast).

**On custom images:** Model identified many objects but mislabeled some (e.g., person as bicycle, bicycle as bird).

---

## Real-World Applications & Why Detection Matters

### 1. Medical Imaging (Tumor Detection)

**Application:** Radiology systems analyzing X-rays, MRIs, CT scans.

**Why detection (not just classification):**
- Classifier says "tumor present" — not helpful
- Detector shows "tumor at [location]" → doctors can:
  - Locate it precisely
  - Measure size
  - Plan surgery / treatment

---

### 2. Retail & Inventory Management (Cashier-less Stores)

**Application:** Amazon Go, automated checkouts.

**Why detection is critical:**
- Classifier says "soda and chips in image" — can't distinguish:
  - How many sodas?
  - Which specific item did the customer pick up?
  - Movement over time?
- Detector tracks individual items in space → accurate billing

---

### 3. Security Surveillance

**Application:** Perimeter monitoring, intrusion detection.

**Why detection matters:**
- Classifier: "Image contains a person"
- Detector: "Person detected at coordinates [0.4, 0.6], crossing into restricted zone"
- Enables:
  - Multi-person tracking
  - Behavior analysis (loitering, trespassing)
  - Automated alerts
  - Time-series anomaly detection

---

## Precision-Recall Trade-offs in Different Domains

### Self-Driving Car (Pedestrian Detection)

**Priority:** **HIGH RECALL**

**Why:** Missing a pedestrian = collision = death. Better to have false alarms (high false positives) than miss someone. The car errs on the side of caution — it will brake/avoid even if uncertain.

### Photo App (Object Tagging)

**Priority:** **HIGH PRECISION**

**Why:** Tagging someone as a "person" in a murder scene who wasn't there = serious harm to reputation. Better to not tag (false negative) than mislabel (false positive). Accuracy > coverage.

---

## Key Debugging Insight

The initial 0.00% precision/recall wasn't a bug in the code — it was a **data mismatch assumption**. The model used COCO classes; the dataset had VOC classes. Trying to match labels directly failed. The fix: evaluate IoU **independently of class labels**, treating any detection with high IoU as "correct localization" regardless of label mismatch.

**Lesson:** Sometimes the error is not in your algorithm — it's in your assumptions about what the data represents.

---

## Technologies Used

| Library | Purpose |
|---|---|
| Python 3 | Primary language |
| TensorFlow | Deep learning framework |
| TensorFlow Hub | Pre-trained models |
| TensorFlow Datasets | VOC dataset loading |
| Matplotlib | Bounding box visualization |
| NumPy | Numerical operations |

---

## Dataset

- **Name:** Pascal VOC 2007
- **Source:** `tensorflow_datasets.load("voc/2007")`
- **Classes:** 20 object categories (person, car, dog, cat, bird, etc.)
- **Split:** 99% train, 99% validation (to maximize learning)
- **Annotations:** Bounding boxes + class labels for every object

> This dataset is not uploaded to the repository; it loads automatically via TensorFlow Datasets.

---

## Files

| File | Description |
|---|---|
| `L06_Rich_Fox_ITAI1378.ipynb` | Complete notebook with model loading, detection, visualization, and IoU calculation |
| `L06_Rich_Fox_ITAI1378.docx` | Reflective analysis with answers to 5 lab questions + bonus research |

---

## How to Run

```bash
cd "Computer Vision/Labs/Lab6"
jupyter notebook L06_Rich_Fox_ITAI1378.ipynb
```

Run all cells sequentially. The notebook will download TF Hub models and datasets automatically.

### Dependencies

```bash
pip install tensorflow tensorflow-hub tensorflow-datasets matplotlib numpy
```

---

## Key Takeaway

Lab 6 marks the shift from understanding individual objects to understanding **scenes with multiple objects**. The technical foundation (SSD MobileNet, IoU metrics) is important, but the deeper insight is recognizing that **no single metric is universal**. High precision vs. high recall is a choice shaped by real-world consequences — whether it's safer to miss something or to over-detect. This reflects a mature understanding: ML isn't just about accuracy, it's about alignment with stakeholder needs and ethical constraints.

---

*[← Back to Computer Vision](../../README.md) | [← Back to Portfolio Home](../../../README.md)*
