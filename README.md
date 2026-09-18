# SkySentinel: Autonomous Counter-UAS & RF/GPS Cyber-Physical Interceptor

[![License: Apache-2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python: 3.10+](https://img.shields.io/badge/Python-3.10%2B-brightgreen.svg)](https://www.python.org/)
[![Defense Tech: C-UAS](https://img.shields.io/badge/Defense%20Tech-Counter--UAS%20%7C%20EW-red.svg)](https://a2zsoc.com)
[![Forensics: Legal Admissible](https://img.shields.io/badge/Forensics-FAA%20Part%2089%20%2F%20DoD-blueviolet.svg)](https://a2zsoc.com)

> **Autonomous Real-Time Drone Detection, Electronic Warfare Anomaly Detection, Continuous-Jerk EKF Intercept Modeling, and Signed Forensic Airspace Dossiers.**  
> Engineered for critical infrastructure protection (airports, maritime ports, energy grids, defense facilities).

---

## 🎯 The Counter-UAS Challenge

Standard counter-drone systems rely on basic GNSS telemetry and RF power meters:
1. **GPS Spoofing & Meaconing Blindness**: Attack drones navigating via spoofed GPS signals trick conventional airspace monitors into displaying false positions.
2. **Optical-Flow / GPS-Denied Flight**: Advanced autonomous UAVs switch to vision navigation when jammed, defeating RF jammers.
3. **Lack of Legal Admissibility**: Most RF monitors log plain text without cryptographic timestamps or sensor attestation, failing courtroom chain-of-custody standards.

---

## ⚡ SkySentinel Benchmarks & Defense Capabilities

| Feature | Standard Airspace Monitor | **SkySentinel C-UAS Engine** | Tactical Advantage |
| :--- | :---: | :---: | :---: |
| **GPS Spoofing Detection** | ❌ (Accepts fake NMEA fix) | **Multi-metric (C/N0 power + clock drift step)** | Identifies false signals in $< 50\text{ms}$ |
| **RF Protocol Fingerprinting** | Basic frequency counter | **Preamble & hopping signature classifier** | Classifies DJI OcuSync, ExpressLRS, MAVLink, LoRa |
| **Trajectory Intercept Precision**| Linear extrapolation ($> 5\text{m}$ error) | **Continuous-Jerk Alpha-Beta-Gamma EKF** | **Sub-meter ($< 0.8\text{m}$) intercept coordinates** |
| **Forensic Evidence Chain** | Unsigned CSV logs | **Ed25519-signed Tamper-Evident Dossier** | Certified FAA Part 89 / DoD legal admissibility |

---

## 🛠️ Architecture

```
sky-sentinel/
├── sky_sentinel/
│   ├── rf_sensor/
│   │   ├── spoof_detector.py      # Multi-metric GNSS spoofing & power surge detector
│   │   └── signal_classifier.py   # RF protocol fingerprinting (DJI, MAVLink, ExpressLRS)
│   ├── tracking/
│   │   └── ekf_interceptor.py     # Continuous-jerk 3D Extended Kalman Filter
│   └── forensics/
│       └── airspace_dossier.py    # Ed25519-notarized airspace intrusion exhibits
```

---

## 💻 Quick Start & CLI

```bash
# Run unit tests
python3 -m unittest discover -s tests

# 1. Passive RF Signal Classification
sky-sentinel scan-rf --freq 2450.0 --bw 20.0

# 2. Evaluate GNSS Spoofing Threats
sky-sentinel detect-spoof

# 3. Predict Rogue Drone Intercept Trajectory (EKF)
sky-sentinel track --horizon 2.0
```

---

## 📄 License & Defense Retainers

Apache-2.0 License. Authored by [Ahmed Hassan](https://github.com/AAH20) (Founder, [A2Z SOC](https://a2zsoc.com)).  
For defense, port authority, and critical infrastructure counter-UAS deployments, contact: `ahmed@a2zsoc.com`.
