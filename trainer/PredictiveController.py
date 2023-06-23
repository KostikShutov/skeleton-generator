import math
import numpy as np
from common.coordinates.Coordinate import Coordinate
from common.coordinates.CoordinatesTransformer import CoordinatesTransformer
from common.interpolation.InterpolateService import InterpolateService
from trainer.PredictiveConfig import PredictiveConfig
from trainer.PredictiveHelper import PredictiveHelper
from trainer.PredictiveState import PredictiveState


class PredictiveController:
    def __init__(self, coordinatesTransformer: CoordinatesTransformer,
                 predictiveHelper: PredictiveHelper) -> None:
        self.coordinatesTransformer = coordinatesTransformer
        self.predictiveHelper = predictiveHelper

    def calculateTrajectory(self, course: list[Coordinate]) -> list[Coordinate]:
        inputX, inputY, inputYaw = self.coordinatesTransformer.separateToFloatLists(course)

        sp = self.predictiveHelper.calc_speed_profile(inputX, inputY, inputYaw, PredictiveConfig.TARGET_SPEED)
        state = PredictiveState(x=inputX[0], y=inputY[0], yaw=inputYaw[0], v=0.0)

        if state.yaw - inputYaw[0] >= math.pi:
            state.yaw -= math.pi * 2.0
        elif state.yaw - inputYaw[0] <= -math.pi:
            state.yaw += math.pi * 2.0

        time: float = 0.0
        outputX = [state.x]
        outputY = [state.y]
        outputYaw = [state.yaw]
        outputV = [state.v]
        outputT = [0.0]
        outputS = [0.0]
        outputA = [0.0]
        target_ind, _ = self.predictiveHelper.calc_nearest_index(state, inputX, inputY, inputYaw, 0)
        odelta, oa = None, None
        inputYaw = self.predictiveHelper.smooth_yaw(inputYaw)
        path: list[Coordinate] = []

        for i in range(min(len(inputX), len(inputY), len(inputYaw))):
            xref, target_ind, dref = self.predictiveHelper.calc_ref_trajectory(
                state=state,
                cx=inputX,
                cy=inputY,
                cyaw=inputYaw,
                ck=None,
                sp=sp,
                ds=InterpolateService.DS,
                pind=target_ind,
            )

            x0 = [state.x, state.y, state.v, state.yaw]

            oa, odelta, ox, oy, oyaw, ov = self.predictiveHelper.iterative_linear_mpc_control(
                xref=xref,
                x0=x0,
                dref=dref,
                oa=oa,
                od=odelta,
            )

            acceleration, steering = 0.0, 0.0

            if odelta is not None:
                acceleration, steering = oa[0], odelta[0],
                state.update(acceleration, steering, i, inputX, inputY)

            time = time + PredictiveConfig.DT
            outputX.append(state.x)
            outputY.append(state.y)
            outputYaw.append(state.yaw)
            outputV.append(state.v)
            outputT.append(time)
            outputA.append(acceleration)
            outputS.append(steering)
            path.append(Coordinate(state.x, state.y, float(np.degrees(-steering))))

        return path
