# Applied AI & Computer Vision (ITAI 1378) — Complete Portfolio

> **Student:** Rich Fox  
> **Institution:** HCC (Houston Community College)  
> **Program:** Applied AI & Robotics  
> **Course:** ITAI 1378 — Computer Vision with AI  
> **Duration:** 12 Modules (Labs 1–11 + Final Project)  
> **Academic Year:** 2025–2026

---

## Portfolio Overview

This portfolio documents a comprehensive journey through modern computer vision and AI — from foundational image processing through classical machine learning, deep learning, multimodal understanding, and finally autonomous agents with frameworks.

**The narrative arc:**
1. **Labs 1–2:** Visual fundamentals — understanding images as data, basic operations
2. **Lab 3:** The transition — classical ML struggles reveal why deep learning is needed
3. **Labs 4–6:** Deep learning emergence — CNNs learn better representations, localize objects
4. **Labs 7–8:** Multimodality — reasoning across vision and language; recognizing limitations
5. **Labs 9–11:** Autonomous systems — agents perceive, reason, act; track objects over time
6. **Final Project:** Real-world capstone synthesizing all concepts

---

## Lab Breakdown

### **Lab 1 — Digital Image Processing Fundamentals**
- **Focus:** Image as matrices of pixels; pixel-level operations
- **Techniques:** Brightness/contrast, sharpening, blurring, edge detection, histogram equalization, geometric transforms, CLAHE
- **Key Learning:** Photos are manipulable data; understanding signal processing enables computer vision
- **Real-world link:** Photography, medical imaging, remote sensing

---

### **Lab 2 — Image Processing Fundamentals**
- **Focus:** Hands-on implementation of core image processing operations
- **Techniques:** Point operations (brightness/contrast), neighborhood operations (convolution), kernel-based filtering, histogram analysis, geometric transformations, creative effects
- **Key Learning:** Complex effects combine simple operations; traditional techniques form the foundation of AI vision tools
- **Real-world link:** Instagram filters, medical imaging enhancement, autonomous vehicle perception, AR/VR applications
- **Connection to Labs 3+:** Convolution (hand-designed kernels) is exactly what CNNs learn automatically

---

### **Lab 3 — Classical ML vs. Deep Learning (Overfitting & Generalization)**

**Part A: Face Recognition with HOG/LBP + SVM/Random Forest**
- **Dataset:** Olivetti Faces (400 images, 40 people, 10 images/person)
- **Features:** HOG (1,764 dims) vs. LBP (10 dims) vs. raw pixels (4,096 dims)
- **Models:** SVM, Random Forest
- **Critical lesson:** A model with 99% training accuracy can completely fail on validation data (overfitting)
- **Evaluation:** Gap between train/validation accuracy reveals overfitting; cross-validation provides realistic estimates

**Part B: CIFAR-10 Image Classification with SVM**
- **Dataset:** 3-class subset (cat, dog, ship) from CIFAR-10
- **Pipeline:** Grayscale conversion → Normalization → Flattening → Linear SVM
- **Limitation:** Raw pixel features carry noise; classical ML struggles with natural images

**Key insight:** Classical ML's limitation (poor performance on raw pixels) motivates the shift to deep learning.

---

### **Lab 4 — Foundational CNNs (PyTorch)**

**Project:** Chihuahua vs. Muffin Classifier

- **Architecture:** Custom CNN with 4 convolutional blocks + 2 fully connected layers
- **Input:** 128×128 color images
- **Key concepts:** 
  - Convolutions preserve spatial structure
  - MaxPooling reduces dimensionality
  - Data augmentation prevents overfitting
- **Results:** ~15-20% accuracy improvement over classical ML on this task
- **Lesson:** CNNs are the standard for image tasks because they exploit 2D structure

---

### **Lab 5 — CNN Optimization & Comparative Analysis**

**Project:** Chihuahua vs. Muffin Classifier (optimized)

- **Improvements:** Larger input (224×224), batch size tuning, learning rate optimization
- **Speed comparison:** CNN ~15 seconds vs. traditional NN ~20 minutes (80× faster)
- **Critical reflection:**
  - High training accuracy ≠ good model (hallucination of generalization)
  - Test accuracy alone doesn't guarantee real-world performance (bias in training data)
  - All muffins were blueberry; all chihuahuas similar color → model biased
- **Ethical learning:** Responsible AI requires understanding limitations, auditing for bias, and human-in-the-loop oversight

---

### **Lab 6 — Object Detection (SSD MobileNet V2)**

**Project:** Detecting multiple objects with bounding boxes using pretrained models

- **Dataset:** Pascal VOC 2007 (20 classes)
- **Model:** SSD MobileNet V2 from TensorFlow Hub
- **Key metrics:**
  - **IoU (Intersection over Union):** Measures detection accuracy
  - **Precision vs. Recall:** Fundamental trade-off
  - **Confidence threshold:** Filters low-confidence detections
