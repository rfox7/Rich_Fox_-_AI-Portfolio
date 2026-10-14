# Module 01 — Introduction to Robotics & Autonomous Systems

**Course:** ITAI 2374 — Robotics Systems and Applications
**Instructor:** Sitaram Ayyagari
**Platform:** PiDog (quadruped robot platform used throughout the term)

---

## 📋 Overview

Module 1 introduces the foundational concepts of robotics and autonomous systems — what robotics is, why and where robotic systems are used, the core sense-perceive-act framework, and an overview of the sensors, actuators, planning, and control concepts that will recur throughout the course. The module introduces **PiDog**, a quadruped robot platform, as the running example that will be used for hands-on labs this term.

---

## 🎯 Course Overview & Expectations

**What This Course Covers:**
Robots that **sense → plan → act**

**Weekly Rhythm:**
- Lecture + lab
- Portfolio maintained on GitHub

**Deliverables:**
- Assignments, labs, midterm, final project/exam

**Also Emphasized:**
- Professional conduct & safety mindset

---

## 🤖 What Is Robotics?

### **Origin of the Term**
- The term "robotics" traces back to **1920**, when Czech writer **Karel Čapek** used "robot" in his play *"Rossum's Universal Robot"* (R.U.R.)
- **Isaac Asimov** first used the term "robotics" in print in **1941** in a work of fiction
- Asimov introduced the **Three Laws of Robotics**, still considered highly relevant today:
  1. A robot may not injure a human being or, through inaction, allow a human being to come to harm
  2. A robot must obey orders given by human beings, except where such orders conflict with the First Law
  3. A robot must protect its own existence, as long as such protection doesn't conflict with the First or Second Law

### **Working Definition**
Robotics deals with the development of **autonomous mechatronic machines** — a system capable of **"carrying out a complex series of actions automatically"** (Wikipedia).

### **Robotics vs. Mechatronics**
- Robotics is a **subset of mechatronics**, with some level of **autonomy**
- All robotic systems are mechatronic systems, but **not all mechatronic systems are robotic systems**
- Robots are traditionally considered systems that can **sense, think, act, and communicate** — including some level of mechanics, sensing, control, intelligence, or autonomy

### **Form Factors**
Robots come in a wide variety of forms:
- Humanoid
- Industrial
- Bio-inspired soft robots

---

## 🔧 What Is Mechatronics?

**Definition:** "Systems showing a combination of mechanical and electrical engineering disciplines for the development of industrial automation"

### **The Disciplines Involved**
Mechatronics combines:
- **Mechanical Engineering**
- **Electrical Engineering**
- **Information Engineering**
- **Computer Science**
- **Control Theory**

**Range of Complexity:** Mechatronic systems range from simple (a blender or toaster) to advanced (industrial robotics). We are surrounded by mechatronic systems in daily life.

**Key Relationship:** Robotics = an autonomous mechatronic system (robotics sits *within* the broader field of mechatronics, distinguished by its degree of autonomy).

---

## 🌍 Why & Where Robotic Systems Are Used

### **Deployment Contexts**
- **Dangerous tasks** — nuclear facilities, outer space
- **Tasks requiring high precision, fast computation**
- **Tasks requiring continuous monitoring**
- **Industry sectors:** Manufacturing, logistics, healthcare, energy, service, agriculture/inspection

### **Common Goals**
Safety, repeatability, speed, cost, data capture

### **Real-World Constraints**
Power, compute, communications, environmental conditions

### **Example Application Categories**
- Industrial robotics (e.g., robotic arms)
- Radio-controlled aerial drones
- Modern cars (self-driving)
- Robotic exoskeletons
- Humanoid robots
- Disaster recovery robots

---

## 🔄 The Robotics Pipeline

**Core Pipeline:**
```
Perception → State Estimation → Planning → Control → Execution
```

**Key Infrastructure:**
- Data flows via **middleware** (e.g., ROS 2 nodes/topics/services)
- **Evaluation loop:** logs, metrics, safety checks

This pipeline will recur throughout the course — later modules dive deeper into each stage (perception in Modules 2-3 and 7, planning in Module 6, control in Module 5, and the ROS middleware itself in Module 10).

---

