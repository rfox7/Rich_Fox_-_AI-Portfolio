# Module 00 — Approved Curriculum: Robotics Systems and Applications

**Course:** ITAI 2374 — Robotics Systems and Applications
**Document Type:** Official Approved Curriculum (Reference)

---

## 📋 Overview

This document captures the official approved curriculum for ITAI 2374, serving as the authoritative reference for course objectives, learning outcomes, module structure, assessment weights, and recommended resources. Use this alongside the syllabus README for the complete picture of course expectations.

---

## 📖 Course Description

This intermediate course explores the principles, methods, and applications of robotics systems and their integration in artificial intelligence and autonomous technologies. Students will investigate how robots perceive, plan, and interact with their environment through various sensors, actuators, and control systems. Emphasis is placed on both foundational concepts and practical skills, with hands-on experience using contemporary tools and real-world robotic platforms. The course highlights ethical considerations and the evolving role of robotics technologies in AI-driven systems.

**Prerequisites:** MATH 1314, ITAI 1370, ITAI 1371, ITAI 1372, ITAI 1378, ITSC 1316

---

## 🎯 Course Objectives

By the end of this course, students will be able to:

1. **Summarize** the historical evolution, foundational concepts, and industrial impact of robotics and autonomous systems
2. **Differentiate** among classic robotics algorithms, control techniques, and their appropriate use cases in AI and automation
3. **Apply** classic machine-learning methods to construct end-to-end robotic perception and control pipelines
4. **Analyze** kinematic and dynamic features (motion, sensing, actuation) to extract structured knowledge from robotic sensor data
5. **Evaluate** the effectiveness, safety, and ethical implications of robotic systems using quantitative metrics and critical reflection
6. **Design and create** a functional robotic application (such as an autonomous navigation system or manipulation task) that integrates sensing, planning, and control best practices

---

## 🎓 Course Specific Student Learning Outcomes (CSLOs)

By the end of this course, students will be able to:

1. Define key terminology in robotics, autonomous systems, and multimodal robotic technologies
2. Explain the robotics pipeline and its role within broader AI-automation workflows
3. Implement sensor processing, feature extraction, and classic ML classifiers using Python libraries (ROS, OpenCV, scikit-learn)
4. Interpret kinematic models, sensor data, motion planning, and control systems to gain robotic insight
5. Critique safety concerns, privacy issues, and societal impacts of robotic technologies, proposing mitigation strategies
6. Construct and present an end-to-end autonomous or interactive robotic system leveraging pre-trained perception models

---

## 🗺️ SLO Mapping to Modules

| SLO | Description | Primary Modules | Reinforced Modules |
|---|---|---|---|
| **1** | Define key terminology in robotics, autonomous systems, and multimodal robotic technologies | 1, 3, 10, 14 | Throughout course |
| **2** | Explain the robotics pipeline and its role within broader AI-automation workflows | 1, 2, 4, 12 | 3, 5–11 |
| **3** | Implement sensor processing, feature extraction, and classic ML classifiers | 2, 4, 5, 7, 8, 9, 10, 11, 13 | 6, 12 |
| **4** | Interpret kinematic models, sensor data, motion planning, and control systems | 5, 6, 7, 8, 9 | 10, 11 |
| **5** | Critique safety concerns, privacy issues, and societal impacts of robotic technologies | 10, 14 | 7, 11, 12 |
| **6** | Construct and present an end-to-end autonomous or interactive robotic system | 11, 12, 13, 15, 16 | 10, 14 |

**Key Insight:** Notice how SLOs build cumulatively — SLO 1 (terminology) is reinforced throughout the entire course, while SLO 6 (end-to-end system construction) concentrates in the later, integrative modules (11–16), reflecting a natural progression from foundational knowledge to capstone synthesis.

---

## 📚 Course Detailed Outline (Curriculum Reference)

### **Module 1: Introduction to Robotics and Autonomous Systems**
*Addresses SLOs: 1, 2*
- Course overview and expectations
- Key applications and industry use cases
- History and evolution of robotics and autonomous systems
- Introduction to the robotics pipeline
- Overview of robotic modalities (manipulation, navigation, interaction)
- Overview of robotics tools and libraries (ROS, Gazebo)
- **Lab:** Environment setup, simple robot simulation and basic control

