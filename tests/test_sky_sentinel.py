import unittest
from sky_sentinel.rf_sensor.spoof_detector import GNSSSpoofDetector, GNSSMeasurement
from sky_sentinel.rf_sensor.signal_classifier import RFSignalClassifier
from sky_sentinel.tracking.ekf_interceptor import EKFTrajectoryPredictor
from sky_sentinel.forensics.airspace_dossier import AirspaceIntrusionDossier

class TestSkySentinel(unittest.TestCase):
    def test_gnss_spoof_detection(self):
        detector = GNSSSpoofDetector()
        nominal = GNSSMeasurement(42.0, 10.0, 0.05, 10)
        res_nom = detector.evaluate_telemetry(nominal)
        self.assertFalse(res_nom["spoof_detected"])

        spoofed = GNSSMeasurement(60.0, 0.0, 3.8, 2)
        res_spoof = detector.evaluate_telemetry(spoofed)
        self.assertTrue(res_spoof["spoof_detected"])
        self.assertEqual(res_spoof["threat_level"], "CRITICAL")

    def test_rf_classifier(self):
        dji = RFSignalClassifier.classify_frequency(2450.0, 20.0)
        self.assertEqual(dji["protocol"], "DJI_OCUSYNC_4")

        mavlink = RFSignalClassifier.classify_frequency(920.0, 0.5)
        self.assertEqual(mavlink["protocol"], "MAVLINK_TELEMETRY_SIK")

    def test_ekf_tracking_prediction(self):
        ekf = EKFTrajectoryPredictor(dt=0.1)
        # Constant velocity along X: 20 m/s (2.0m every 0.1s)
        for i in range(15):
            ekf.update_measurement(10.0 + i * 2.0, 0.0, 100.0)

        # Check velocity converged near 20 m/s
        self.assertTrue(18.0 <= ekf.state.vx <= 22.0)

        # Predict 1.0s forward: x should be approx 10 + 14*2 + 20 = 58
        ix, iy, iz = ekf.predict_intercept(1.0)
        self.assertTrue(ix > ekf.state.x)

    def test_airspace_dossier(self):
        dossier = AirspaceIntrusionDossier.generate_signed_dossier(
            target_id="UAV-ROGUE-44",
            protocol="DJI_OCUSYNC_4",
            threat_level="CRITICAL",
            coordinates_path=[{"x": 100.0, "y": 200.0, "z": 50.0}],
            rf_anomalies=["SPOOFED_BROADCAST_ID"]
        )
        self.assertEqual(dossier["admissibility"], "LEGAL_DEFENSE_GRADE")
        self.assertIn("sig_sentinel_", dossier["ed25519_signature"])

if __name__ == "__main__":
    unittest.main()