## 🏗️ Robotic Systems Design — The Environment

Every robotic system is **situated in an environment** and interacts with it in some way.

**The environment:**
- **Defines the problem** the robot must solve
- **Imposes conditions/constraints** on the system design

**Environmental factors:**
- Material properties
- Terrain
- Morphology (shape/structure)

**Examples of environments:** field, kitchen, factory

**Key Insight:** The environment determines both the constraints on design AND the goal of the system — to cause impact or interaction with the environment in some manner.

---

## 🔁 Sense-Perceive-Act Model

The fundamental framework for understanding how robots interact with their environment.

### **The Three Stages**

**1. Sense**
- A set of sensors estimates the state of the system
- Determines what modifications are needed and provides understanding of the environment

**2. Perceive**
- An algorithm interprets sensor input to determine what action to take
- Often runs on an embedded system (microcontroller or microprocessor)

**3. Act**
- The perception algorithm determines how to affect the environment through **actuators**
- Actuators receive signals from the microcontroller and physically alter the environment

### **Open Loop vs. Closed Loop Control**

| Type | Description |
|---|---|
| **Open Loop** | The control loop happens once — actuation occurs with no feedback |
| **Closed Loop** | The system iterates the control loop repeatedly, using feedback from the output |

---

## 🐕 Sense-Perceive-Act Model — PiDog Example

Applying the framework to a walking quadruped robot:

**Scenario:** PiDog wants to walk forward toward a goal while avoiding obstacles.

| Stage | PiDog Implementation |
|---|---|
| **Sense** | Imaging (camera), Accelerometer — understand both the robot itself (speed/position) and the environment (obstacle locations) |
| **Perceive** | Determine position from sensor data; determine location of obstacles in the environment |
| **Act** | Actuate leg servos to avoid obstacles / walk forward |

**Closed Loop:** The action leads to changes in the environment, so the loop begins again — this makes PiDog a **closed loop system**.

**Key Takeaway:** The sense-perceive-act framework is a useful method for understanding and designing robotic systems generally, not just PiDog specifically.

---

## 📡 Sensors at a Glance

**Core sensor types covered:** Cameras (RGB/Depth), LiDAR, IMU, encoders, tactile, GPS

**Universal trade-offs across all sensors:** range, resolution, latency, cost

### **Encoders**
- **How it works:** Measure rotation of wheels, joints, or motors (optical or magnetic)
- **Strengths:** Precise joint/rotation feedback, low cost, robust
- **Limitations:** Slip or backlash can reduce accuracy; only local (relative) movement, not absolute position
- **Robotics uses:** Odometry (distance traveled), robotic arm joint positioning, speed control of wheels/motors

### **Tactile / Force Sensors**
- **How it works:** Detect touch, pressure, or force (force-sensitive resistors, piezo sensors, capacitive touch)
- **Strengths:** Enable robots to sense contact, grip force, textures
- **Limitations:** Usually local (only at contact point), can wear out
- **Robotics uses:** Robotic hands for grasping fragile items, collision detection, human-robot interaction safety

### **GPS (Global Positioning System)**
- **How it works:** Satellite-based system for global location
- **Strengths:** Absolute positioning outdoors, widely available
- **Limitations:** Poor indoors, limited accuracy (1-5 m), can be degraded in urban canyons or jammed
- **Robotics uses:** Outdoor navigation (drones, autonomous cars, agricultural robots), geo-fencing, waypoint following

**Discussion Prompt from Slides:** *"What happens if we only use this sensor? What gaps remain?"* — this ties back to **sensor fusion**: why robots almost always combine multiple sensors rather than relying on just one.

### **Complete Sensor Comparison Table**

