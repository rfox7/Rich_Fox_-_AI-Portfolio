# 🤖 Robot Operating System & Platform (ITAI-2374)

**Course:** ITAI-2374 — Robot Operating System & Platform
**Term:** SS 2026, Section 7 | 09/14/2026 – 12/13/2026
**Credits:** 3 (2 lecture, 4 lab)
**Modality:** Hybrid (In-Person)
**Meeting:** Mondays, 6:00 PM – 9:50 PM | Location: C145

**Instructor:** Sitaram Ayyagari
**Email:** sitaram.ayyagari@hccs.edu (use Canvas Inbox preferred)
**Response Time:** ~48 hours for email and grading

**Institution:** Houston City College – Applied AI & Robotics Program
**Status:** 🔄 **IN PROGRESS**

---

## 📚 Welcome to Robotics!

This course explores the principles, methods, and applications of robotics systems and their integration into artificial intelligence and autonomous technologies. You'll investigate how robots perceive, plan, and interact with their environment through sensors, actuators, and control systems.

The course emphasizes both **foundational concepts** and **practical, hands-on skills** using contemporary tools and real-world robotic platforms — while highlighting ethical considerations and the evolving role of robotics in AI-driven systems.

**Prerequisites:** MATH 1314, ITSC 1316 or COSC 1436, ITAI 1370, ITAI 1371, ITAI 1378, ITAI 2373

---

## 🎯 Course Student Learning Outcomes (CSLOs)

By the end of this course, you will be able to:

1. **Define** key terminology in robotics, autonomous systems, and multimodal robotics
2. **Explain** the robotics pipeline and its role within broader AI-automation workflows
3. **Implement** sensor processing, feature extraction, and ML classifiers using Python libraries (ROS, OpenCV, scikit-learn, TensorFlow)
4. **Interpret** kinematic models, sensor data, motion planning, and control systems to gain robotic insight
5. **Critique** safety concerns, privacy issues, and societal impacts of robotic technologies, proposing mitigation strategies
6. **Construct and present** an end-to-end autonomous or interactive robotic system leveraging pre-trained perception models

### **Additional Learning Objectives**
- Summarize fundamental ML concepts and types of learning (supervised, unsupervised, reinforcement)
- Apply Python-based ML tools (Scikit-learn, Pandas, AutoGluon) to build, train, and evaluate models
- Demonstrate proficiency in preparing datasets through cleaning, preprocessing, and feature engineering
- Compare and evaluate ML models using appropriate metrics and validation methods
- Critique fairness and bias issues in ML and propose mitigation strategies
- Create and communicate applied ML solutions, maintaining a professional GitHub portfolio

---

## 📖 Course Structure — 16 Modules

### **Module 1: Introduction to Robotics and Autonomous Systems**
*Addresses SLOs: 1, 2*
- Course overview and expectations
- Key applications and industry use cases
- History and evolution of robotics and autonomous systems
- Introduction to the robotics pipeline
- Overview of robotic modalities (manipulation, navigation, interaction)
- Overview of robotics tools and libraries (ROS, Gazebo)
- **Lab:** Environment setup, simple robot simulation and basic control

---

### **Module 2: Sensors and Perception**
*Addresses SLOs: 2, 3*
- Sensor types and characteristics
- Camera systems and image processing
- LIDAR and depth sensing
- Inertial measurement units (IMUs)
- Introduction to why multimodal sensing is relevant in robotics
- High-level overview of how different sensors complement each other
- Brief introduction to sensor fusion as a perception modality
- **Lab:** Sensor data collection and processing pipeline in ROS and OpenCV

---

### **Module 3: Introduction to Computer Vision and Image Processing**
*Addresses SLOs: 1, 2*
- Fundamentals of digital images and computer vision
- Image acquisition and preprocessing
- Feature detection and extraction: edges, corners, key points
- Image filtering and enhancement techniques
- Overview of object detection and recognition systems
- **Lab:** Loading, visualizing, and processing image data using OpenCV

---

