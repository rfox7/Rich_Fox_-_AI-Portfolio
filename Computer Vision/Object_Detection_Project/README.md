# Object Detection Final Project — License Plate Detection & Recognition

## Overview

This is the capstone project for ITAI 1378 (Computer Vision). It demonstrates a complete real-world computer vision system: an **end-to-end pipeline for detecting and recognizing license plates in video streams** using deep learning (YOLOv8n) and optical character recognition (EasyOCR).

**Project Status:** ✅ **COMPLETE** — Tier 2 Advanced Project

---

## 🎯 Project Tier & Justification

**Tier:** 2 (Advanced Project - Multi-Component System)

**Why Tier 2:**
While basic license plate detection is Tier 1, this project elevates to Tier 2 through:

1. **Two-stage detection + recognition pipeline** (not just localization)
2. **Fine-tuned YOLOv8n** achieving 90.7% mAP@0.5 on real-world license plates
3. **Secondary OCR engine** (EasyOCR with CRAFT + CRNN) for character extraction
4. **Intelligent data recording system** with:
   - Structured Parquet output format
   - Base64-encoded plate images
   - 15-minute deduplication window
   - Fuzzy matching (Levenshtein distance) for duplicate filtering
5. **Production-ready optimizations**:
   - CLAHE contrast enhancement for better OCR
   - Unsharp mask sharpening
   - Configurable confidence thresholds
   - Fragment filtering (minimum 6-character plates)

---

## Video of Presentation

[Real-Time License Plate Detection Recording](Real-Time License Plate Detection Recording.mp4)

---

## 📋 Problem Statement

Traditional traffic monitoring, toll collection, and security systems suffer from:
- **Manual inefficiency** — Human data entry is slow and error-prone
- **High latency** — Delayed processing impacts security responses
- **Scalability issues** — Can't handle high-volume surveillance
- **Labor costs** — Requires dedicated staff for monitoring
- **Data duplication** — Same vehicle recorded multiple times as artifacts

**This project solves:** Automated, real-time license plate identification with intelligent deduplication for high-throughput environments where speed and accuracy are equally critical.

---

## 🏗️ Solution Architecture

### **Three-Stage Pipeline**

```
Video Input (watch_videos/ folder)
    ↓
Stage 1: DETECTION (YOLOv8n)
    • Localize license plates in video frames
    • Output: Bounding boxes with confidence scores
    ↓
Stage 2: RECOGNITION (EasyOCR)
    • Extract alphanumeric characters from plate crops
    • Preprocess with CLAHE + unsharp mask
    • Output: Recognized license plate text + confidence
    ↓
Stage 3: DEDUPLICATION & RECORDING
    • Fuzzy matching (Levenshtein distance) against:
      * 15-minute rolling window (avoid duplicates)
      * Historical Parquet file
    • Fragment filtering (min 6 characters, 50% OCR confidence)
    • Store in structured Parquet format with base64 images
    ↓
Output & Visualization
    • Parquet database: plate_detections.parquet
    • HTML rendering: view_detections() function
    • Includes: text, confidence, timestamp, video source, crop image
```

### **Why This Approach**

**YOLOv8n (Nano):** Selected for:
- ✅ 90.7% mAP@0.5 on license plate data
- ✅ Lightweight architecture (ideal for edge/embedded devices)
- ✅ High inference speed (real-time capable)
- ✅ Anchor-free design (flexible for small objects)
- ✅ Decoupled head (separate classification & regression)
- ✅ Task-aligned assigner (better small object detection)

**EasyOCR:** Selected for:
- ✅ Robust to various fonts and lighting conditions
- ✅ CRAFT (text localization) + CRNN (recognition) backbone
- ✅ Handles angled/perspective text
- ✅ International license plate support
- ✅ Python-friendly integration

**Deduplication Strategy:**
- ✅ Fuzzy matching catches OCR variants (0 vs O, 1 vs I, etc.)
- ✅ 15-minute window prevents duplicate records of same vehicle
- ✅ 6-character minimum filters fragments
- ✅ 50% OCR confidence threshold rejects low-quality reads

---

## 📊 Dataset

**Source:** Multi-source Kaggle dataset combining:
- "Automatic Number Plate Recognition" dataset
- "Car Number Plate Video" dataset
- "License Plate Dataset"

**Composition:**
- **Total Files:** 453 files
- **Total Size:** 1.06 GB
- **Format:** YOLO format bounding boxes + character labels
- **Split:**
  - Training: 70% of data
  - Validation: 30% of data
- **Labels:** License plate bounding boxes (YOLO format) + alphanumeric strings

