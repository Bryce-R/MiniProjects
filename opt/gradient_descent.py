# -*- coding: utf-8 -*-
"""Gradient descent.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1SCiIWflX_5HzrKuyM7yopG08WLBcx12f
"""

import numpy as np
import matplotlib.pyplot as plt


ks = np.array([[1.0], [1.0]], dtype=np.double)


def f1(x1, x2):
    return ks[0]*x1 + ks[1]*x2


def df1(x1, x2):
    return ks


class circle:
    _k1 = 1.0
    _k2 = 1.0
    _r = 1

    def __init__(self, params):
        if len(params) != 0:
            print("params unpack not implemented.")
            pass

    def cons(self, x):
        return self._k1*x[0]**2 + self._k2*x[1]**2 - self._r

    def deriv(self, x):
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
        x[1, 0] = c/k2
        x[0, 1] = 2.0
        x[1, 1] = c/k2
    elif k2 == 0.0:
        x[0, 0] = c/k1
        x[1, 0] = -2.0
        x[0, 1] = c/k1
        x[1, 1] = 2.0
    else:
        x[0, 0] = c/k1
        x[1, 0] = 0.0
        x[0, 1] = 0.0
        x[1, 1] = c/k2
    return x


class linearCons:
    _kx = [0.0, -1.0]
    _ky = [-1.0, 0.0]
    _c = [-0.5, -0.5]

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

    def deriv(self, x):
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
        pass


k1 = 0.0
k2 = -1.0
c = 0.5


# def linear1(x1, x2):
#     return linear(x1, x2, k1, k2, c)


# def dlinear1(x1, x2):
#     return dlinear(x1, x2, k1, k2)/linear(x1, x2, k1, k2, c)


def drawLinear1():
    return drawLinear(k1, k2, c)


# def linearAndCircle(x1, x2):
#     return np.maximum(linear1(x1, x2), circle(x1, x2))


# def linearAndCircleBarrier(x1, x2):
#     return -np.log(-linear1(x1, x2)) - np.log(-circle(x1, x2))


# def dlinearAndCircle(x1, x2):
#     return dlinear1(x1, x2) + dcircle(x1, x2)


def GD(x0, constraint):
    x = x0
    maxIter = 200
    x_history = np.zeros((2, maxIter), dtype=np.double)
    x_history[:, 0] = x0
    step = 0.2
    k = 1

    cons, dCons = constraints.cons, constraints.deriv
    for i in range(1, maxIter):
        x -= step*df1(x[0], x[1])
        x_history[:, k] = x
        k += 1
        if cons(x) >= 0.0:
            break
    x_history = x_history[:, :k]
    return x_history