| Sensor | How It Works | Strengths | Limitations | Example Use |
|---|---|---|---|---|
| **Cameras (RGB/Depth)** | Capture 2D/3D images of the environment | Rich information, versatile, low cost | Sensitive to lighting/occlusion, high compute needs | Object detection, SLAM, HRI |
| **LiDAR** | Emits laser pulses, measures return time → 3D point cloud | High accuracy, day/night operation | Expensive, weather sensitive, limited color info | Self-driving cars, warehouse mapping |
| **IMU** | Accelerometers + gyros (sometimes magnetometers) | Fast, lightweight, works indoors | Drift over time, cumulative errors | Drone stabilization, dead reckoning |
| **Encoders** | Measure rotation of wheels/joints (optical/magnetic) | Precise, low cost, robust | Affected by slip/backlash, local only | Odometry, arm joint positioning |
| **Tactile / Force** | Detect touch, pressure, or force | Enables grasping, safety, texture sensing | Local contact only, sensor wear | Grippers, collision detection, HRI |
| **GPS** | Triangulates signals from satellites | Absolute global position outdoors | Poor indoors, 1-5 m accuracy, jamming | Outdoor navigation, drones, agriculture |

---

## ⚙️ Actuators & Mechanisms

**Core types covered:** DC/BLDC/servo/stepper motors, grippers, wheels, legs

**Key Principle:** Mechanical design affects control difficulty.

**Conceptual split:**
- **Motors** → movement units (DC, BLDC, servo, stepper)
- **Mechanisms** → embodiment (grippers to manipulate, wheels/legs to move through environment)

### **DC Motors (Direct Current)**
- **How it works:** Continuous rotation with variable speed controlled by voltage or PWM
- **Strengths:** Simple, inexpensive, widely available
- **Limitations:** Low precision unless combined with encoders
- **Robotics uses:** Drive wheels on small robots, conveyor belts, fans
- **Analogy:** Like a fan — plug it in, it spins; more voltage = faster
- **Behavior:** Just keeps spinning until power is cut; control is via voltage (speed) and polarity (direction)

### **Servo Motors**
- **How it works:** DC motor + feedback + control electronics → precise position or angle control
- **Strengths:** Easy to command angles (e.g., 0-180°), widely supported, reliable
- **Limitations:** Limited range of motion, torque depends on size
- **Robotics uses:** Robotic arms, grippers, camera pan-tilt systems, leg joints
- **Analogy:** Like your arm — if you tell your elbow "bend to 90°," it moves there and holds
- **Key Difference from DC Motor:** A motor alone = raw power (spins when powered); a servo = controlled motion (knows where it is, goes to a commanded angle)

**PiDog's Three Servo Types:**

| Servo | Function |
|---|---|
| **Leg Servos** | Control each leg's hip and knee joints to produce a walking gait; coordinated movement lets PiDog walk, turn, sit, and stand |
| **Head Servo** | Moves PiDog's head (and camera) side to side and up/down — lets the robot "look around" without repositioning its whole body |
| **Tail Servo** | Wags to express PiDog's mood, like a real dog — adds personality beyond pure function |

**Analogy:** Leg servos = PiDog's equivalent of a car's wheels and steering (they actually move the robot). Head servo = neck muscles; tail servo = expressive wag. All are **position-control servos**, not continuous-rotation motors.

### **Stepper Motors**
- **How it works:** Rotates in fixed angular steps (open-loop, no feedback needed)
- **Strengths:** Precise, repeatable positioning without an encoder (for light loads)
- **Limitations:** Can lose steps under heavy load (no correction if open-loop)
- **Robotics uses:** 3D printers, CNC machines, low-cost robot arms

### **Grippers**
- **Types:** Parallel jaw (pinch), suction, magnetic, adaptive (soft robotics)
- **Strengths:** Allow interaction with the environment; can be task-specific
- **Limitations:** Limited dexterity compared to a human hand; force control is critical
- **Robotics uses:** Pick-and-place robots, warehouse automation, surgical robotics

### **Wheels**
- **Types:** Standard fixed wheels, caster wheels, omni wheels, mecanum wheels
- **Strengths:** Efficient for flat surfaces, simple kinematics
- **Limitations:** Poor on rough terrain, can't handle stairs
- **Robotics uses:** Mobile service robots, warehouse AGVs, delivery robots
- **Note:** PiDog does not use wheels — included here for comparison

### **Legs**
- **Designs:** Bipeds, quadrupeds, hexapods
- **Strengths:** Excellent mobility over uneven terrain; can step over obstacles
- **Limitations:** Mechanically complex, energy expensive, harder to control
- **Robotics uses:** Boston Dynamics Spot, humanoid robots, exploration robots — **and PiDog, our quadruped platform this term**