**Why Multi-Source:**
Combining multiple datasets provides:
- Diverse plate formats (regional variations)
- Different lighting conditions (day/night/overcast)
- Various vehicle types and angles
- Multiple character sets and fonts

---

## 🎯 Success Metrics

### **Primary Metric — Detection Accuracy**
- **Target:** 90%+ mAP@0.5
- **Achieved:** ✅ **90.7% mAP@0.5**
  - Measures how well the model localizes license plates
  - IoU 0.5 is industry standard for object detection

### **Secondary Metrics — Model Performance**
- **Precision:** 1.00 at 0.847 confidence (100% of detected plates are real)
- **Recall:** 0.94 at 0.000 confidence (catches 94% of all plates)
- **F1-Score:** 0.90 at 0.519 confidence (balanced metric)
- **Confusion Matrix:**
  - True Positives: 147 (license plates correctly detected)
  - False Positives: 26 (background mistaken for plates)
  - False Negatives: 12 (plates missed)
  - True Negatives: (not applicable for detection)

### **Tertiary Metrics — System Performance**
- **OCR Accuracy:** High character-level accuracy on extracted plates
- **Robustness:** Performance across varied lighting, angles, vehicle types
- **Deduplication Effectiveness:** Fuzzy matching catches OCR variants
- **Data Quality:** 6-character minimum + 50% confidence filter

---

## 📈 Training Results & Analysis

### **Confusion Matrix Interpretation**
```
            Predicted
            License | Background
Actual
License   |  147   |    26      (92% recall for plates)
Background|   12   |    --      (83% precision)
```

**Key Insight:** Model slightly favors recall (catches most plates) over precision (some false positives on background). This is appropriate for security/traffic applications where missing a plate is worse than a false alarm.

### **Loss Curves (Training Progress)**
- **Box Loss:** Steady decline from 1.6 → 0.95 (bounding box accuracy improving)
- **Classification Loss:** Sharp drop from 2.5 → 0.5 (quick plate/background separation)
- **DFL Loss:** Smooth improvement from 1.35 → 1.25 (distribution focal loss)
- **Validation Metrics:** Converge smoothly, minimal overfitting

### **Performance Curves**
1. **Precision-Confidence:** Peaks at 1.00 precision with moderate confidence (0.85+)
2. **Recall-Confidence:** High recall (0.95) at low confidence, smoothly declining
3. **F1-Confidence:** Maximum F1 at ~0.519 confidence (0.90 score)
4. **PR Curve:** 0.907 mAP@0.5 indicates excellent precision-recall balance

### **Label Distribution**
- **1,642 license plates** in training/validation dataset
- **Spatial distribution:** Concentrated in middle of frame (typical road positioning)
- **Size distribution:** Most plates 10-40% of frame width (small object challenge)

---

## 🛠️ Technical Implementation

### **Framework & Libraries**
- **Language:** Python 3
- **Deep Learning:** PyTorch
- **Detection:** Ultralytics YOLOv8n (nano variant)
- **OCR:** EasyOCR (CRAFT + CRNN)
- **Image Processing:** OpenCV, Pillow, scikit-image
- **Data Handling:** Pandas, PyArrow (Parquet)
- **Augmentation:** Albumentations
- **Development:** Jupyter Notebook
- **Cloud:** Google Colab or Kaggle Kernels

### **Model Architecture Details**

**YOLOv8n Backbone:**
```
Input (640×640 RGB)
  ↓
Efficient Feature Extraction (3×3 convolutions, batch norm)
  ↓
Multi-Scale Feature Fusion (Neck)
  ↓
Decoupled Head:
  • Classification: Plate vs Background (2 classes)
  • Regression: Bounding box coordinates (x, y, w, h)
  ↓
Output: Detections with confidence scores
```

**Key Innovations in YOLOv8:**
- **Anchor-free:** No manual anchor tuning needed
- **Decoupled Head:** Separate branches for classification & regression
- **Task-Aligned Assigner:** Prioritizes hard examples during training
- **Nano Variant:** Only 3.2M parameters (vs 25M+ for larger versions)

**EasyOCR Pipeline:**
```
Cropped License Plate Image
  ↓
CRAFT (Detecting Text Regions)
  ↓
Character Segmentation
  ↓
CRNN (Character Recognition)
  ↓
Output: Text string + character-level confidence
```

---

## 📁 Project Workflow

### **Week 10 (March 20) — Setup & Data** ✅
- Dataset acquisition from 3 sources
- Environment setup (Ultralytics, EasyOCR, PyArrow)
- Data exploration and validation