### **Module 2: Sensors and Perception**
*Addresses SLOs: 2, 3*
- Sensor types and characteristics
- Camera systems and image processing
- LIDAR and depth sensing; Inertial measurement units (IMUs)
- Introduction to why multimodal sensing is relevant in robotics
- High-level overview of how different sensors complement each other
- Brief introduction to sensor fusion as a perception modality
- **Lab:** Sensor data collection and processing pipeline in ROS and OpenCV

### **Module 3: Introduction to Computer Vision and Image Processing**
*Addresses SLOs: 1, 2*
- Fundamentals of digital images and computer vision
- Image acquisition and preprocessing
- Feature detection and extraction: edges, corners, key points
- Image filtering and enhancement techniques
- Overview of object detection and recognition systems
- **Lab:** Loading, visualizing, and processing image data using OpenCV

### **Module 4: Robot Kinematics and Motion**
*Addresses SLOs: 2, 3*
- Forward and inverse kinematics
- Coordinate frames and transformations
- Joint space and Cartesian space representations
- Introduction to motion planning (conceptual)
- Compare kinematic representations with sensor feature representations
- **Lab:** Kinematic calculations using robotics toolboxes and visualization

### **Module 5: Actuators and Control Systems**
*Addresses SLOs: 3, 4*
- Actuator types and characteristics
- Motor control: servo, stepper, and DC motors
- Control system fundamentals: PID control
- Control challenges and system dynamics
- How sensor feedback systems provide data for control; challenges with real-world environments (noise, delays)
- **Lab:** Motor control implementation using microcontrollers and ROS

### **Module 6: Path Planning and Navigation**
*Addresses SLOs: 4*
- Introduction to path planning algorithms
  - **Grid-based planning:** A*, Dijkstra
  - **Sampling-based planning:** RRT, PRM
- Introduction to simultaneous localization and mapping (SLAM)
- Navigation in dynamic environments; obstacle avoidance and real-time planning
- **Lab:** Implementing path planning algorithms with visualization, extracting waypoints and trajectories

### **Module 7: Object Detection and Recognition**
*Addresses SLOs: 3, 4*
- Overview of object detection and recognition
- Techniques for object detection (YOLO, R-CNN)
- Applications in manipulation and navigation
- Recognition from multiple viewpoints and lighting conditions
- **Lab:** Implementing an object detection model with OpenCV, using pre-trained models

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

### **Module 9: Localization and Mapping**
*Addresses SLOs: 3, 4*
- Introduction to robot localization
- Simultaneous Localization and Mapping (SLAM)
- Applications of SLAM in robotics
- SLAM with different sensor modalities (visual, LIDAR-based)
- **Lab:** Implementing SLAM algorithms with ROS, visualizing maps and trajectories

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

### **Module 11: Human-Robot Interaction**
*Addresses SLOs: 3, 6*
- Introduction to human-robot interaction (HRI)
- Social robotics and collaborative systems
- Natural interfaces: gesture, voice, and visual interaction
- Evaluation of HRI systems
- Multi-modal interaction pipelines
- **Lab:** Using pre-trained interaction models, evaluating interaction quality

### **Module 12: Autonomous Systems and Decision Making**
*Addresses SLOs: 2, 6*
- Autonomous system architecture
- State estimation and sensor fusion
- Decision making and task planning
- Rule-based and learning-based autonomous systems
- Introduction to multi-agent systems (conceptual)
- Autonomous systems for mobile and manipulation tasks
- **Lab:** Build a rule-based or learning-based autonomous system for a robotics use case

### **Module 13: Robot Manipulation and Grasping**
*Addresses SLOs: 3, 6*
- Introduction to robot manipulation
- Grasp planning and execution
- Introduction to manipulation planning systems
- Manipulation of objects in unstructured environments
- **Lab:** Implementing grasp planning and simple manipulation with simulation and real robots

### **Module 14: Course Review and Modern Trends**
*Addresses SLOs: 1, 5*
- Review of all modules and key concepts
- Modern and multimodal robotics: vision, tactile, audio (overview)
- AI applications of multimodal robotics
- Robot learning and adaptation basics (overview)
- Responsible robotics: ethics, safety, privacy, and societal impact (summary)
- Review activities, Q&A, project troubleshooting, portfolio

