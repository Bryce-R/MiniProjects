import numpy as np
import pylab as pl
# model
# dx/dt = v*cos(theta)
# dy/dt = v*sin(theta)
# d(theta)/dt = v*curvature


class state:
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0


def integrate(x, y, theta, v, curvature):
    x_next = x + v*np.cos(theta)
    y_next = y + v*np.sin(theta)
    theta_next = theta + v*curvature
    return (x_next, y_next, theta_next)


def f_x(x, y, theta, v, curvature):
    f_x = np.zeros([numState, numState], dtype=np.double)
    f_x[0, 0] = 1  # dx/dx
    f_x[0, 2] = -v*np.sin(theta)  # dx/d  theta
    f_x[1, 1] = 1
    f_x[1, 2] = v*np.cos(theta)  # dy/d(theta)
    f_x[2, 2] = 1
    return f_x


class iLQR(object):
    def __init__(self, numInput, numState, horizon, Q, R, Qf):
        self._numInput = numInput
        self._numState = numState
        self._horizon = horizon
        self._Q = Q
        self._R = R
        self._Qf = Qf
        assert(_Q.shape == (_numState, _numState))
        assert(_Qf.shape == (_numState, _numState))
        assert(_R.shape == (_numInput, _numInput))

    def solve(reference, control):
        assert(reference.shape == (_numState, _horizon))
        assert(reference.shape == (_numInput, _horizon))
        self._reference = reference
        self._control = control

    def forwardPass():
        # uninitilized, need to overwrite
        updated_output = np.empty([numState, horizon], dtype=np.double)

        updated_output[:, 0] = self._reference[:, 0]
        for i in range(1, self.updated_output.shape(1)):
            x_next, y_next, theta_next = integrate(
                self.updated_output[0, i-1], self.updated_output[1, i-1], self.updated_output[2, i-1], self._control[0, i-1], self._control[1, i-1])
            self.updated_output[0, i] = x_next
            self.updated_output[1, i] = y_next
            self.updated_output[2, i] = theta_next

    def backwardPass():
        # Eqs (5a), (5b) and (5c).
        # Q_x = l_x + f_x.T.dot(V_x)
        # Q_u = l_u + f_u.T.dot(V_x)
        # Q_xx = l_xx + f_x.T.dot(V_xx).dot(f_x)

        # Eqs (11b) and (11c).
        # reg = self._mu * np.eye(self.dynamics.state_size)
        # Q_ux = l_ux + f_u.T.dot(V_xx + reg).dot(f_x)
        # Q_uu = l_uu + f_u.T.dot(V_xx + reg).dot(f_u)
        # k = -(Q_uu)^-1 * Q_u
        # K = -(Q_uu)^-1 * Q_ux
        # u(i)_new =  u(i) + k(i) + K(i)*[x(i) - x_ref(i)]

        # Vf = xf^T * Qf * xf
        # final state
        Vxx = _Qf
        Vx = self.updated_output[:, -1]*_Qf

        for i in range(self.updated_output.shape(1), -1):
            l_x = self.updated_output[:, i]*_Q  # l_x = x^T * Q * x
            f_x = f_x(self.updated_output[0, i], self.updated_output[1, i],
                      self.updated_output[2, i], self._control[0, i-1], self._control[1, i-1])
            Q_x = l_x + f_x.transpose()*Vx
            l_u = self._control[0, i-1]*_R
            # Q_u = l_u + f_u.transpose()*Vx


if __name__ == '__main__':

    horizon = 2
    numState = 3
    numInput = 2
    iLQR ilqr(numInput, numState, horizon)
    reference = np.zeros((numState, horizon), dtype=np.double)
    control = np.zeros((numInput, horizon), dtype=np.double)
    ilqr.solve(reference, control)