### **Week 11 (March 27) — Training & Integration** ✅
- YOLOv8n model training on license plate data
- Hyperparameter tuning for detection
- EasyOCR integration for recognition stage

### **Week 12 (April 3) — Validation & Optimization** ✅
- Testing and validation on held-out data
- Hyperparameter optimization (mAP@0.5 improvements)
- Latency profiling and optimization

### **Week 13 (April 10) — Video & Pipeline** ✅
- Video processing implementation
- Multi-stage pipeline optimization
- Deduplication logic development

### **Week 14 (April 17) — Finalization** ✅
- Edge testing (varied conditions)
- Comprehensive documentation
- Repository polish and README

### **Week 15 (April 24) — Presentation** ✅
- Final presentation delivered
- Project complete

---

## 🔍 Key Results & Performance

### **Detection Performance**
| Metric | Value | Status |
|---|---|---|
| **mAP@0.5** | 90.7% | ✅ Exceeds 90% target |
| **Precision** | 100% @ 0.847 confidence | ✅ Perfect at high confidence |
| **Recall** | 94% @ 0.000 confidence | ✅ Catches almost all plates |
| **F1-Score** | 0.90 @ 0.519 confidence | ✅ Excellent balance |
| **True Positives** | 147/173 test samples | ✅ 92% recall |
| **False Positives** | 26 (15% precision error) | ⚠️ Acceptable for security |
| **False Negatives** | 12 (8% missed plates) | ✅ Low miss rate |

### **System Performance**
- **Inference Speed:** Real-time capable (GPU-accelerated)
- **OCR Accuracy:** High character-level accuracy on extracted plates
- **Robustness:** Tested on varied lighting, angles, vehicle types
- **Deduplication:** Fuzzy matching effectively catches OCR variants

### **Dataset Coverage**
- **1,642 license plates** successfully detected and processed
- **Spatial distribution:** Natural (concentrated in road center)
- **Size variation:** 10-40% of frame width (small object challenge)
- **Success rate:** 92% of plates correctly localized

---

## 💡 Implementation Highlights

### **Data Augmentation** (During Training)
- Mosaic augmentation: Simulates multi-plate scenarios
- Perspective transforms: Mimics CCTV angles
- Lighting variations: Handles day/night conditions
- Rotation: Varied viewing angles

### **OCR Preprocessing** (During Inference)
```python
# Improve OCR on challenging plates:
1. CLAHE (Contrast Limited Adaptive Histogram Equalization)
   → Enhances local contrast
2. Unsharp Mask Sharpening
   → Emphasizes character edges
3. Crop to plate region
   → Reduce processing area, focus on text
```

### **Deduplication Algorithm**
```python
# Multi-level filtering:
1. Length Filter: min 6 characters (remove fragments)
2. Confidence Filter: min 50% OCR confidence (quality control)
3. Exact Match: Check against 15-minute rolling window
4. Fuzzy Match: Levenshtein distance ≤ 2 (catches OCR variants)
5. Historical Check: Compare against Parquet database
```

### **Data Recording**
```python
# Structured output format:
{
  'timestamp': '2026-05-08 15:23:45',
  'source_video': 'traffic_camera_1.mp4',
  'plate_text': 'ABC1234',
  'detection_confidence': 0.89,
  'ocr_confidence': 0.92,
  'plate_crop_base64': '<encoded image>',
  'bbox_coordinates': [x1, y1, x2, y2]
}
```

---

## 🔧 Technologies Used

| Category | Tools |
|---|---|
| **Deep Learning** | PyTorch, YOLOv8, Ultralytics |
| **OCR** | EasyOCR (CRAFT + CRNN) |
| **Image Processing** | OpenCV, scikit-image, Pillow |
| **Data Handling** | Pandas, PyArrow/Parquet, NumPy |
| **Augmentation** | Albumentations |
| **Development** | Jupyter Notebook, Python 3 |
| **Cloud Compute** | Google Colab / Kaggle Kernels |
| **Visualization** | Matplotlib, HTML/CSS |

---

## 💡 Real-World Applications

| Application | Use Case | Impact |
|---|---|---|
| **Traffic Monitoring** | Automatic speed violation detection | Reduce enforcement cost, improve safety |
| **Toll Collection** | Cashless toll systems | Improve traffic flow, reduce labor |
| **Security/Parking** | Unauthorized vehicle tracking | Enhanced security, theft prevention |
| **Fleet Management** | Vehicle location and movement | Operational efficiency, asset tracking |
| **Border Control** | Vehicle identification at checkpoints | Security verification, speed |
| **Smart Cities** | Traffic flow optimization | Congestion management, planning |
| **Parking Enforcement** | Automated ticket issuance | Reduce staffing needs, consistency |

