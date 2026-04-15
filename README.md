# Real-Time Squat Counter using Computer Vision

A lightweight and efficient real-time squat detection and repetition counter built using `pose estimation` and knee angle tracking. Designed for edge devices, this system provides live feedback on workout performance.

![squat.gif](assets/squat.gif)

## How It Works

1. Pose Estimation \
Detects human keypoints (hips, knees, ankles) using a lightweight model.

2. Angle Calculation \
    Computes the knee joint angle using 3 keypoints:
    - Hip
    - Knee
    - Ankle

3. Rep Counting Logic
    - Detects downward motion (squat)
    - Detects upward motion (standing)
    - Counts one full rep per cycle

4. Posture Analysis
    - Ensures correct squat depth
    - Flags improper form (e.g., shallow squats)