### **Module 15: Final Project**
*Addresses SLOs: 6*
- Self-study class dedicated to finalizing the project

### **Module 16: Final Project Submission**
*Addresses SLOs: 6*
- Final project presentations or exam

---

## 📘 Instructional Resources

**No prescribed textbook is required** due to the rapidly evolving nature of artificial intelligence and robotics. Instructors will curate up-to-date articles, papers, videos, and other resources via Canvas to provide the latest advancements and diverse perspectives. This approach ensures flexibility to tailor content to class needs and incorporate emerging topics.

### **Supplemental Books (Optional)**

| Book | Author(s) | Recommended For Modules |
|---|---|---|
| *Springer Handbook of Robotics* (3rd ed.) | Siciliano, B., & Khatib, O. (2025) | 1, 5, 7, 9, 11, 13, 14 — comprehensive robotics techniques (kinematics, control, perception, autonomous systems) |
| *Modern Robotics: Mechanics, Planning, and Control* (2nd ed.) | Lynch, K. M., & Park, F. C. (2025) | 10, 13, 14 — robot mechanics, motion planning, control systems |
| *Robotics, Vision and Control: Fundamental Algorithms in Python* (3rd ed.) | Corke, P. (2025) | 11, 13, 16 — implementing robotics algorithms, capstone project development |
| *Programming Robots with ROS* | Quigley, M., & Gerkey, B. (2020) | 2, 5, 6, 9 — ROS programming, sensor integration, system architecture |

### **Supplemental Papers (Optional)**

| Paper | Author(s) / Year | Recommended For Modules |
|---|---|---|
| "The foundation models for robotics: A comprehensive survey" | Zhao, W., et al. (2024) | 11, 13 — advanced robotics models and autonomous systems |
| "Unleashing the transformers: Vision models enhance robot manipulation in manufacturing" | Chen, L. (2024) | 7, 8 — object detection and manipulation planning |
| "MambaBot: Linear-time sequence modeling for robot behavior learning" | Kumar, A., & Singh, P. (2024) | 11 — efficient robot learning architectures |
| "GraphSLAM: Knowledge graphs for simultaneous localization and mapping" | Boston Dynamics Research (2024) | 13, 14 — advanced SLAM in autonomous navigation and mapping |
| "Ethical considerations in autonomous robot deployment in healthcare and service industries" | Rodriguez, M., & Kim, J. (2025) | 15 — ethical frameworks in robotics applications |

---

## 🕒 Teaching Methods and Course Structure

| Detail | Value |
|---|---|
| **Total Course Duration** | 96 contact hours, 16 weeks (Regular term) |
| **Weekly Contact Time** | 6 hours |
| **Weekly Structure** | Lecture: 2–3 hours; Lab: 3–4 hours |

### **Delivery Methods / Modality**
- **Hybrid Lab:** Meets 3 hrs on campus + 3 hrs of labs on their own time
- **Online Anytime:** Fully asynchronous, completed within the term; all coursework accessible online with no set meeting times, but predefined due dates apply

---

## 📊 Assignments & Assessment Breakdown

| Category | Weight | Objective |
|---|---|---|
| **General Assignments** | 20% | Reinforce theoretical concepts and develop analytical skills through weekly assignments — case studies, research discussions, problem sets, design tasks tied to module content |
| **Labs / Hands-On Activities** | 25% | Provide practical understanding of robotics systems through guided implementation exercises, coding workshops, and interactive demonstrations using industry-standard tools/frameworks |
| **Midterm Project or Exam** | 20% | Individual or group project demonstrating integration/application of knowledge from the first half of the course — design and implement a focused robotics solution for a specific problem/use case |
| **Final Exam or Capstone Project** | 25% | Comprehensive hands-on experience creating a practical, real-world application — integrate multiple robotics techniques into an end-to-end solution with documentation and presentation |
| **Course Portfolio** | 10% | Individual dynamic document continuously updated on GitHub — a comprehensive record of learning progress, code repositories, reflections, and achievements demonstrating professional development and technical growth |

**Total:** 100%

