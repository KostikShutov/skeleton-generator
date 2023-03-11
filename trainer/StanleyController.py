import numpy as np
from common.coordinates.Coordinate import Coordinate
from common.interpolation.InterpolateService import InterpolateService
from trainer.StanleyHelper import StanleyHelper
from trainer.StanleyState import StanleyState


class StanleyController:
    def __init__(self, stanleyHelper: StanleyHelper,
                 interpolateService: InterpolateService) -> None:
        self.stanleyHelper = stanleyHelper
        self.interpolateService = interpolateService

    def predictTrajectory(self, course: list[Coordinate]) -> list[Coordinate]:
        courseNew = self.interpolateService.interpolateByModel(course)
        x, y, yaw = self.interpolateService.interpolateBySplines(courseNew)

        # Initial state
        start_yaw: float = float(np.radians(20.0))
        state = StanleyState(self.stanleyHelper, x=courseNew[0].x, y=courseNew[0].y, yaw=start_yaw, v=0.0)

        last_idx: int = len(x) - 1
        time: float = 0.0
        resultX: list = [state.x]
        resultY: list = [state.y]
        resultYaw: list = [state.yaw]
        resultV: list = [state.v]
        resultT: list = [0.0]
        target_idx, _ = self.stanleyHelper.calc_target_index(state, x, y)
        path: list[Coordinate] = []

        while self.stanleyHelper.MAX_SIMULATION_TIME >= time and last_idx > target_idx:
            ai = self.stanleyHelper.pid_control(self.stanleyHelper.TARGET_SPEED, state.v)
            di, target_idx = self.stanleyHelper.stanley_control(state, x, y, yaw, target_idx)
            state.update(ai, di)
            time += self.stanleyHelper.DT

            resultX.append(state.x)
            resultY.append(state.y)
            resultYaw.append(state.yaw)
            resultV.append(state.v)
            resultT.append(time)
            path.append(Coordinate(state.x, state.y, state.yaw))

        return path
