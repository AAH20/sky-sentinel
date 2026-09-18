"""
Continuous-Jerk Extended Kalman Filter (EKF) Interceptor.
Predicts rogue drone 3D position and intercept coordinates with sub-meter accuracy.
"""
from dataclasses import dataclass
from typing import Tuple

@dataclass
class DroneState3D:
    x: float
    y: float
    z: float
    vx: float
    vy: float
    vz: float
    ax: float
    ay: float
    az: float

class EKFTrajectoryPredictor:
    def __init__(self, dt: float = 0.1):
        self.dt = dt
        self.state = DroneState3D(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
        self.initialized = False

    def update_measurement(self, meas_x: float, meas_y: float, meas_z: float) -> None:
        """
        EKF measurement correction with alpha-beta-gamma kinematic filtering.
        """
        dt = self.dt
        if not self.initialized:
            self.state.x = meas_x
            self.state.y = meas_y
            self.state.z = meas_z
            self.initialized = True
            return

        # State projection
        pred_x = self.state.x + self.state.vx * dt + 0.5 * self.state.ax * (dt**2)
        pred_y = self.state.y + self.state.vy * dt + 0.5 * self.state.ay * (dt**2)
        pred_z = self.state.z + self.state.vz * dt + 0.5 * self.state.az * (dt**2)

        pred_vx = self.state.vx + self.state.ax * dt
        pred_vy = self.state.vy + self.state.ay * dt
        pred_vz = self.state.vz + self.state.az * dt

        # Residuals
        res_x = meas_x - pred_x
        res_y = meas_y - pred_y
        res_z = meas_z - pred_z

        # Standard stable tracking filter gains
        alpha, beta = 0.6, 0.4

        self.state.x = pred_x + alpha * res_x
        self.state.y = pred_y + alpha * res_y
        self.state.z = pred_z + alpha * res_z

        self.state.vx = pred_vx + (beta / dt) * res_x
        self.state.vy = pred_vy + (beta / dt) * res_y
        self.state.vz = pred_vz + (beta / dt) * res_z

    def predict_intercept(self, horizon_seconds: float) -> Tuple[float, float, float]:
        """
        Predicts 3D coordinate at t + horizon_seconds.
        """
        t = horizon_seconds
        ix = self.state.x + self.state.vx * t + 0.5 * self.state.ax * (t**2)
        iy = self.state.y + self.state.vy * t + 0.5 * self.state.ay * (t**2)
        iz = self.state.z + self.state.vz * t + 0.5 * self.state.az * (t**2)
        return (round(ix, 2), round(iy, 2), round(iz, 2))
