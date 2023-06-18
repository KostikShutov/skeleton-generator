import math
import numpy as np
from common.coordinates.Coordinate import Coordinate
from common.interpolation.InterpolateService import InterpolateService
from trainer.PredictiveConfig import PredictiveConfig
from trainer.PredictiveHelper import PredictiveHelper
from trainer.PredictiveState import PredictiveState


class PredictiveController:
    def __init__(self, predictiveHelper: PredictiveHelper,
                 interpolateService: InterpolateService) -> None:
        self.predictiveHelper = predictiveHelper
        self.interpolateService = interpolateService

    def calculateTrajectory(self, course: list[Coordinate]) -> list[Coordinate]:
        courseNew = self.interpolateService.interpolateByLinear(course)
        cx, cy, cyaw = self.interpolateService.interpolateBySplines(courseNew)
        sp = self.predictiveHelper.calc_speed_profile(cx, cy, cyaw, PredictiveConfig.TARGET_SPEED)
        state = PredictiveState(x=cx[0], y=cy[0], yaw=cyaw[0], v=0.0)

        if state.yaw - cyaw[0] >= math.pi:
            state.yaw -= math.pi * 2.0
        elif state.yaw - cyaw[0] <= -math.pi:
            state.yaw += math.pi * 2.0

        time: float = 0.0
        x = [state.x]
        y = [state.y]
        yaw = [state.yaw]
        v = [state.v]
        t = [0.0]
        s = [0.0]
        a = [0.0]
        target_ind, _ = self.predictiveHelper.calc_nearest_index(state, cx, cy, cyaw, 0)
        odelta, oa = None, None
        cyaw = self.predictiveHelper.smooth_yaw(cyaw)
        path: list[Coordinate] = []

        for i in range(min(len(cx), len(cy), len(cyaw))):
            xref, target_ind, dref = self.predictiveHelper.calc_ref_trajectory(
                state=state,
                cx=cx,
                cy=cy,
                cyaw=cyaw,
                ck=None,
                sp=sp,
                ds=self.interpolateService.DS,
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
                state.update(acceleration, steering, i, cx, cy)

            time = time + PredictiveConfig.DT
            x.append(state.x)
            y.append(state.y)
            yaw.append(state.yaw)
            v.append(state.v)
            t.append(time)
            a.append(acceleration)
            s.append(steering)
            path.append(Coordinate(state.x, state.y, float(np.degrees(-steering))))

        return path