- **Real-world applications:**
  - Medical imaging (tumor location)
  - Retail (inventory tracking)
  - Security (person tracking and alerts)
- **Critical insight:** No single metric is universal — choice of precision vs. recall depends on downstream consequences

---

### **Lab 7 — Visual Language Models (CLIP & BLIP)**
*Referenced in portfolio; full documentation in Lab 8*

**Focus:** AI systems that jointly understand images and text

---

### **Lab 8 — VLM Applications, Ethics & Deployment**

**Depth:** Critical analysis of VLM limitations and responsibilities

**Core concepts:**
- **Hallucinations:** Confident false information; critical in high-stakes domains
- **Bias:** Inherited from training data; amplified at scale
- **Precision-recall trade-offs:** Different applications prioritize differently
  - Self-driving car: high recall (missing pedestrian = death)
  - Photo app: high precision (false ID = reputational harm)
- **Deployment options:**
  - API services: instant scaling, data privacy concerns, usage-based cost
  - Self-hosted: fixed costs, privacy control, infrastructure burden
  - Break-even: ~20,000 images/month

**Architectural decision framework:**
- CLIP → zero-shot classification
- BLIP → generation (captioning, VQA)
- LLaVA → conversation/dialogue
- GPT-4V → complex reasoning

**Ethical imperatives:**
- "Golden Rule": VLMs are powerful **assistants**, not autonomous decision-makers
- Mandatory human-in-the-loop for high-stakes decisions
- Transparency about limitations to users

---

### **Lab 9 — AI Agents (Perception-Reasoning-Action Loop)**

**Synthesis:** Everything from Labs 1–8 combines into autonomous agents

**The PRA Loop:**
1. **Perception:** YOLO detects objects in video frames
2. **Reasoning:** Simple logic ("if person, then alert") or complex rules
3. **Action:** Print alert, display visualization, trigger automation

**Real-world challenges:**
- YOLO struggles with distance, odd poses, lighting
- Lab accuracy ≠ deployment accuracy (gap revealed in bird detection on ocean video)
- Defensive engineering: frame skipping, confidence thresholds, human review

**Applications:**
- Self-driving cars (detect pedestrians, signs, vehicles)
- Security monitoring (detect intrusion)
- Industrial inspection (detect defects)

---

### **Lab 10 — Agent Frameworks (Tools, Memory, Workflow)**

**Capstone:** Scaling simple agents to complex, extensible systems

**Three core components:**

1. **Tools:** Functions/services the agent can invoke
   - Each tool has clear input/output
   - Examples: get_weather(), calculate(), search_database()

2. **Workflow:** Decision logic that routes queries to tools
   - Simple: Keyword-based if-elif-else
   - Advanced: LLM decides which tool fits the task

3. **Memory:** Persistent storage of context and learned facts
   - Short-term: Conversation history
   - Long-term: Knowledge base, user profiles
   - Our simple agent had none; production agents need both

**Framework benefits:**
- Decouple tools from workflow
- Add capabilities without redesigning core logic
- Reusable components across agents
- Clear abstractions for testing

**Trade-offs:**
- Rule-based routing: predictable, debuggable, limited
- LLM-based routing: flexible, expensive, unpredictable

---

### **Lab 11 — Object Tracking & Zone-Based Analytics**

**Advanced:** Temporal understanding of object movement and behavior

**Key concepts:**
- **Detection vs. Tracking:** Detection identifies objects; tracking follows them over time
- **Persistent ID:** YOLO with `persist=True` maintains object IDs across frames
- **Zone-based analytics:** Define regions and analyze object behavior within them

**Applications:**
- **Retail:** Optimize staffing by monitoring customer flow
- **Traffic:** Detect congestion and flow patterns
- **Security:** Detect intrusion in restricted areas
- **Healthcare:** Monitor social distancing

**Production challenges:**
- **Occlusion:** Objects hidden behind obstacles get new IDs → duplicate counts
- **ID switching:** Overlapping objects cause ID swaps → confusing trajectories
- **Flickering:** Poor lighting causes detection gaps → tracking instability

---

## Cross-Lab Themes

### **1. The Feature Representation Problem**

| Lab | Representation | Limitation |
|---|---|---|
| **Lab 2** | Hand-crafted (blur, sharpen, edge) | Manually designed; not adaptive |
| **Lab 3** | Hand-crafted (HOG, LBP) | Time-intensive; domain-specific |
| **Lab 3B** | Raw pixels | Noisy; high-dimensional |
| **Lab 4–5** | Learned CNN features | Domain-specific; requires training |
| **Lab 6** | Pretrained CNN backbone | Transfer learning; potential bias |
| **Lab 8** | Multimodal embeddings | Can hallucinate; not grounded |

