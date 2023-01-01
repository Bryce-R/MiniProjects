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


class iLQR(object):
    def __init__(self, numInput, numState, horizon, Q, R):
        self._numInput = numInput
        self._numState = numState
        self._horizon = horizon
        self._Q = Q
        self._R = R
        assert(_Q.shape == (_numState, _numState))
        assert(_Q.shape == (_numInput, _numInput))

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
        pass


if __name__ == '__main__':

    horizon = 2
    numState = 3
    numInput = 2
    iLQR ilqr(numInput, numState, horizon)
    reference = np.zeros((numState, horizon), dtype=np.double)
    control = np.zeros((numInput, horizon), dtype=np.double)
    ilqr.solve(reference, control)
