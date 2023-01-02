import numpy as np


class circle:
    _k1 = 1.0
    _k2 = 1.0
    _r = 1
    name = "circleCons"

    def __init__(self, params):
        if len(params) != 0:
            print("params unpack not implemented.")
            pass

    def cons(self, x):
        return self._k1*x[0]**2 + self._k2*x[1]**2 - self._r

    def derivBarrier(self, x):
        dfdx = -np.array(
            [self._k1*2.0*x[0], self._k2*2.0*x[1]], dtype=np.double)
        return np.reshape(dfdx, (2, 1)) / self.cons(x)

    def barrier(self, x):
        c = self.cons(x)
        if (c > 0.0):
            print("function is infeasible!")
        return -np.log(-c)

    def boundary(self):
        boundaries = []
        num = 101
        rad = np.pi/(num-1)*2
        x = np.zeros((2, num), dtype=np.double)
        for i in range(num):
            x[0, i] = self._r*np.cos(i*rad)
            x[1, i] = self._r*np.sin(i*rad)
        boundaries += [x]
        return boundaries


def linear(x1, x2, k1, k2, c):
    return x1*k1 + x2*k2 + c


def dlinear(x1, x2, k1, k2):
    return np.array([[k1], [k2]], dtype=np.double)


def drawLinear(k1, k2, c):
    num = 2
    x = np.zeros((2, num), dtype=np.double)
    if k1 == 0.0:
        x[0, 0] = -2.0
        x[1, 0] = -c/k2
        x[0, 1] = 2.0
        x[1, 1] = -c/k2
    elif k2 == 0.0:
        x[0, 0] = -c/k1
        x[1, 0] = -2.0
        x[0, 1] = -c/k1
        x[1, 1] = 2.0
    else:
        x[0, 0] = -c/k1
        x[1, 0] = 0.0
        x[0, 1] = 0.0
        x[1, 1] = -c/k2
    return x


class linearCons:
    _kx = [0.0, -1.0]
    _ky = [-1.0, 0.0]
    _c = [-0.5, -0.5]
    name = "linearCons"

    def __init__(self, params):
        if len(params) != 0:
            print("params unpack not implemented.")
            pass

    def cons(self, x):
        res = -np.inf
        for i in range(len(self._kx)):
            f = linear(
                x[0], x[1], self._kx[i], self._ky[i], self._c[i])
            res = max(res, f)
            # print("res, f", res, f)
        return res

    def derivBarrier(self, x):
        res = np.zeros((2, 1), dtype=np.double)
        for i in range(len(self._kx)):
            grad = -dlinear(x[0], x[1], self._kx[i], self._ky[i])
            f = linear(
                x[0], x[1], self._kx[i], self._ky[i], self._c[i])
            # print("grad, f", grad, f)
            res += grad/f
        return res

    def barrier(self, x):
        res = 0.0
        for i in range(len(self._kx)):
            f = linear(
                x[0], x[1], self._kx[i], self._ky[i], self._c[i])
            if (f > 0.0):
                print("function is infeasible!")
            res += -np.log(-f)
        return res

    def boundary(self):
        boundaries = []
        for i in range(len(self._kx)):
            x = drawLinear(self._kx[i], self._ky[i], self._c[i])
            boundaries += [x]
        return boundaries
