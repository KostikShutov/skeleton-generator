import math
from trainer.PredictiveConfig import PredictiveConfig


class PredictiveState:
    def __init__(self, x=0.0, y=0.0, yaw=0.0, v=0.0) -> None:
        self.x = x
        self.y = y
        self.yaw = yaw
        self.v = v

    def update(self, acceleration, steering, i=None, cx=None, cy=None):
        if steering >= PredictiveConfig.MAX_STEER:
            steering = PredictiveConfig.MAX_STEER
        elif steering <= -PredictiveConfig.MAX_STEER:
            steering = -PredictiveConfig.MAX_STEER

        if i is None:
            self.x = self.x + self.v * math.cos(self.yaw) * PredictiveConfig.DT
            self.y = self.y + self.v * math.sin(self.yaw) * PredictiveConfig.DT
        else:
            self.x = cx[i]
            self.y = cy[i]

        self.yaw = self.yaw + self.v / PredictiveConfig.WB * math.tan(steering) * PredictiveConfig.DT
        self.v = self.v + acceleration * PredictiveConfig.DT

        if self.v > PredictiveConfig.MAX_SPEED:
            self.v = PredictiveConfig.MAX_SPEED
        elif self.v < PredictiveConfig.MIN_SPEED:
            self.v = PredictiveConfig.MIN_SPEED
