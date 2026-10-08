# 🚗 AI-Based Driver Drowsiness Detection & Alert System

## 📌 Overview

The AI-Based Driver Drowsiness Detection & Alert System is a real-time computer vision project designed to detect visual signs of driver fatigue and provide timely alerts.

The system uses a camera to continuously monitor the driver and analyzes facial features such as eye closure, blinking, yawning, and head position to identify potential signs of drowsiness.

The goal is to reduce the risk of accidents caused by driver fatigue by providing an early warning when prolonged or repeated signs of drowsiness are detected.

---

## 🎯 Objectives

- Monitor the driver using a real-time camera feed.
- Detect and analyze the driver's face.
- Identify facial landmarks such as the eyes and mouth.
- Analyze eye closure and blinking patterns.
- Detect signs of yawning.
- Analyze head position and movement.
- Perform temporal analysis of driver behavior.
- Estimate the driver's drowsiness level.
- Generate an alert when significant signs of drowsiness are detected.

---

## ⚙️ System Workflow

```text
Camera
   ↓
Video Frames
   ↓
Face Detection
   ↓
Facial Landmark Detection
   ↓
┌──────────────┬──────────────┬──────────────┐
↓              ↓              ↓
Eye Analysis   Yawning        Head Pose
↓              ↓              ↓
└──────────────┬──────────────┘
               ↓
        Temporal Analysis
               ↓
       Drowsiness Analysis
               ↓
        Drowsiness Score
               ↓
       ┌───────┴───────┐
       ↓               ↓
    NORMAL           DROWSY
                       ↓
                  🚨 ALERT

 ->Key Concepts:

(*)Eye Analysis
The system analyzes the driver's eyes to identify:
- Eye opening and closing
- Blink patterns
- Prolonged eye closure
Eye-related measurements such as the Eye Aspect Ratio (EAR) will be used to analyze eye closure.
(*)Yawning Detection
The system analyzes mouth movement and opening patterns to identify possible yawning behavior.
(*) Facial Landmark Analysis
Facial landmarks are used to locate important facial regions such as:
- Eyes
- Nose
- Mouth
- Face outline
These landmarks provide the measurements required for further analysis.

->Temporal Analysis
A single frame is not enough to determine drowsiness.
The system analyzes driver behavior across multiple video frames to distinguish normal actions such as blinking from prolonged or repeated signs of drowsiness.
