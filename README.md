
# Motion‑Controlled Game Input (ESP32‑C3 + MPU6050)

![License](https://img.shields.io/github/license/darksamurai1890/gesture-game-controller)

A stable motion→keyboard game controller built with an ESP32‑C3 and an MPU6050. The device maps calibrated hand tilt into reliable Bluetooth HID keyboard events (WASD) so games receive predictable digital inputs instead of an unstable joystick HID on ESP32‑C3.

Summary
- Hardware: ESP32‑C3, MPU6050 (accelerometer, optional gyro)
- Output: Bluetooth HID (Keyboard mode) — sends WASD / other keys
- Key idea: calibrate the user’s real motion range, normalize per‑direction, apply deadzone + smoothing, and emit thresholded key events

Table of Contents
- [Demo](#demo)
- [Features](#features)
- [Hardware & BOM](#hardware--bom)
- [Wiring](#wiring)
- [Getting started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Flash / Build](#flash--build)
- [Calibration & Usage](#calibration--usage)
  - [Calibration procedure](#calibration-procedure)
  - [Mapping & thresholds](#mapping--thresholds)
- [Algorithm overview](#algorithm-overview)
- [Configuration](#configuration)
- [Troubleshooting & Tips](#troubleshooting--tips)
- [Project structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

Demo
- Add a short GIF or video here showing the device moving and a game responding.
![demo](https://github.com/user-attachments/assets/9fdc2306-7b23-4a90-a9e8-64ba587e32ff)

Features
- Calibrated, asymmetric range mapping (no fixed ±30° assumptions)
- Per‑direction normalization to [-1, +1]
- Deadzone and single‑pole low‑pass smoothing
- Thresholded digital output → keyboard key press/release
- Minimal BLE flooding and improved stability vs. joystick HID

Hardware & BOM
- 1 × ESP32‑C3 (dev board or module)
- 1 × MPU6050 (I²C accelerometer ± gyro)
- Wires, breadboard, USB cable / battery
- Optional: pull‑up resistors for I²C (4.7k), enclosure / mounting

Wiring
- Connect MPU6050 to ESP32‑C3 via I²C:
  - VCC → 3.3V
  - GND → GND
  - SDA → configurable SDA pin (example: IO4)
  - SCL → configurable SCL pin (example: IO5)
- Add 4.7k pullups on SDA/SCL if your board needs them.
- Confirm pin mappings in firmware config.

Getting started

Prerequisites
- One of: Arduino IDE with ESP32 board support, PlatformIO, or ESP‑IDF toolchain
- USB cable and permissions to flash the board
- Basic familiarity with building/flashing ESP sketches

Flash / Build (examples)
- Arduino / PlatformIO:
  1. Open the firmware folder in your environment.
  2. Select the ESP32‑C3 board.
  3. Install required libraries (MPU6050, BLE HID or their equivalents).
  4. Build and upload.
- ESP‑IDF:
  1. idf.py set-target esp32c3
  2. idf.py menuconfig (set I2C pins / BLE options)
  3. idf.py build flash monitor

Calibration & Usage

Calibration procedure
1. Power the device and keep the MPU flat for several seconds → record center.
2. Tilt to each extreme (forward, backward, left, right) and hold briefly → record min/max pitch & roll.
3. Save calibration to non‑volatile storage (done automatically by firmware).
4. Verify normalized outputs are within [-1, +1] and adjust thresholds if necessary.

Example calibration output
Pitch: -27.33 to 50.73  
Roll : -42.02 to 29.44

Mapping & thresholds
- Range‑based normalization (per direction):
  if value > 0: normalized = value / positive_max  
  else: normalized = value / abs(negative_min)
- Deadzone:
  if abs(normalized) < DEADZONE → treat as 0
- Smoothing (low‑pass):
  filtered += alpha × (new − filtered)
- Press/release logic:
  - forward_value > press_threshold → press 'W'
  - forward_value < release_threshold → release 'W'
  - Repeat for S/A/D with their axes
- Only send keyboard events on state transitions to avoid BLE flooding.

Algorithm overview
1. Read raw accelerometer (ax, ay, az)
2. Compute angles:
   - roll  = atan2(ay, az)
   - pitch = atan2(-ax, sqrt(ay² + az²))
3. Run calibration to capture per‑direction min/max
4. Normalize ranges → [-1, +1]
5. Apply deadzone and smoothing
6. Apply thresholds → keyboard HID events (press/release)

Configuration
- Example config (config.json or config.h)
```json
{
  "i2c": { "sda": 4, "scl": 5 },
  "deadzone": 0.08,
  "alpha": 0.15,
  "press_threshold": 0.6,
  "release_threshold": 0.45,
  "key_bindings": {
    "forward": "W",
    "back": "S",
    "left": "A",
    "right": "D"
  }
}
```
- Expose these in menuconfig, constants, or a JSON file depending on build system.

Troubleshooting & Tips
- BLE disconnects: ensure stable power and avoid enclosing the antenna; try different USB cables.
- Noisy readings: increase smoothing (alpha) or enlarge deadzone.
- Drift: rerun calibration; provide a quick re‑calibrate button or hold gesture.
- Game too slow: lower smoothing (increase alpha) or lower press_threshold.
- If joystick HID is required later, use a non‑C3 ESP32 variant for better stability.

Project structure (suggested)
/
├─ firmware/            # firmware source (Arduino, PlatformIO or ESP‑IDF)
│  ├─ src/
│  │  ├─ main.cpp
│  │  ├─ imu.cpp / imu.h
│  │  ├─ calibration.cpp / calibration.h
│  │  └─ ble_hid.cpp / ble_hid.h
│  └─ config.json
├─ hardware/
│  └─ wiring_diagram.svg
├─ docs/
│  └─ demo.gif
├─ README.md
└─ LICENSE

Contributing
- Fork → create a feature branch → open a PR with a clear description and testing steps.
- Add changelog entries for breaking changes.
- Please include test steps for firmware behavior (calibration, thresholds, BLE stability).

License
- MIT recommended. See LICENSE file.

Acknowledgements
- MPU6050 library authors, ESP32 BLE HID projects, and community examples for calibration & mapping approaches.

Appendix: quick tuning guide
- Deadzone: 0.05–0.12 (start 0.08)
- Alpha (smoothing): 0.1–0.25 (start 0.15)
- Press threshold: 0.5–0.7 (start 0.6)
- Release threshold: press_threshold − 0.15 (helps prevent flapping)