**Key Insight:** The Course Portfolio (10%) is explicitly a **GitHub-based, continuously updated** deliverable — this validates using GitHub documentation as an ongoing companion throughout the course, not just a final submission.

---

## 📅 Summary Course Outline (16-Week Calendar)

| Week | Module | Topic | Assignment Due |
|---|---|---|---|
| 1 | Mod 1 | Introduction to Robotics and Autonomous Systems | — |
| 2 | Mod 2 | Sensors and Perception | — |
| 3 | Mod 3 | Introduction to Computer Vision and Image Processing | — |
| 4 | Mod 4 | Robot Kinematics and Motion | — |
| 5 | Mod 5 | Actuators and Control Systems | — |
| 6 | Mod 6 | Path Planning and Navigation | — |
| 7 | Mod 7 | Object Detection and Recognition | — |
| 8 | Mod 8 | Robot Learning and Behavior Classification | — |
| 9 | Mod 9 | Localization and Mapping | **Midterm Project Due** |
| 10 | Mod 10 | Robot Operating System (ROS) and Integration | — |
| 11 | Mod 11 | Human-Robot Interaction | — |
| 12 | Mod 12 | Autonomous Systems and Decision Making | — |
| 13 | Mod 13 | Robot Manipulation and Grasping | — |
| 14 | Mod 14 | Course Review & Modern Trends, Responsible Robotics | — |
| 15 | Mod 15 | Final Project Work | — |
| 16 | Mod 16 | Final Exam / Project Submission | **Final Project Submission** |

### **Alternate 12-Week Compressed Calendar**

| Week | Module(s) | Combined Topic | Assignment Due |
|---|---|---|---|
| 1 | Mod 01 | Introduction to Robotics and Autonomous Systems | — |
| 2 | Mod 02 | Sensors and Perception | — |
| 3 | Mod 03 | Introduction to Computer Vision and Image Processing | — |
| 4 | Mod 04 & 05 | Robot Kinematics & Motion + Actuators and Control Systems | — |
| 5 | Mod 06 | Path Planning and Navigation | — |
| 6 | Mod 07 & 08 | Object Detection & Recognition + Robot Learning (Behavior Classification) | — |
| 7 | Mod 09 | Localization and Mapping (SLAM) | **Midterm Project Due** |
| 8 | Mod 10 | Robot Operating System (ROS 2) and Integration | — |
| 9 | Mod 11 | Human-Robot Interaction (HRI) & Safety | — |
| 10 | Mod 12 | Robot Manipulation and Grasping | — |
| 11 | Mod 13 & 14 | Autonomous Systems & Decision Making + Responsible/Trustworthy Robotics | — |
| 12 | Mod 15 & 16 | Course Review & Modern Trends; Final Demos/Exam | **Final Project Submission / Final Exam** |

*Note: Your specific section (SS 2026, Section 7) follows the 16-week Monday evening hybrid schedule per the syllabus — the 12-week version applies to accelerated/compressed terms.*

---

## 🎓 Key Takeaways

✅ **Six overarching course objectives** progress from historical/conceptual understanding → algorithm differentiation → applied ML pipelines → kinematic analysis → ethical evaluation → full system design

✅ **Six CSLOs** map cumulatively across modules, with foundational SLOs (terminology, pipeline understanding) reinforced throughout, and integrative SLOs (end-to-end system construction) concentrated in later modules

✅ **No fixed textbook** — resources are curated and current, reflecting the fast-moving nature of robotics/AI; several excellent optional supplemental texts and papers are available per module cluster

✅ **Assessment is heavily practical:** 45% of the grade comes from Labs (25%) + Portfolio (10%) + hands-on components of projects — reflecting the course's emphasis on applied skill-building over pure theory

✅ **The GitHub portfolio (10%) is a continuous, dynamic deliverable** — reinforcing the value of documenting progress throughout the course rather than compiling everything at the end

✅ **Path planning (Module 6) introduces specific named algorithms** — A*, Dijkstra (grid-based), RRT, PRM (sampling-based) — worth flagging for focused study

---

*[← Back to Robot Operating System & Platform](../ROS_Platform_README.md) | [← Back to Portfolio Home](../../PORTFOLIO_README_FINAL.md)*
