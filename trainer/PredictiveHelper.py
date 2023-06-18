import math
import cvxpy
import numpy as np
from trainer.PredictiveConfig import PredictiveConfig
from trainer.PredictiveState import PredictiveState


class PredictiveHelper:
    def pi_2_pi(self, angle):
        while angle > math.pi:
            angle = angle - 2.0 * math.pi

        while angle < -math.pi:
            angle = angle + 2.0 * math.pi

        return angle

    def get_linear_model_matrix(self, v, phi, delta):
        A = np.zeros((PredictiveConfig.NX, PredictiveConfig.NX))
        A[0, 0] = 1.0
        A[1, 1] = 1.0
        A[2, 2] = 1.0
        A[3, 3] = 1.0
        A[0, 2] = PredictiveConfig.DT * math.cos(phi)
        A[0, 3] = -PredictiveConfig.DT * v * math.sin(phi)
        A[1, 2] = PredictiveConfig.DT * math.sin(phi)
        A[1, 3] = PredictiveConfig.DT * v * math.cos(phi)
        A[3, 2] = PredictiveConfig.DT * math.tan(delta) / PredictiveConfig.WB

        B = np.zeros((PredictiveConfig.NX, PredictiveConfig.NU))
        B[2, 0] = PredictiveConfig.DT
        B[3, 1] = PredictiveConfig.DT * v / (PredictiveConfig.WB * math.cos(delta) ** 2)

        C = np.zeros(PredictiveConfig.NX)
        C[0] = PredictiveConfig.DT * v * math.sin(phi) * phi
        C[1] = -PredictiveConfig.DT * v * math.cos(phi) * phi
        C[3] = -PredictiveConfig.DT * v * delta / (PredictiveConfig.WB * math.cos(delta) ** 2)

        return A, B, C

    def get_nparray_from_matrix(self, x):
        return np.array(x).flatten()

    def calc_nearest_index(self, state, cx, cy, cyaw, pind):
        dx = [state.x - icx for icx in cx[pind:(pind + PredictiveConfig.N_IND_SEARCH)]]
        dy = [state.y - icy for icy in cy[pind:(pind + PredictiveConfig.N_IND_SEARCH)]]
        d = [idx ** 2 + idy ** 2 for (idx, idy) in zip(dx, dy)]
        mind = min(d)
        ind = d.index(mind) + pind
        mind = math.sqrt(mind)
        dxl = cx[ind] - state.x
        dyl = cy[ind] - state.y
        angle = self.pi_2_pi(cyaw[ind] - math.atan2(dyl, dxl))

        if angle < 0:
            mind *= -1

        return ind, mind

    def predict_motion(self, x0, oa, od, xref):
        xbar = xref * 0.0

        for i, _ in enumerate(x0):
            xbar[i, 0] = x0[i]

        state = PredictiveState(x=x0[0], y=x0[1], yaw=x0[3], v=x0[2])

        for (ai, di, i) in zip(oa, od, range(1, PredictiveConfig.T + 1)):
            state.update(ai, di)
            xbar[0, i] = state.x
            xbar[1, i] = state.y
            xbar[2, i] = state.v
            xbar[3, i] = state.yaw

        return xbar

    def iterative_linear_mpc_control(self, xref, x0, dref, oa, od):
        ox, oy, oyaw, ov = None, None, None, None

        if oa is None or od is None:
            oa = [0.0] * PredictiveConfig.T
            od = [0.0] * PredictiveConfig.T

        for i in range(PredictiveConfig.MAX_ITER):
            xbar = self.predict_motion(x0, oa, od, xref)
            poa, pod = oa[:], od[:]
            oa, od, ox, oy, oyaw, ov = self.linear_mpc_control(xref, xbar, x0, dref)
            du = sum(abs(oa - poa)) + sum(abs(od - pod))

            if du <= PredictiveConfig.DU_TH:
                break

        return oa, od, ox, oy, oyaw, ov

    def linear_mpc_control(self, xref, xbar, x0, dref):
        x = cvxpy.Variable((PredictiveConfig.NX, PredictiveConfig.T + 1))
        u = cvxpy.Variable((PredictiveConfig.NU, PredictiveConfig.T))

        cost = 0.0
        constraints = []

        for t in range(PredictiveConfig.T):
            cost += cvxpy.quad_form(u[:, t], PredictiveConfig.R)

            if t != 0:
                cost += cvxpy.quad_form(xref[:, t] - x[:, t], PredictiveConfig.Q)

            A, B, C = self.get_linear_model_matrix(xbar[2, t], xbar[3, t], dref[0, t])
            constraints += [x[:, t + 1] == A @ x[:, t] + B @ u[:, t] + C]

            if t < (PredictiveConfig.T - 1):
                cost += cvxpy.quad_form(u[:, t + 1] - u[:, t], PredictiveConfig.Rd)
                constraints += [cvxpy.abs(u[1, t + 1] - u[1, t]) <= PredictiveConfig.MAX_DSTEER * PredictiveConfig.DT]

        cost += cvxpy.quad_form(xref[:, PredictiveConfig.T] - x[:, PredictiveConfig.T], PredictiveConfig.Qf)

        constraints += [x[:, 0] == x0]
        constraints += [x[2, :] <= PredictiveConfig.MAX_SPEED]
        constraints += [x[2, :] >= PredictiveConfig.MIN_SPEED]
        constraints += [cvxpy.abs(u[0, :]) <= PredictiveConfig.MAX_ACCEL]
        constraints += [cvxpy.abs(u[1, :]) <= PredictiveConfig.MAX_STEER]

        prob = cvxpy.Problem(cvxpy.Minimize(cost), constraints)
        prob.solve(solver=cvxpy.ECOS, verbose=False)

        if prob.status == cvxpy.OPTIMAL or prob.status == cvxpy.OPTIMAL_INACCURATE:
            ox = self.get_nparray_from_matrix(x.value[0, :])
            oy = self.get_nparray_from_matrix(x.value[1, :])
            ov = self.get_nparray_from_matrix(x.value[2, :])
            oyaw = self.get_nparray_from_matrix(x.value[3, :])
            oa = self.get_nparray_from_matrix(u.value[0, :])
            odelta = self.get_nparray_from_matrix(u.value[1, :])
        else:
            print('Error: Cannot solve mpc..')
            oa, odelta, ox, oy, oyaw, ov = None, None, None, None, None, None

        return oa, odelta, ox, oy, oyaw, ov

    def calc_ref_trajectory(self, state, cx, cy, cyaw, ck, sp, ds, pind):
        xref = np.zeros((PredictiveConfig.NX, PredictiveConfig.T + 1))
        dref = np.zeros((1, PredictiveConfig.T + 1))
        ncourse = len(cx)

        ind, _ = self.calc_nearest_index(state, cx, cy, cyaw, pind)

        if pind >= ind:
            ind = pind

        xref[0, 0] = cx[ind]
        xref[1, 0] = cy[ind]
        xref[2, 0] = sp[ind]
        xref[3, 0] = cyaw[ind]
        dref[0, 0] = 0.0

        travel = 0.0

        for i in range(PredictiveConfig.T + 1):
            travel += abs(state.v) * PredictiveConfig.DT
            dind = int(round(travel / ds))

            if (ind + dind) < ncourse:
                xref[0, i] = cx[ind + dind]
                xref[1, i] = cy[ind + dind]
                xref[2, i] = sp[ind + dind]
                xref[3, i] = cyaw[ind + dind]
                dref[0, i] = 0.0
            else:
                xref[0, i] = cx[ncourse - 1]
                xref[1, i] = cy[ncourse - 1]
                xref[2, i] = sp[ncourse - 1]
                xref[3, i] = cyaw[ncourse - 1]
                dref[0, i] = 0.0

        return xref, ind, dref

    def calc_speed_profile(self, cx, cy, cyaw, target_speed):
        speed_profile = [target_speed] * len(cx)
        direction = 1.0

        for i in range(len(cx) - 1):
            dx = cx[i + 1] - cx[i]
            dy = cy[i + 1] - cy[i]
            move_direction = math.atan2(dy, dx)

            if dx != 0.0 and dy != 0.0:
                dangle = abs(self.pi_2_pi(move_direction - cyaw[i]))

                if dangle >= math.pi / 4.0:
                    direction = -1.0
                else:
                    direction = 1.0

            if direction != 1.0:
                speed_profile[i] = -target_speed
            else:
                speed_profile[i] = target_speed

        speed_profile[-1] = 0.0

        return speed_profile

    def smooth_yaw(self, yaw):
        for i in range(len(yaw) - 1):
            dyaw = yaw[i + 1] - yaw[i]

            while dyaw >= math.pi / 2.0:
                yaw[i + 1] -= math.pi * 2.0
                dyaw = yaw[i + 1] - yaw[i]

            while dyaw <= -math.pi / 2.0:
                yaw[i + 1] += math.pi * 2.0
                dyaw = yaw[i + 1] - yaw[i]

        return yaw