**Insight:** Better representations = better downstream performance. The entire field of representation learning seeks to learn features that generalize.

---

### **2. The Overfitting-Generalization Tension**

| Lab | Challenge | Solution |
|---|---|---|
| **Lab 3** | 99% training accuracy = terrible validation | Cross-validation; focus on validation gap |
| **Lab 5** | Small dataset (120 images) | Data augmentation; dropout |
| **Lab 6** | Dataset mismatch (COCO vs. VOC) | IoU-based evaluation; ignore labels |
| **Lab 8** | VLM bias from training data | Audit across diverse inputs |
| **Lab 11** | YOLO misses objects in deployment | Understand the gap; defensive engineering |

**Fundamental insight:** Your training set is always biased toward your data. Real world is different. Bridge the gap through careful evaluation and human oversight.

---

### **3. The Accuracy-Interpretability Trade-off**

| Approach | Accuracy | Interpretability | Use Case |
|---|---|---|---|
| **Rule-based (Lab 10)** | Lower | High | Simple, auditable decisions |
| **Classical ML (Lab 3)** | Moderate | Moderate | Baseline, constrained resources |
| **Deep Learning (Labs 4–6)** | High | Low | Complex patterns; trust required |
| **Multimodal (Lab 8)** | High* | Low | Rich understanding; hallucinations |
| **Agent frameworks (Lab 10)** | High | Depends on workflow | Flexible; trade interpretability for power |

*Depends on downstream task; often high performance doesn't translate to deployment.

---

### **4. From Narrow AI → General Reasoning**

**Labs 1–3:** **Narrow AI** — solve specific task (classify this image)

**Labs 4–6:** **Specialized Deep Learning** — object detection, image-specific CNNs

**Labs 7–8:** **Multimodal Understanding** — reason across vision + language

**Labs 9–11:** **Agentic AI** — perceive environment, reason flexibly, take diverse actions

---

## Key Metrics & Evaluation Methods

| Metric | Use Case | Formula | Interpretation |
|---|---|---|---|
| **Accuracy** | Overall correctness | (TP + TN) / Total | What % of predictions are correct? |
| **Precision** | Low false positive cost | TP / (TP + FP) | Of predicted positives, how many are correct? |
| **Recall** | Low false negative cost | TP / (TP + FN) | Of actual positives, how many did we find? |
| **F1-Score** | Balanced trade-off | 2(P×R)/(P+R) | Harmonic mean of precision & recall |
| **IoU** | Detection localization | Intersection / Union | How much does predicted box overlap truth? |
| **BLEU / CIDEr** | Caption quality | N-gram overlap with reference | Does generated caption match ground truth? |
| **Recall@K** | Ranking/retrieval | "Is true item in top K?" | Does search return what we wanted? |

---

## Real-World Applications Across Labs

### **Healthcare**
- **Labs 1–2:** Medical image preprocessing (sharpen, segment)
- **Lab 3:** Classify tissue types
- **Lab 6:** Detect tumors (need localization, not just classification)
- **Lab 8:** Generate radiology reports (VLM)
- **Labs 9–11:** Diagnostic agent combining imaging + patient history

### **Autonomous Vehicles**
- **Labs 4–5:** Perceive road environment (CNN backbone)
- **Lab 6:** Detect pedestrians, vehicles, signs (localization critical)
- **Lab 9:** PRA loop — perceive hazards, reason about response, execute (brake/steer)
- **Lab 11:** Track vehicle positions over time; predict trajectories

### **Retail**
- **Lab 3:** Product classification
- **Lab 6:** Object detection for inventory tracking
- **Lab 8:** Visual search (find products via images)
- **Lab 11:** Monitor customer flow; optimize staffing

### **Security & Surveillance**
- **Lab 6:** Detect people, vehicles, intrusions
- **Lab 8:** Flag unusual activity (multimodal context)
- **Lab 9:** Alert on unauthorized access
- **Lab 11:** Track suspect through building; maintain identity across frames

---

## Critical Lessons for Real-World Deployment

### **1. Understand Your Data**
- Bias exists. Audit your training set for representation.
- Distribution shift: your test set differs from deployment.
- Label quality matters more than quantity.

### **2. Separate Train/Val/Test**
- Never touch test data until final evaluation.
- Validation gap (train - val) reveals overfitting.
- Cross-validation provides robust estimates.

### **3. Choose Metrics Aligned With Consequences**
- High-stakes decisions (medical): prioritize recall + human review
- Convenience (photo tagging): prioritize precision + minimal false alarms
- Safety (self-driving): balance both; involve domain experts

### **4. Embrace Ensembles and Uncertainty**
- Single models are unreliable. Use multiple models.
- Uncertainty estimates (confidence) are informative only if calibrated.
- Always maintain human-in-the-loop for important decisions.

