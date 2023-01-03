
import numpy as np
import matplotlib.pyplot as plt
from constraint import *

a = 5.0
b = 1.0
ks = np.array([[a], [b]], dtype=np.double)


def f1(x):
    return ks[0]*x[0] ** 2 + ks[1]*x[1] ** 2


def df1(x):
    dfdx = np.array(
        [ks[0]*2.0*x[0], ks[1]*2.0*x[1]], dtype=np.double)
    return np.reshape(dfdx, (2, 1))


def boundary():
    boundaries = []
    num = 101
    rad = np.pi/(num-1)*2
    for j in range(10):
        k = j*0.1+0.2
        x = np.zeros((2, num), dtype=np.double)
        for i in range(num):
            x[0, i] = k*np.cos(i*rad)/a
            x[1, i] = k*np.sin(i*rad)/b
        boundaries += [x]
    return boundaries


def GD(x0, f, df):
    x = x0
    maxIter = 200
    x_history = np.zeros((2, maxIter), dtype=np.double)
    cost_history = np.zeros((maxIter, 1), dtype=np.double)
    cost_history[0, 0] = f(x0)
    x_history[:, 0] = x0[:, 0]
    step = 0.2
    k = 1
    step_tol = 1e-8
    printDebug = True
    for i in range(1, maxIter):
        before_cost = f(x)
        gradient = df(x)
        while step >= step_tol:
            x_after = x - step*gradient
            after_cost = f(x_after)
            if after_cost < before_cost:
                x_history[:, k] = x_after[:, 0]
                cost_history[k, 0] = after_cost
                x = x_after
                k += 1
                break
            else:
                step /= 2.0
        if (step < step_tol):
            if printDebug:
                print(
                    'Iter: {}: step < tol, exiting.'.format(i))
            break
        # if (np.abs(before_cost - after_cost) / np.abs(before_cost) < 1e-12):
        #     if printDebug:
        #         print(
        #             'Iter: {}: cost change < tol, exiting.'.format(i))
        #     break
        if np.linalg.norm(gradient) < 1e-5:
            if printDebug:
                print(
                    "Iter: {}: gradien norm < 1e-5, exiting .".format(i))
            break
    x_history = x_history[:, :k]
    cost_history = cost_history[:k, :]
    return x_history, cost_history, k


def NesterovGD(x0, f, df):
    # http://awibisono.github.io/2016/06/20/accelerated-gradient-descent.html
    x = x0
    maxIter = 200
    x_history = np.zeros((2, maxIter), dtype=np.double)
    cost_history = np.zeros((maxIter, 1), dtype=np.double)
    cost_history[0, 0] = f(x0)
    x_history[:, 0] = x0[:, 0]
    step = 0.05  # should be less than eps where f function is 1/eps smooth
    k = 1
    step_tol = 1e-8
    printDebug = True
    for i in range(1, maxIter):
        before_cost = f(x)

        kk = k-1
        y_k = x + (kk-1)/(kk+2) * \
            np.reshape(x_history[:, kk]-x_history[:, max(kk-1, 0)], (2, 1))

        gradient = df(y_k)
        x_after = x - step*gradient
        after_cost = f(x_after)
        x_history[:, k] = x_after[:, 0]
        cost_history[k, 0] = after_cost
        x = x_after
        k += 1

        if (step < step_tol):
            if printDebug:
                print(
                    'Iter: {}: step < tol, exiting.'.format(i))
            break
        # if (np.abs(before_cost - after_cost) / np.abs(before_cost) < 1e-5):
        #     if printDebug:
        #         print(
        #             'Iter: {}: cost change < tol, exiting.'.format(i))
        #     break
        if np.linalg.norm(gradient) < 1e-5:
            if printDebug:
                print(
                    "Iter: {}: gradient norm < 1e-5, exiting .".format(i))
            break
    x_history = x_history[:, :k]
    cost_history = cost_history[:k, :]
    return x_history, cost_history, k


x = np.zeros((2, 6), dtype=np.double)
# simple case, converging along one axis
x[:, 0] = np.array([0.0, 0.8], dtype=np.double)
# swing and overshoot left and right
x[:, 1] = np.array([0.12, -0.8], dtype=np.double)
x[:, 2] = np.array([-0.01, 0.8], dtype=np.double)
x[:, 3] = np.array([0.6, -0.4], dtype=np.double)
x[:, 4] = np.array([-0.5, 1.2], dtype=np.double)  # infeasible intial solution
# closer to solution but not on center path
x[:, 5] = np.array([-0.6, -0.4], dtype=np.double)

# opt, name = GD, "vanillaGD"
opt, name = NesterovGD, "NesterovGD"


print("-------------------Starting Optimization---------------------------")
runAllSolve = True
if runAllSolve:
    for i in range(x.shape[1]):
        x_history, cost_history, k = opt(np.reshape(x[:, i], (2, 1)), f1, df1)
        print("Solve {}, Total iterations: {}.".format(i, k))
else:
    i = 4
    x_history, cost_history, k = opt(np.reshape(x[:, i], (2, 1)), f1, df1)
    print("Solve {}, Total iterations: {}.".format(i, k))
    print('Calculated Optimal solution x1 = {}, x2 = {}.'.format(
        x_history[0, -1], x_history[1, -1]))
    # print(x_history)

    # plt.figure(figsize=(12, 9))
    # plt.figure(figsize=(16, 12))
    plt.figure(figsize=(8, 6))
    plt.plot(x_history[0, :], x_history[1, :], '.:', label='history')
    plt.plot(x_history[0, 0], x_history[1, 0], 's', label='init')
    # for i in range(1, x_history.shape[1]):
    #   dx = x_history[0,i] - x_history[0,i-1]
    #   dy = x_history[1,i] - x_history[1,i-1]
    #   plt.arrow(x_history[0,i-1], x_history[1,i-1], dx, dy, head_width=0.04, head_length=0.1, linewidth=1, color='r', length_includes_head=True)
    plt.plot(x_history[0, -1], x_history[1, -1], 'o', label='solution')

    boundaries = boundary()
    i = 1
    for boundary in boundaries:
        plt.plot(boundary[0, :], boundary[1, :],
                 '--', label='level-' + str(i))
        i += 1

    plt.axis('equal')
    plt.legend(fancybox=True, framealpha=0.5)
    plt.title("min(5*x1^2 + x2^2)")
    plt.xlabel("x1")
    plt.ylabel("x2")
    # plt.grid()
    plt.grid(color='lightgray', linestyle='--')
    plt.show(block=False)
    plt.savefig('acc_'+name+'_2d.png')

    # plt.figure(figsize=(12, 9))
    # plt.figure(figsize=(16, 12))

    plt.figure(figsize=(8, 6))
    plt.suptitle(name)
    plt.subplot(3, 1, 1)
    plt.plot(x_history[0, :], '.-')
    plt.ylabel("x1")
    plt.grid()
    plt.subplot(3, 1, 2)
    plt.plot(x_history[1, :], '.-')
    plt.ylabel("x2")
    plt.grid()
    plt.subplot(3, 1, 3)
    plt.plot(cost_history[:, 0], '.-')
    plt.yscale('log')
    # plt.autoscale(enable=True, axis='x', tight=True)
    plt.ylabel("cost")
    plt.grid()
    plt.savefig('acc_'+name+'_x.png')

    plt.show()
