import numpy as np
from common.interpolation.CubicSpline2D import CubicSpline2D


class CubicSplineService:
    def calcSplineCourse(self, x, y, ds=0.1):
        sp = CubicSpline2D(x, y)
        s = list(np.arange(0, sp.s[-1], ds))
        rx, ry, ryaw, rk = [], [], [], []

        for i_s in s:
            ix, iy = sp.calc_position(i_s)
            rx.append(ix)
            ry.append(iy)
            ryaw.append(sp.calc_yaw(i_s))
            rk.append(sp.calc_curvature(i_s))

        return rx, ry, ryaw, rk, s