### **5. Invest in Interpretability**
- "Black box AI" is unacceptable for high-stakes domains.
- Techniques: LIME, SHAP, attention visualization, saliency maps
- If you can't explain your model's decision, you shouldn't deploy it

### **6. Plan for Failure Modes**
- What happens if the model is wrong?
- What are the consequences (financial, reputational, safety)?
- Can you detect when the model is uncertain?
- Is human review feasible and affordable?

### **7. Monitor in Production**
- Accuracy degrades over time as data distribution shifts.
- Set up alerts for performance drops.
- Maintain audit trails for accountability.
- Retrain regularly with new data.

---

## Technologies & Frameworks Used

### **Core Libraries**
- **PyTorch & TensorFlow:** Deep learning frameworks
- **OpenCV:** Computer vision (video, image processing)
- **Scikit-learn:** Classical ML, metrics, evaluation
- **Scikit-image:** Image processing features (HOG, LBP)

### **Pre-trained Models**
- **YOLO (YOLOv8):** Real-time object detection and tracking
- **CLIP, BLIP:** Vision-language models from Hugging Face
- **SSD MobileNet V2:** Object detection (TensorFlow Hub)

### **Supporting Tools**
- **Matplotlib, Seaborn:** Visualization
- **NumPy, Pandas:** Data manipulation
- **Jupyter:** Interactive notebooks
- **Git:** Version control

### **Production Frameworks (Not used in labs; mentioned for context)**
- **LangChain:** Agent orchestration
- **LlamaIndex:** Document indexing and retrieval
- **MLflow:** Model tracking and deployment
- **Docker:** Containerization
- **Kubernetes:** Scaling

---

## Key Takeaway: The Maturity Arc

**Labs 1–3:** Understanding fundamentals
- Images are data
- Features matter
- Trade-offs exist (speed vs. accuracy, train vs. generalization)

**Labs 4–6:** Moving to deep learning
- Learned representations outperform hand-crafted features
- Scale matters (more data, bigger models, bigger compute)
- Specialization emerges (task-specific architectures)

**Labs 7–8:** Recognizing limitations
- Confidence ≠ accuracy
- Bias is systemic, not incidental
- Hallucinations are a feature, not a bug
- Ethical considerations are non-negotiable

**Labs 9–11:** Building systems
- Perception alone is insufficient; reasoning and action matter
- Frameworks enable composition and extensibility
- Temporal understanding unlocks production applications
- Trade-offs (simplicity/power, interpretability/capability) are explicit, not hidden

---

## For Future Study

### **Next Steps in Vision**
1. **Semantic Segmentation:** Pixel-level classification (DeepLab, SegFormer)
2. **Instance Segmentation:** Per-object masks (Mask R-CNN, DETR)
3. **3D Vision:** Depth estimation, 3D reconstruction
4. **Video Understanding:** Temporal reasoning (3D CNNs, transformers)
5. **Efficient Models:** MobileNet, SqueezeNet for edge devices

### **Next Steps in Multimodal AI**
1. **Retrieval Augmented Generation (RAG):** Ground VLMs in knowledge bases
2. **Vision Transformers (ViTs):** Beyond CNNs; attention for vision
3. **Diffusion Models:** Generative models for images and video
4. **Multimodal Fusion:** Combining vision, language, audio, sensor data

### **Next Steps in Agents**
1. **Tool Use & Function Calling:** LLMs invoking real APIs
2. **Multi-Agent Collaboration:** Agents coordinating to solve complex tasks
3. **Reinforcement Learning:** Agents learning through trial and error
4. **Embodied AI:** Agents with physical bodies (robotics)

### **Next Steps in Responsible AI**
1. **Fairness & Bias Mitigation:** Techniques for reducing discrimination
2. **Explainability (XAI):** Understanding model decisions
3. **Privacy-Preserving ML:** Federated learning, differential privacy
4. **Robustness & Adversarial Training:** Making models resist attacks

---

## Course Reflection

This 12-lab journey reflects the current state of AI: we've moved from trying to hand-craft understanding (early computer vision) → learning to extract patterns at scale (deep learning) → combining modalities to reason about the world (multimodal AI) → building systems that act autonomously (agents).

Yet we've also learned humility:
- No model is perfect
- Bias is persistent and subtle
- Confidence is decoupled from accuracy
- Real-world performance is harder than benchmark performance
- Ethical considerations aren't optional

The future of applied AI isn't about building bigger models. It's about:
1. Understanding our models' limitations
2. Building systems with appropriate human oversight
3. Ensuring fairness and accountability
4. Creating AI that augments human capability, not replaces human judgment

---

*Portfolio compiled: May 2026  
All 12 labs documented | Final project pending  
Instructor: Patricia McManus  
Course: ITAI 1378 — Applied AI & Computer Vision  
Institution: Houston Community College*