def BarrierGD(x0, constraints):
    maxIter = 8
    maxInnerIter = 30

    x = x0
    x_history = np.zeros((2, maxIter*maxInnerIter+1), dtype=np.double)
    x_history[:, 0] = x0[:, 0]

    t = 1.0
    mu = 5.0  # t is scaled by this each outer iteration
    max_t = 1e7
    step_tol = 1e-8
    # gradient descent on t*f(x) + phi(x)
    # phi(x) is the barrier on inequality constraints phi(x) = -log(-g(x))
    # g(x)<=0.0
    # d(phi(x))/dx = - (d(gx)/dx) / g(x)
    # constraint function, constraint function derivative, linearAndCircleBarrier
    cons, dCons, barrierCons = constraints.cons, constraints.deriv, constraints.barrier
    k = 1
    # infeasibility handling
    step = 0.3
    while cons(x) > 0.0:
        # infeasible
        gradient = dCons(x)
        before_cost = cons(x)
        while step >= step_tol:
            x_after = x - step*gradient
            after_cost = cons(x_after)
            if after_cost < before_cost:
                x_history[:, k] = x_after
                x = x_after
                k += 1
                break
            else:
                step /= 2.0
    print("{} iters of infeasibility steps.".format(k-1))
    for i in range(maxIter):
        # centering step
        for j in range(maxInnerIter):
            before_cost = t*f1(x[0], x[1]) + barrierCons(x)
            gradient = t*df1(x[0], x[1]) + dCons(x)
            # print("x, gradient, dCons(x)", x, gradient, dCons(x))
            if np.linalg.norm(gradient) < 1e-5:
                print(
                    "outer iter: {}, innerIter: {}. gradien norm < 1e-5, exiting inner loop.".format(i, j))
                break
            while step >= step_tol:
                x_after = x - step*gradient
                # print("x, gradient, x_after", x, gradient, x_after)
                if cons(x_after) >= -1e-8:
                    print("violating constraints, halfing step size.")
                    # print('cons(x_after):', cons(x_after))
                    step /= 2.0
                    continue
                after_cost = t*f1(x_after[0], x_after[1]
                                  ) + barrierCons(x_after)
                if after_cost < before_cost:
                    x_history[:, k] = x_after[:, 0]
                    x = x_after
                    k += 1
                    # print("step, gradient, x: ",step, gradient, x)
                    break
                else:
                    step /= 2.0
            if (step < step_tol):
                print(
                    'outer iter: {}, innerIter: {}. step < tol, exiting inner loop.'.format(i, j))
                break
        if (step < step_tol):
            print(
                'step < tol, exiting outer loop at iter {}.'.format(i))
            break
        t = t*mu
        if t >= max_t:
            print("exit, t = {}".format(t))
            break
    x_history = x_history[:, :k]
    return x_history


x0 = np.array([0.2, 0.4], dtype=np.double)
# x0 = np.array([-0.1, -0.1], dtype=np.double)
# x0 = np.array([-0.5, 0.5],dtype=np.double)
x0 = np.array([0.6, -0.4], dtype=np.double)
# x0 = np.array([-0.5, 1.2], dtype=np.double)  # infeasible intial solution

# closer to solution but not on center path
# x0 = np.array([-0.6, -0.4], dtype=np.double)
x0 = np.reshape(x0, (2, 1))
# opt = GD
opt = BarrierGD

constraints = circle([])
# constraints = linearCons([])

x_history = opt(x0, constraints)
# '{:-9} YES votes  {:2.2%}'.format(yes_votes, percentage)
print('Optimal solution x1 = {}, x2 = {}.'.format(
    x_history[0, -1], x_history[1, -1]))
# print(x_history)
print(f1(x_history[0, -1], x_history[1, -1]))
# plt.figure(figsize=(12, 9))
# plt.figure(figsize=(16, 12))
plt.figure(figsize=(8, 6))
plt.plot(x_history[0, :], x_history[1, :], '.:', label='history')
plt.plot(x_history[0, 0], x_history[1, 0], 's', label='init')
# for i in range(1, x_history.shape[1]):
#   dx = x_history[0,i] - x_history[0,i-1]
#   dy = x_history[1,i] - x_history[1,i-1]
#   plt.arrow(x_history[0,i-1], x_history[1,i-1], dx, dy, head_width=0.04, head_length=0.1, linewidth=1, color='r', length_includes_head=True)

plt.plot([-np.sqrt(2)/2], [-np.sqrt(2)/2], 'o', label='solution')

boundaries = constraints.boundary()
for boundary in boundaries:
    plt.plot(boundary[0, :], boundary[1, :], '--', label='constraint boundary')
# boundary = drawLinear1()
# plt.plot(boundary[0, :], boundary[1, :], '--', label='constraint boundary')
plt.axis('equal')
plt.legend()
plt.title("min(x1 + x2)")
plt.xlabel("x1")
plt.ylabel("x2")
plt.grid()
plt.show(block=False)

# plt.figure(figsize=(12, 9))
# plt.figure(figsize=(16, 12))
# plt.figure(figsize=(8, 6))

# plt.subplot(2, 1, 1)
# plt.plot(x_history[0, :], '.-')
# plt.ylabel("x1")
# plt.grid()
# plt.subplot(2, 1, 2)
# plt.plot(x_history[1, :], '.-')
# plt.ylabel("x2")
# plt.grid()
plt.show()
