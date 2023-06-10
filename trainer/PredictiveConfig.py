import numpy as np


class PredictiveConfig:
    NX = 4  # x = x, y, v, yaw
    NU = 2  # a = [accel, steer]
    T = 5  # Horizon length

    # Mpc parameters
    R = np.diag([0.01, 0.01])  # Input cost matrix
    Rd = np.diag([0.01, 1.0])  # Input difference cost matrix
    Q = np.diag([1.0, 1.0, 0.5, 0.5])  # State cost matrix
    Qf = Q  # State final matrix
    GOAL_DIS = 1.5  # Goal distance
    STOP_SPEED = 0.5 / 3.6  # Stop speed
    MAX_TIME = 500.0  # Max simulation time

    # Iterative parameters
    MAX_ITER = 3  # Max iteration
    DU_TH = 0.1  # Iteration finish param

    TARGET_SPEED = 10.0 / 3.6  # [m/s] Target speed
    N_IND_SEARCH = 10  # Search index number

    DT = 0.2  # [s] Time tick

    # Vehicle parameters
    WB = 2.5  # [m]

    MAX_STEER = np.deg2rad(45.0)  # Maximum steering angle [rad]
    MAX_DSTEER = np.deg2rad(30.0)  # Maximum steering speed [rad/s]
    MAX_SPEED = 55.0 / 3.6  # Maximum speed [m/s]
    MIN_SPEED = -20.0 / 3.6  # Minimum speed [m/s]
    MAX_ACCEL = 1.0  # Maximum accel [m/ss]