### **Module 4: Robot Kinematics and Motion**
*Addresses SLOs: 2, 3*
- Forward and inverse kinematics
- Coordinate frames and transformations
- Joint space and Cartesian space representations
- Introduction to motion planning (conceptual)
- Compare kinematic representations with sensor feature representations
- **Suggested Lab:** Kinematic calculations using robotics toolboxes and visualization

---

### **Module 5: Actuators and Control Systems**
*Addresses SLOs: 3, 4*
- Actuator types and characteristics
- Motor control: servo, stepper, and DC motors
- Control system fundamentals: PID control
- Control challenges and system dynamics
- How sensor feedback systems provide data for control; challenges with real-world environments (noise, delays)
- **Lab:** Motor control implementation using microcontrollers and ROS

---

### **Module 6: Path Planning and Navigation**
*Addresses SLOs: 4*
- Introduction to path planning algorithms
- Grid-based planning
- Introduction to simultaneous localization and mapping (SLAM)
- Navigation in dynamic environments; obstacle avoidance and real-time planning
- **Lab:** Implementing path planning algorithms with visualization, extracting waypoints and trajectories

---

### **Module 7: Object Detection and Recognition**
*Addresses SLOs: 3, 4*
- Overview of object detection and recognition
- Techniques for object detection (YOLO, R-CNN)
- Applications in manipulation and navigation
- Recognition from multiple viewpoints and lighting conditions
- **Lab:** Implementing an object detection model with OpenCV, using pre-trained models

---

### **Module 8: Robot Learning and Behavior Classification**
*Addresses SLOs: 3, 4*
- Introduction to robot learning
- Feature extraction for behavior classification
- Common algorithms for behavior learning (reinforcement learning, imitation learning)
- Model evaluation and performance analysis
- Classification of robot behaviors (task recognition in manipulation)
- Common behavior patterns
- Behavior trees in real-world and industrial applications
- Use cases of behavior classification in autonomous robot operation
- **Lab:** Building a behavior classification model with scikit-learn; pre-trained behavior models with TensorFlow

---

### **Module 9: Localization and Mapping**
*Addresses SLOs: 3, 4*
- Introduction to robot localization
- Simultaneous Localization and Mapping (SLAM)
- Applications of SLAM in robotics
- SLAM with different sensor modalities (visual, LIDAR-based)
- **Lab:** Implementing SLAM algorithms with ROS, visualizing maps and trajectories

---

### **Module 10: Robot Operating System (ROS) and Integration**
*Addresses SLOs: 1, 3, 5*
- Fundamentals of ROS architecture
- Nodes, topics, services, and parameters
- Message passing and communication protocols
- Limitations of monolithic robot systems
- Introduction to distributed robotics systems (multi-robot, conceptual)
- Overview of robot middleware and integration platforms
- Ethical considerations and safety in robotic systems
- ROS in simulation and real robot deployment
- **Lab:** Implement a multi-node ROS system; explore robot simulation using Gazebo

---

### **Module 11: Human-Robot Interaction**
*Addresses SLOs: 3, 6*
- Introduction to human-robot interaction (HRI)
- Social robotics and collaborative systems
- Natural interfaces: gesture, voice, and visual interaction
- Evaluation of HRI systems
- Multi-modal interaction pipelines
- **Lab:** Using pre-trained interaction models, evaluating interaction quality

---

### **Module 12: Autonomous Systems and Decision Making**
*Addresses SLOs: 2, 6*
- Autonomous system architecture
- State estimation and sensor fusion
- Decision making and task planning
- Rule-based and learning-based autonomous systems
- Introduction to multi-agent systems (conceptual)
- Autonomous systems for mobile and manipulation tasks
- **Lab:** Build a rule-based or learning-based autonomous system for a robotics use case

---

### **Module 13: Robot Manipulation and Grasping**
*Addresses SLOs: 3, 6*
- Introduction to robot manipulation
- Grasp planning and execution
- Introduction to manipulation planning systems
- Manipulation of objects in unstructured environments
- **Lab:** Implementing grasp planning and simple manipulation with simulation and real robots

