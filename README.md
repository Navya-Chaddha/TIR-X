#  TIR-X: Light-Controlled Dino Game

An interactive endless runner inspired by the Chrome Dino Game, powered by physics and designed to be controlled using optical signals.

Overview

TIR-X is a fusion of **physics, electronics, and game development**.
Instead of traditional keyboard input, this project is designed to use **light intensity variations transmitted through optical fiber** to control gameplay.
The system demonstrates real-world concepts like **Total Internal Reflection (TIR)** and **optical signal attenuation** in a fun, interactive way.

Core Concept

Light from a laser travels through an optical fiber and reaches a sensor.
When the fiber is bent or disturbed, light intensity changes due to loss of total internal reflection.
These variations are mapped to game controls:

* 🟢 High intensity → Run
* 🟡 Medium intensity → Jump
* 🔴 Low intensity → Duck

Game Features

* Endless runner gameplay
* Smooth jump physics
* Functional duck mechanic
* Random obstacle generation
* Collision detection
* Score tracking
* Increasing difficulty over time
* Clean and minimal UI

## Tech Stack

* Python
* Pygame
* (Planned) ESP32 + Optical Fiber Hardware
* (Planned) Serial Communication using PySerial

---

## 🛠️ How to Run

### 1. Clone the repository

```bash
git clone https://github.com/your-username/TIR-X.git
cd TIR-X
```

### 2. Install dependencies

```bash
pip install pygame pyserial
```

### 3. Run the game

```bash
python main.py
```
##  Current Controls (Without Hardware)

* SPACE → Jump
* DOWN ARROW → Duck

---

##  Future Integration

This project is designed to integrate with a hardware system:

* Laser diode (light source)
* Optical fiber (transmission medium)
* Photodiode/LDR (receiver)
* ESP32 (signal processing)

The ESP32 will send real-time sensor values to control the game via serial communication.

##  Physics Behind the Project

* Total Internal Reflection (TIR)
* Optical signal attenuation
* Fiber bending loss
* Light-to-electrical signal conversion

##  Vision

To demonstrate how **real-world optical communication systems** can be used as interactive control interfaces, bridging the gap between **engineering concepts and user experience**.

## Contributions

Open to ideas, improvements, and feature additions!

## If you like this project
Give it a star and share it 🚀
