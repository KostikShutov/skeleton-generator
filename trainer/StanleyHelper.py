import numpy as np


class StanleyHelper:
    K = 0.5  # control gain
    KP = 1.0  # speed proportional gain
    DT = 0.1  # [s] time difference
    L = 1  # [m] Wheelbase of vehicle
    MAX_STEER_IN_DEGREES = 45.0  # [deg] max steering angle
    MAX_STEER_IN_RADIANS = np.radians(MAX_STEER_IN_DEGREES)  # [rad] max steering angle
    TARGET_SPEED: float = 30.0 / 3.6  # [m/s]
    MAX_SIMULATION_TIME: float = 250.0

    def pid_control(self, target, current):
        return self.KP * (target - current)

    def stanley_control(self, state, cx, cy, cyaw, last_target_idx):
        current_target_idx, error_front_axle = self.calc_target_index(state, cx, cy)

        if last_target_idx >= current_target_idx:
            current_target_idx = last_target_idx

        # theta_e corrects the heading error
        theta_e = self.normalize_angle(cyaw[current_target_idx] - state.yaw)
        # theta_d corrects the cross track error
        theta_d = np.arctan2(self.K * error_front_axle, state.v)
        # Steering control
        delta = theta_e + theta_d

        return delta, current_target_idx

    def normalize_angle(self, angle):
        while angle > np.pi:
            angle -= 2.0 * np.pi

        while angle < -np.pi:
            angle += 2.0 * np.pi

        return angle

    def calc_target_index(self, state, cx, cy):
        # Calc front axle position
        fx = state.x + self.L * np.cos(state.yaw)
        fy = state.y + self.L * np.sin(state.yaw)

        # Search nearest point index
        dx = [fx - icx for icx in cx]
        dy = [fy - icy for icy in cy]
        d = np.hypot(dx, dy)
        target_idx = np.argmin(d)

        # Project RMS error onto front axle vector
        front_axle_vec = [-np.cos(state.yaw + np.pi / 2), -np.sin(state.yaw + np.pi / 2)]
        error_front_axle = np.dot([dx[target_idx], dy[target_idx]], front_axle_vec)

        return target_idx, error_front_axle