---

### **Module 14: Course Review and Modern Trends**
*Addresses SLOs: 1, 5*
- Review of all modules and key concepts
- Modern and multimodal robotics: vision, tactile, audio (overview)
- AI applications of multimodal robotics
- Robot learning and adaptation basics (overview)
- Responsible robotics: ethics, safety, privacy, and societal impact (summary)
- Review activities, Q&A, project troubleshooting, portfolio

---

### **Module 15: Final Project**
*Addresses SLOs: 6*
- Self-study class dedicated to finalizing the project
- Or Part 1 of student project presentations

---

### **Module 16: Final Project Submission**
*Addresses SLOs: 6*
- Final project due, or final exam
- **Portfolio Due**

---

## 📂 Folder Structure (To Be Completed)

```
Robot_Operating_System_Platform/
├── README.md (This file)
├── COURSE_INDEX.md (Complete course overview)
├── FILE_MANIFEST.txt (Inventory of all files)
├── COMPLETION_SUMMARY.md (Progress tracking)
│
├── Module_1/
│   └── README.md (Introduction to Robotics and Autonomous Systems)
├── Module_2/
│   └── README.md (Sensors and Perception)
├── Module_3/
│   └── README.md (Computer Vision and Image Processing)
├── Module_4/
│   └── README.md (Robot Kinematics and Motion)
├── Module_5/
│   └── README.md (Actuators and Control Systems)
├── Module_6/
│   └── README.md (Path Planning and Navigation)
├── Module_7/
│   └── README.md (Object Detection and Recognition)
├── Module_8/
│   └── README.md (Robot Learning and Behavior Classification)
├── Module_9/
│   └── README.md (Localization and Mapping)
├── Module_10/
│   └── README.md (ROS and Integration)
├── Module_11/
│   └── README.md (Human-Robot Interaction)
├── Module_12/
│   └── README.md (Autonomous Systems and Decision Making)
├── Module_13/
│   └── README.md (Robot Manipulation and Grasping)
├── Module_14/
│   └── README.md (Course Review and Modern Trends)
├── Module_15/
│   └── Final_Project_Part1_README.md
├── Module_16/
│   └── Final_Project_Submission_README.md
│
└── Notebooks/
    └── (Implementation notebooks and lab code)
```

---

## 🛠️ Tools & Technologies You'll Use

| Tool | Purpose | Relevant Modules |
|---|---|---|
| **ROS (Robot Operating System)** | Robotics middleware — nodes, topics, services | 1, 2, 5, 9, 10 |
| **Gazebo** | Robot simulation environment | 1, 10 |
| **OpenCV** | Computer vision, image processing | 2, 3, 7 |
| **scikit-learn** | Machine learning for behavior classification | 8 |
| **TensorFlow** | Deep learning, pre-trained behavior models | 8 |
| **Pandas** | Data preparation and cleaning | General |
| **AutoGluon** | Automated ML | General |
| **YOLO / R-CNN** | Object detection architectures | 7 |
| **Robotics toolboxes** | Kinematic calculations and visualization | 4 |
| **Microcontrollers** | Motor control implementation | 5 |

---

## 📊 Course Progress Tracking

| Module | Topic | Status | Lab | README |
|---|---|---|---|---|
| 1 | Introduction to Robotics & Autonomous Systems | ⏳ Pending | — | — |
| 2 | Sensors and Perception | ⏳ Pending | — | — |
| 3 | Computer Vision and Image Processing | ⏳ Pending | — | — |
| 4 | Robot Kinematics and Motion | ⏳ Pending | — | — |
| 5 | Actuators and Control Systems | ⏳ Pending | — | — |
| 6 | Path Planning and Navigation | ⏳ Pending | — | — |
| 7 | Object Detection and Recognition | ⏳ Pending | — | — |
| 8 | Robot Learning and Behavior Classification | ⏳ Pending | — | — |
| 9 | Localization and Mapping | ⏳ Pending | — | — |
| 10 | ROS and Integration | ⏳ Pending | — | — |
| 11 | Human-Robot Interaction | ⏳ Pending | — | — |
| 12 | Autonomous Systems and Decision Making | ⏳ Pending | — | — |
| 13 | Robot Manipulation and Grasping | ⏳ Pending | — | — |
| 14 | Course Review and Modern Trends | ⏳ Pending | — | — |
| 15 | Final Project (Part 1) | ⏳ Pending | — | — |
| 16 | Final Project Submission | ⏳ Pending | — | — |

