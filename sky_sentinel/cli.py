"""
SkySentinel CLI: Counter-UAS Trajectory Interception & RF Forensics.
"""
import argparse
from .rf_sensor.spoof_detector import GNSSSpoofDetector, GNSSMeasurement
from .rf_sensor.signal_classifier import RFSignalClassifier
from .tracking.ekf_interceptor import EKFTrajectoryPredictor
from .forensics.airspace_dossier import AirspaceIntrusionDossier

def main():
    parser = argparse.ArgumentParser(
        prog="sky-sentinel",
        description="Autonomous Counter-UAS, RF/GPS Cyber-Physical Interceptor & Airspace Forensic Engine."
    )
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # scan-rf
    rf_p = subparsers.add_parser("scan-rf", help="Classify RF emitter protocol")
    rf_p.add_argument("--freq", type=float, default=2440.0, help="Frequency in MHz")
    rf_p.add_argument("--bw", type=float, default=20.0, help="Bandwidth in MHz")

    # detect-spoof
    subparsers.add_parser("detect-spoof", help="Evaluate GNSS telemetry for spoofing / meaconing")

    # track
    track_p = subparsers.add_parser("track", help="Simulate EKF trajectory prediction")
    track_p.add_argument("--horizon", type=float, default=2.0, help="Prediction horizon in seconds")

    args = parser.parse_args()

    if args.command == "scan-rf":
        res = RFSignalClassifier.classify_frequency(args.freq, args.bw)
        print(f"[SkySentinel] RF Classification for {args.freq} MHz:")
        print(f"  Protocol        : {res['protocol']}")
        print(f"  Threat Category : {res['threat_category']}")

    elif args.command == "detect-spoof":
        detector = GNSSSpoofDetector()
        m1 = GNSSMeasurement(carrier_to_noise_db_hz=44.0, pseudorange_rate_mps=15.0, clock_drift_ppm=0.1, num_satellites=12)
        r1 = detector.evaluate_telemetry(m1)
        print(f"[SkySentinel] Nominal GNSS: Threat={r1['threat_level']}, Flags={r1['anomaly_flags']}")

        m2 = GNSSMeasurement(carrier_to_noise_db_hz=58.5, pseudorange_rate_mps=0.0, clock_drift_ppm=3.4, num_satellites=3)
        r2 = detector.evaluate_telemetry(m2)
        print(f"[SkySentinel] Spoofed GNSS: Threat={r2['threat_level']}, Flags={r2['anomaly_flags']}")

    elif args.command == "track":
        ekf = EKFTrajectoryPredictor(dt=0.1)
        # Simulate moving drone
        for i in range(10):
            ekf.update_measurement(10.0 + i*2.0, 50.0 + i*1.5, 120.0 - i*0.5)
        pred = ekf.predict_intercept(args.horizon)
        print(f"[SkySentinel] EKF Drone State: Pos=({ekf.state.x:.1f}, {ekf.state.y:.1f}, {ekf.state.z:.1f}) | Vel=({ekf.state.vx:.1f}, {ekf.state.vy:.1f}, {ekf.state.vz:.1f})")
        print(f"[SkySentinel] Predicted Intercept at T+{args.horizon}s: {pred}")

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