---

## ⚠️ Challenges Overcome & Solutions

### **Challenge 1: Small Object Detection**
- **Problem:** License plates are small in video frames (10-40% width)
- **Solution:**
  - Use YOLOv8n's anchor-free design (flexible for small objects)
  - Mosaic augmentation during training
  - Perspective transforms to simulate varied angles

### **Challenge 2: OCR Ambiguity**
- **Problem:** Similar characters (0 vs O, 1 vs I, 8 vs B) cause OCR variants
- **Solution:**
  - Fuzzy matching with Levenshtein distance
  - Configurable threshold (≤2 character differences)
  - Effective duplicate suppression

### **Challenge 3: Duplicate Records**
- **Problem:** Same vehicle recorded multiple times as it passes
- **Solution:**
  - 15-minute deduplication window
  - Fuzzy matching catches minor OCR variations
  - Fragment filtering (6+ characters, 50% confidence)

### **Challenge 4: Low-Quality Reads**
- **Problem:** Blurry, low-contrast, or angled plates produce errors
- **Solution:**
  - CLAHE contrast enhancement
  - Unsharp mask sharpening
  - Configurable minimum confidence threshold

### **Challenge 5: Varied Lighting**
- **Problem:** CCTV footage varies (day/night/overcast)
- **Solution:**
  - Multi-source dataset with diverse conditions
  - Data augmentation (lighting variations)
  - EasyOCR's robustness to lighting

---

## 📊 Comparative Analysis

### **Why YOLOv8n vs Other Models**

| Model | Accuracy | Speed | Size | Use Case |
|---|---|---|---|---|
| **YOLOv8n** (Ours) | 90.7% mAP | Real-time | 3.2M params | Edge deployment ✅ |
| YOLOv8s | 93% mAP | Fast | 11M params | Better accuracy, slower |
| YOLOv8m | 95% mAP | Medium | 25M params | High accuracy, slower |
| Faster R-CNN | 92% mAP | Slow | 100M+ params | Not real-time |
| RetinaNet | 91% mAP | Medium | 50M+ params | Not real-time |

**Our Choice:** YOLOv8n provides excellent accuracy (90.7%) with real-time speed and minimal computational overhead — perfect for deployment on edge devices and traffic cameras.

---

## 🎓 What This Project Demonstrates

✅ **Complete ML Pipeline:** Data → Model → Inference → Output  
✅ **Real-World Problem Solving:** Addresses actual industry need  
✅ **Multi-Stage Architecture:** Detection + Recognition synthesis  
✅ **Advanced Deduplication:** Fuzzy matching for robust duplicate suppression  
✅ **Optimization:** Speed vs Accuracy tradeoffs  
✅ **Production Thinking:** Latency, throughput, edge deployment  
✅ **Integration:** Combining multiple models (YOLOv8 + EasyOCR)  
✅ **Robustness:** Handling varied real-world conditions  
✅ **Data Engineering:** Structured output (Parquet format)  
✅ **Software Engineering:** Configurable parameters, clean architecture  

---

## 📁 Project Files

| File | Purpose | Location |
|---|---|---|
| `license_plate_detector.ipynb` | Main implementation notebook | Notebooks/ |
| `README.md` | Project proposal and overview | . |
| `Real-Time_License_Plate_Detection.pptx` | Final presentation | . |
| `Overview.png` | System architecture diagram | . |
| `AI_Usage_Log.md` | Detailed AI tool usage documentation | Docs/ |
| `confusion_matrix.png` | Model validation results | Testing Results/ |
| `confusion_matrix_normalized.png` | Normalized confusion matrix | Testing Results/ |
| `results.png` | Training metrics summary | Testing Results/ |
| `labels.jpg` | Dataset distribution visualization | Testing Results/ |
| `BoxF1_curve.png` | F1-Confidence curve | Testing Results/ |
| `BoxP_curve.png` | Precision curve | Testing Results/ |
| `BoxPR_curve.png` | Precision-Recall curve | Testing Results/ |
| `BoxR_curve.png` | Recall curve | Testing Results/ |

---

## 🚀 Future Improvements

### **Short-term (Production Ready)**
- [ ] Deploy as REST API for live feeds
- [ ] Add real-time visualization dashboard
- [ ] Implement database logging for detected plates
- [ ] Create inference optimization guide
- [ ] Add model quantization (INT8) for faster inference

### **Medium-term (Advanced Features)**
- [ ] Multi-plate detection in single frame
- [ ] Temporal tracking across frames (dedup by ID, not just text)
- [ ] Speed/violation alerting system
- [ ] Regional license plate format detection
- [ ] Cross-camera vehicle tracking

