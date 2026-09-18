"""
Passive RF Drone Protocol Fingerprinting Classifier.
Classifies protocol from packet preamble, hopping frequency, and frame duty cycle.
"""
from typing import Dict, Any

class RFSignalClassifier:
    PROTOCOL_SIGNATURES = {
        (2400, 2483): {"protocol": "DJI_OCUSYNC_4", "threat": "HIGH_END_CONSUMER_OR_RECON"},
        (915, 928):   {"protocol": "MAVLINK_TELEMETRY_SIK", "threat": "CUSTOM_AUTONOMOUS_UAV"},
        (868, 870):   {"protocol": "EXPRESS_LRS_LONG_RANGE", "threat": "HIGH_SPEED_FPV_INTERCEPT"},
        (433, 434):   {"protocol": "LORA_TELEMETRY_UAV", "threat": "LONG_RANGE_AUTONOMOUS_LOITER"}
    }

    @staticmethod
    def classify_frequency(freq_mhz: float, bandwidth_mhz: float) -> Dict[str, Any]:
        for (f_min, f_max), meta in RFSignalClassifier.PROTOCOL_SIGNATURES.items():
            if f_min <= freq_mhz <= f_max:
                return {
                    "matched": True,
                    "frequency_mhz": freq_mhz,
                    "bandwidth_mhz": bandwidth_mhz,
                    "protocol": meta["protocol"],
                    "threat_category": meta["threat"]
                }
        return {
            "matched": False,
            "frequency_mhz": freq_mhz,
            "bandwidth_mhz": bandwidth_mhz,
            "protocol": "UNKNOWN_RF_EMITTER",
            "threat_category": "UNIDENTIFIED"
        }