### **Complete Actuators & Mechanisms Comparison Table**

| Type | How It Works | Strengths | Limitations | Example Use |
|---|---|---|---|---|
| **DC Motor** | Rotates continuously; speed controlled by voltage/PWM | Simple, cheap, widely available | Low precision without encoder | Small robot wheels, fans, conveyors |
| **BLDC Motor** | Brushless, electronically commutated | Efficient, high torque-to-weight, long lifespan | Needs controller, more expensive | Drones, high-performance arms |
| **Servo Motor** | DC motor + feedback for angle control | Easy position control, reliable | Limited angle range, torque depends on size | Camera pan-tilt, robot arms, grippers |
| **Stepper Motor** | Moves in discrete steps (open-loop) | Precise, repeatable, no encoder needed (light loads) | Can skip steps under load, lower efficiency | 3D printers, CNC machines, low-cost arms |
| **Grippers** | Mechanical jaws, suction, magnetic, or soft actuators | Enables object manipulation | Limited dexterity, grip strength issues | Pick-and-place, warehouse robots |
| **Wheels** | Rolling contact (fixed, caster, omni, mecanum) | Efficient, simple control on flat surfaces | Poor on rough terrain, stairs impossible | Warehouse AGVs, delivery robots |
| **Legs** | Articulated linkages for stepping | Handles rough terrain, stairs, adaptable | Complex, costly, high energy | Spot (Boston Dynamics), humanoid robots |

---

## 🗺️ Planning & Control

**Two Core Areas:**
- **Motion planning:** graph-based (A*, D*), sampling-based (RRT, PRM)
- **Control basics:** PID and feedback from sensors

### **Motion Planning — Graph-Based (A*, D*)**

**Concept:** The environment is discretized (grid/graph); pathfinding = finding the shortest route.

**A\* (A-star):**
- Uses a heuristic (e.g., Euclidean distance) to guide search
- Finds the **optimal path** (if the heuristic is admissible)
- Faster than Dijkstra on large maps

**D\* (Dynamic A*):**
- Extension of A* for dynamic/partially known environments
- Efficiently replans when obstacles or map updates appear

**Strengths:** Optimal, predictable, good for 2D maps
**Limitations:** Not scalable for high-dimensional spaces (e.g., robot arms)

### **Motion Planning Comparison Table**

| Algorithm | Type | Strengths | Limitations | Use Case |
|---|---|---|---|---|
| **A\*** | Graph-based | Optimal (if heuristic valid), efficient on grids | Not good for high-dim spaces | Mobile robot navigation on maps |
| **D\*** | Graph-based | Dynamic replanning, handles map updates | More complex than A* | Self-driving cars in changing environments |
| **RRT** | Sampling-based | Handles high-dim spaces, quick exploration | Non-optimal, may be jagged | Robotic arm motion in clutter |
| **PRM** | Sampling-based | Good for multiple queries, scalable | Preprocessing cost, not real-time | Multi-goal planning in static maps |

*(Note: RRT and PRM are covered in more depth in Module 6 — Path Planning and Navigation)*

### **Control Basics: PID + Feedback**

**Open vs. Closed Loop**

| Type | Description | Example |
|---|---|---|
| **Open Loop** | Command sent, no feedback | A toaster |
| **Closed Loop** | Sensors measure output → controller adjusts input | A thermostat |

**PID Control — Three Components**

| Component | Function |
|---|---|
| **Proportional (P)** | Corrects error magnitude — bigger error → bigger correction |
| **Integral (I)** | Corrects cumulative bias/drift — eliminates steady-state error |
| **Derivative (D)** | Reacts to rate of change — smooths response, reduces overshoot |

**Combined**, PID control is widely used in robotics for motors, arms, and drones.

**Intuitive Analogy — Cruise Control in a Car:**
- **P:** Push harder if far below target speed
- **I:** Adjust if you've been off-target for a long time
- **D:** Anticipate changes (like approaching a hill)

**⚠️ Tuning Is Critical:**
- Too much **P** → oscillation
- Too much **I** → lag/overshoot
- Too much **D** → noise sensitivity

### **Open vs. Closed Loop (PID) Comparison Table**