---

## 💼 Career Context — Why This Course Matters

**AI is now a core capability across nearly every industry** — healthcare, manufacturing, energy, logistics, finance, retail, government, and education. This course builds toward the **Associate of Applied Science (AAS) in Artificial Intelligence & Robotics**, an applied workforce degree for entry-level and early-career AI roles.

### **Entry-Level Job Roles This Course Supports**
- AI Technician / AI Systems Specialist
- Applied AI or Junior AI Developer
- Machine Learning or Computer Vision Technician
- Automation & Intelligent Systems Specialist
- AI Operations (AIOps) Associate
- Healthcare AI Systems Support Specialist
- Manufacturing AI / Smart Factory Technician
- Logistics & Supply Chain AI Analyst

### **Wages & Career Growth**
| Level | Salary Range |
|---|---|
| Entry-level | $65,000–$90,000 annually |
| Mid-career applied AI | $90,000–$140,000+ |
| Hourly technical roles | $35–$75/hour |

**Industry Shift:** The workforce is moving from traditional software-only roles toward AI-enabled professionals who can deploy, operate, and responsibly use AI systems in real-time.

---

## 🎓 Instructor & Contact Information

**Sitaram Ayyagari**
📧 sitaram.ayyagari@hccs.edu (via Canvas Inbox preferred)
📅 Response time: ~48 hours for email and grading

**Background:** Bachelor's in Electronics and Communications, Master's in Electronic Instrumentation, MBA in Global Management. Career includes IBM (TISL), SHV Energy, NCR Corporation, HCL Corp, Dresser-Rand, Siemens, Atos — spanning product development, project management, and program management, with experience in business applications, dashboards, AI products, and chatbots.

**Department Chair (for escalated concerns):**
Liene Joshua Lo — liene.lo@hccs.edu | 713-718-2279 | Office: C.152

---

## 📌 Important Course Policies Recap

- **Grading:** A (90%+), B (80-89%), C (70-79%), D (60-69%), F (<60%)
- **Weight breakdown:** Written Assignments (15%), Exams/Quizzes (40%), In-Class Activities (25%), Final Exam (20%), Extra Credit (2%)
- **Time commitment:** Expect at least 2x hours outside class studying/completing assignments as time spent in class
- **AI Use:** Permitted for documentation/portfolio only — **not** for lab questions or journals
- **Academic Integrity:** Per HCC Student Procedures — see HCC Student Handbook

---

## 🚀 What You'll Build

By the end of this course, you'll have:

✅ Hands-on experience with ROS, Gazebo, OpenCV, and ML frameworks
✅ Sensor processing and perception pipelines
✅ Object detection and recognition systems
✅ Path planning and SLAM implementations
✅ A complete end-to-end autonomous or interactive robotic system
✅ A professional GitHub portfolio documenting your robotics journey
✅ Critical understanding of ethics, safety, and societal impact in robotics

---

## 🔗 Navigation

- [← Back to Portfolio Home](../../PORTFOLIO_README_FINAL.md)
- [Computer Vision Course](../Computer_Vision/README.md)
- [Machine Learning Course](../Machine_Learning/ML_README.md)
- [Natural Language Processing Course](../Natural_Language_Processing/NLP_README.md)

---

**Welcome to Robotics and Autonomous Systems!** 🤖

From sensors and perception to kinematics, control, SLAM, and human-robot interaction — this course brings together everything from your AI journey into physical, embodied systems. Let's build something that moves in the real world.

---

*Status: Course Introduction Ready | Modules Pending | Final Project To Be Defined*
