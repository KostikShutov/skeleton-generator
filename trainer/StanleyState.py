import numpy as np
from trainer.StanleyHelper import StanleyHelper


class StanleyState(object):
    def __init__(self, stanleyHelper: StanleyHelper, x=0.0, y=0.0, yaw=0.0, v=0.0) -> None:
        super(StanleyState, self).__init__()
        self.stanleyHelper = stanleyHelper
        self.x = x
        self.y = y
        self.yaw = yaw
        self.v = v
        self.steering = None

    def update(self, acceleration, delta):
        delta = np.clip(delta, -self.stanleyHelper.MAX_STEER_IN_RADIANS, self.stanleyHelper.MAX_STEER_IN_RADIANS)

        self.steering = delta
        self.x += self.v * np.cos(self.yaw) * self.stanleyHelper.DT
        self.y += self.v * np.sin(self.yaw) * self.stanleyHelper.DT
        self.yaw += self.v / self.stanleyHelper.L * np.tan(delta) * self.stanleyHelper.DT
        self.yaw = self.stanleyHelper.normalize_angle(self.yaw)
        self.v += acceleration * self.stanleyHelper.DT