| Type | How It Works | Strengths | Limitations | Examples |
|---|---|---|---|---|
| **Open Loop** | No feedback, fixed commands | Simple, cheap | No correction for errors | Basic timed motors, appliances |
| **Closed Loop (PID)** | Adjusts using sensor feedback | Accurate, stable, widely used | Needs tuning, sensitive to noise | Robot arm joints, drones, vehicle speed |

---

## 🖥️ Simulation First

**Why Simulate:** Safe, fast iteration, reproducible

**Key Tools:** Gazebo/Ignition + ROS 2 = rapid pipeline prototyping

### **Why Simulate in Robotics? (Four Key Reasons)**

**1. Safety**
- Test new algorithms without risking expensive hardware or unsafe movements
- Example: tune a drone controller in simulation → avoid real-world crashes

**2. Fast Iteration**
- Reset environments instantly — no need to rebuild hardware or recharge batteries
- Run experiments at faster-than-real-time speeds

**3. Reproducibility**
- Same initial conditions every time → fair comparison of algorithms
- Enables debugging with consistent inputs (e.g., replay logs, identical sensor noise)

**4. Cost Efficiency**
- No wear-and-tear on motors, sensors, or batteries
- Scale up to many "virtual robots" cheaply in the cloud

### **Gazebo / Ignition Simulator**

- Open-source 3D robotics simulator with a physics engine
- Models robots, environments, and realistic sensors (cameras, LiDAR, IMU, GPS)
- Newer versions are branded **Ignition** (also called Gazebo "Fortress"/"Garden")

### **Integration with ROS 2**

- ROS 2 nodes connect directly to simulated robots (publish/subscribe to topics)
- **Same APIs work in simulation and on real hardware** → "code once, run anywhere"
- Can test perception (camera/LiDAR topics), planning (pathfinding), and control (cmd_vel to motors) entirely in simulation

### **Rapid Pipeline Prototyping**

- Prototype the sense → plan → act pipeline in Gazebo/ROS 2 before deploying on a physical robot
- Example: test a SLAM algorithm in a virtual warehouse → deploy to a TurtleBot or PiDog
- **Iterative workflow:** develop → simulate → refine → deploy

---

## 🛠️ Tooling & Workflow

- ROS 2 workspace, packages, nodes; bagging data
- **Version control & course portfolio:** document every lab

---

## ⚖️ Safety, Ethics, and Responsibility

- Design for **fail-safe behavior**, guarded motion, human factors
- **Privacy, data governance, misuse prevention**

*(This theme is revisited in depth in Module 10 — ethical considerations and safety in robotic systems — and Module 14 — responsible robotics summary)*

---

## 🎯 What You'll Build This Term

**Progression:** From simple sim control → perception → planning → integrated demo

**Two Milestones:**
- **Midterm scope** (narrower, focused solution)
- **Final capstone scope** (full end-to-end integrated system)

---

## 🧪 Lab 1 Preview

**Activities:** Environment check, sample sim robot, teleop + basic logging

**Exit Criteria:** "Hello, robot" pipeline runs end-to-end

---

## 🐕 PiDog: A Complex Robotic System — Full Walkthrough

PiDog serves as a complete, concrete example tying together sensing, algorithms, actuation, and power supply — the full mechatronic/robotic stack.

### **Sensing**

A legged robot relies on several sources of information to control its motion:
1. It needs to know its **own orientation and balance** while walking
2. It needs **positional information** — where obstacles are, and where sounds/people are relative to it

| Sensor | Function |
|---|---|
| **Ultrasonic Sensor** | Obstacle distance |
| **Camera** | Vision (e.g., face detection, color tracking) |
| **IMU (6-DOF)** | Balance & orientation — accelerometer + gyroscope detects tilt, falls, sharp turns during walking |
| **Touch Sensors** | Contact/petting detection |
| **Sound-Direction Sensor** | Audio localization |

**Specific roles:**
- Balance/orientation → onboard 6-DOF IMU
- Distance to obstacles → head-mounted ultrasonic sensor
- Visual context about surroundings → camera

### **Algorithm**

**Hardware:** Microcontroller = **Raspberry Pi + Robot HAT**

