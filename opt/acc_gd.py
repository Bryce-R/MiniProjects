
import numpy as np
import matplotlib.pyplot as plt
from constraint import *

a = 5.0
b = 1.0
ks = np.array([[a], [b]], dtype=np.double)


def f1(x):
    return ks[0]*x[0] ^ 2 + ks[1]*x[1] ^ 2


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
    x_history[:, 0] = x0[:, 0]
    step = 0.2
    k = 1

    for i in range(1, maxIter):
        x -= step*df(x)
        x_history[:, k] = x[:, 0]
        k += 1
    x_history = x_history[:, :k]
    return x_history, k


x = np.zeros((2, 6), dtype=np.double)
x[:, 0] = np.array([0.2, 0.4], dtype=np.double)
x[:, 1] = np.array([0.12, -0.8], dtype=np.double)
x[:, 2] = np.array([-0.5, 0.5], dtype=np.double)
x[:, 3] = np.array([0.6, -0.4], dtype=np.double)
x[:, 4] = np.array([-0.5, 1.2], dtype=np.double)  # infeasible intial solution
# closer to solution but not on center path
x[:, 5] = np.array([-0.6, -0.4], dtype=np.double)

opt = GD

print("-------------------Starting Optimization---------------------------")
runAllSolve = False
if runAllSolve:
    for i in range(x.shape[1]):
        x_history, k = opt(np.reshape(x[:, i], (2, 1)), f1, df1)
        print("Solve {}, Total iterations: {}.".format(i, k))
else:
    i = 1
    x_history, k = opt(np.reshape(x[:, i], (2, 1)), f1, df1)
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
                 '--', label='constraint ' + str(i))
        i += 1

    plt.axis('equal')
    plt.legend()
    plt.title("min(5*x1^2 + x2^2)")
    plt.xlabel("x1")
    plt.ylabel("x2")
    # plt.grid()
    plt.grid(color='lightgray', linestyle='--')
    plt.show(block=False)
    plt.savefig('2D_acc_gd.png')

    # plt.figure(figsize=(12, 9))
    # plt.figure(figsize=(16, 12))

    plt.figure(figsize=(8, 6))
    plt.subplot(2, 1, 1)
    plt.plot(x_history[0, :], '.-')
    plt.ylabel("x1")
    plt.grid()
    plt.subplot(2, 1, 2)
    plt.plot(x_history[1, :], '.-')
    plt.ylabel("x2")
    plt.grid()
    plt.show()