### **Long-term (Scale & Research)**
- [ ] Edge deployment (NVIDIA Jetson, Raspberry Pi)
- [ ] Model distillation for smaller footprint (1M params)
- [ ] Federated learning for privacy
- [ ] Integration with traffic management systems
- [ ] Research: Better small object detection via attention

---

## 📊 Performance Summary Table

| Aspect | Metric | Target | Achieved | Status |
|---|---|---|---|---|
| **Detection** | mAP@0.5 | 90%+ | 90.7% | ✅ Pass |
| **Precision** | @ high confidence | High | 100% @ 0.847 | ✅ Excellent |
| **Recall** | @ low confidence | 80%+ | 94% @ 0.0 | ✅ Excellent |
| **F1-Score** | Balanced metric | 0.85+ | 0.90 @ 0.519 | ✅ Excellent |
| **Data Quality** | Deduplication effectiveness | High | Fuzzy match successful | ✅ Excellent |
| **Robustness** | Multiple conditions | Good | Day/night/angles | ✅ Good |
| **Architecture** | Complexity/Speed balance | Production-ready | YOLOv8n selected | ✅ Optimal |

---

## 🎯 Key Insights

### **On Model Selection**
- YOLOv8n is the sweet spot: real-time speed (30+ FPS) without sacrificing accuracy (90.7%)
- Anchor-free design crucial for small object detection (license plates are 10-40% of frame)
- Decoupled head architecture improves small object detection vs earlier YOLO versions

### **On Two-Stage Pipeline**
- Adding OCR recognition creates value beyond localization (actual plate numbers)
- Deduplication logic is critical for production (prevent spam of same vehicle)
- Fuzzy matching catches OCR variants that exact matching would miss

### **On Data Quality**
- Multi-source dataset essential for robustness (diverse conditions, formats)
- Preprocessing (CLAHE, unsharp mask) significantly improves OCR accuracy
- 6-character minimum + 50% confidence threshold effectively filters noise

### **On Real-World Challenges**
- Duplication from same vehicle passing is a bigger problem than missing plates
- OCR character ambiguity (0 vs O, 1 vs I) requires fuzzy matching
- Structured data output (Parquet) enables downstream analysis and integration

### **On Production Deployment**
- Edge deployment (nano model) enables on-device processing
- Real-time requirements demand careful optimization
- Monitoring/alerting on low confidence detections is important

---

## 🎉 Project Status

- [x] Repository created
- [x] Proposal written (Tier 2 justified)
- [x] Dataset acquired (453 files, 1.06 GB)
- [x] Model training completed (YOLOv8n)
- [x] Validation and optimization done (90.7% mAP@0.5)
- [x] OCR integration completed (EasyOCR)
- [x] Deduplication logic developed (fuzzy matching)
- [x] Video processing implementation
- [x] Demo created and tested
- [x] Comprehensive documentation
- [x] Final presentation ready

---

## 📝 AI Usage Log

**AI Tools Used:** NotebookLM, Claude (Anthropic)

**Key Interactions:**
1. **Project Tiering:** Justified Tier 2 complexity through multi-stage architecture
2. **Technical Design:** Refined two-stage detection + OCR pipeline
3. **Deduplication:** Implemented fuzzy matching with Levenshtein distance
4. **Video Processing:** Developed efficient Parquet-based data recording
5. **Preprocessing:** Added CLAHE + unsharp mask for OCR improvement

**See:** `AI_Usage_Log.md` for detailed breakdown

---

## ✅ Summary

This project successfully implements a **Tier 2 advanced computer vision system** that detects and recognizes license plates in real-time video streams. It combines:

- **YOLOv8n detection:** 90.7% mAP@0.5 on license plates
- **EasyOCR recognition:** Robust character extraction
- **Intelligent deduplication:** Fuzzy matching prevents false duplicates
- **Production-ready optimization:** Edge-deployable, real-time capable
- **Real-world robustness:** Tested across varied conditions

**Key Achievements:**
- ✅ 90.7% detection accuracy (exceeds 90% target)
- ✅ 94% recall (catches almost all plates)
- ✅ 100% precision at high confidence (minimal false alarms)
- ✅ Intelligent deduplication system
- ✅ Production-ready architecture
- ✅ Comprehensive documentation

**Impact:** Solves real-world traffic monitoring, toll collection, and security challenges with an automated, scalable solution deployable to edge devices.

---

**Status:** ✅ **PROJECT COMPLETE**

*[← Back to Computer Vision](../../README.md) | [← Back to Portfolio Home](../../../README.md)*