- The **Robot HAT** handles PWM signal generation and power management for the servos
- Sensor inputs (IMU, ultrasonic, touch, sound-direction, camera) are read over **I2C**, digital **GPIO**, or the **camera interface**

**Processing Stages (mapped to the sense-perceive-act model):**
1. **Perception phase:** Recognition algorithms (e.g., face detection) for environment understanding
2. **Planning algorithms:** Decide the next gait/action
3. **Control algorithms:** Translate decisions into servo commands → sent to the actuation phase

### **Actuation**

The Raspberry Pi (via the Robot HAT) uses servos to interact with the environment:

| Servo Group | Function |
|---|---|
| **Leg Servos** | Control hip/knee joint angles → produce PiDog's walking gait and turning motion |
| **Head/Tail Servos** | Control gaze and expressive movement |

**Gait Control Details:**
- The algorithm/microcontroller adjusts timing and angles sent to each leg servo to produce a smooth gait
- Example: PiDog may slow its gait on uneven terrain or when turning sharply
- The **Robot HAT** provides amplification and control circuitry needed to drive all **12 servos** reliably from the Raspberry Pi's GPIO/I2C signals

### **Power Supply**

Every robotic system needs a power supply enabling seamless operation of all components (microcontroller, electronics, sensors, actuators).

**PiDog's Power System:**
- Central component: **battery pack** — stores energy for walking operation
- **Challenge:** Battery depletes over time; voltage is **not stable** and varies with current flow
- **Solution needed:** Power conditioning to ensure stable (uninterruptable) operation
- The **Robot HAT includes power management** to ensure stable power supply to servos and Raspberry Pi despite falling battery voltage

---

## 🎓 Key Takeaways

✅ **Robotics is a subset of mechatronics** distinguished by autonomy — combining mechanical, electrical, computer science, and control theory disciplines

✅ **The Three Laws of Robotics** (Asimov) remain a foundational ethical touchstone, even in modern robotics discourse

✅ **The Sense-Perceive-Act model** is the fundamental framework for understanding robotic system design — and closed-loop systems (using feedback) are essential for real-world robustness

✅ **No single sensor is sufficient** — each has trade-offs (range, resolution, latency, cost), which is why robots use **sensor fusion**, combining multiple sensor types

✅ **Motors provide movement, mechanisms provide embodiment** — DC motors, servos, and steppers each suit different precision/cost/complexity needs; grippers, wheels, and legs each suit different environmental interactions

✅ **PID control** (Proportional-Integral-Derivative) is the workhorse of closed-loop robotic control, requiring careful tuning to avoid oscillation, lag, or noise sensitivity

✅ **Simulation-first development** (Gazebo/Ignition + ROS 2) enables safe, fast, reproducible, cost-efficient testing before real hardware deployment — "code once, run anywhere"

✅ **PiDog integrates the full stack** — sensing (IMU, ultrasonic, camera, touch, sound), algorithm (Raspberry Pi + Robot HAT), actuation (12 servos for legs/head/tail), and power supply (battery + power conditioning) — serving as this term's hands-on hardware platform

---

## 🛠️ Technologies & Platform Referenced

| Component | Role |
|---|---|
| **PiDog** | Quadruped robot platform used throughout the course |
| **Raspberry Pi** | Onboard microcontroller/computer |
| **Robot HAT** | PWM signal generation, power management, servo driver circuitry |
| **6-DOF IMU** | Balance and orientation sensing |
| **Ultrasonic Sensor** | Obstacle distance detection |
| **ROS 2** | Robotics middleware (nodes, topics, services) |
| **Gazebo / Ignition** | 3D robotics simulator with physics engine |

---

## 🔮 Looking Ahead

- **Module 2** dives deeper into sensors and perception (camera systems, LIDAR, IMUs, sensor fusion)
- **Module 4** covers kinematics in depth
- **Module 5** expands on actuators and control systems (PID, motor control)
- **Module 6** provides full treatment of path planning algorithms (A*, D*, RRT, PRM)
- **Module 10** covers ROS architecture and integration in depth

---

*[← Back to Robot Operating System & Platform](../ROS_Platform_README.md) | [← Back to Portfolio Home](../../PORTFOLIO_README_FINAL.md)*
