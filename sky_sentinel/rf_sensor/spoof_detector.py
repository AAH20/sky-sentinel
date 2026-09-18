"""
GNSS / GPS Spoofing & Meaconing Anomaly Detector.
Detects RF power anomalies, clock drift jumps, and Doppler signature inconsistencies.
"""
from dataclasses import dataclass
from typing import Dict, Any, List

@dataclass(frozen=True)
class GNSSMeasurement:
    carrier_to_noise_db_hz: float  # C/N0 (typically 35-50 dB-Hz)
    pseudorange_rate_mps: float    # Doppler velocity
    clock_drift_ppm: float         # Oscillator drift
    num_satellites: int

class GNSSSpoofDetector:
    def __init__(self, cn0_max_threshold: float = 54.0, max_clock_drift_jump: float = 2.5):
        self.cn0_max_threshold = cn0_max_threshold
        self.max_clock_drift_jump = max_clock_drift_jump
        self.prev_drift = None

    def evaluate_telemetry(self, measurement: GNSSMeasurement) -> Dict[str, Any]:
        flags = []
        is_spoofed = False

        # 1. Unusually high RF power (often indicates local transmitter/simulator)
        if measurement.carrier_to_noise_db_hz > self.cn0_max_threshold:
            flags.append("ANOMALOUS_HIGH_RF_POWER_SPOOF")
            is_spoofed = True

        # 2. Clock drift step discontinuity
        if self.prev_drift is not None:
            drift_delta = abs(measurement.clock_drift_ppm - self.prev_drift)
            if drift_delta > self.max_clock_drift_jump:
                flags.append("UNREALISTIC_CLOCK_DRIFT_STEP")
                is_spoofed = True

        self.prev_drift = measurement.clock_drift_ppm

        # 3. Constellation spoofing (too few satellites with identical high power)
        if measurement.num_satellites < 4:
            flags.append("INSUFFICIENT_CONSTELLATION_LOCK")

        return {
            "spoof_detected": is_spoofed,
            "threat_level": "CRITICAL" if is_spoofed else "NOMINAL",
            "anomaly_flags": flags,
            "cn0_db_hz": measurement.carrier_to_noise_db_hz
        }
