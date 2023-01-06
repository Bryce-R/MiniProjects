import numpy as np
import matplotlib.pyplot as plt
from constraint import *
from gradient_descent import *


x = np.zeros((2, 6), dtype=np.double)
x[:, 0] = np.array([0.2, 0.4], dtype=np.double)
x[:, 1] = np.array([-0.1, -0.1], dtype=np.double)
x[:, 2] = np.array([-0.5, 0.5], dtype=np.double)
x[:, 3] = np.array([0.6, -0.4], dtype=np.double)
x[:, 4] = np.array([-0.5, 1.2], dtype=np.double)  # infeasible intial solution
# closer to solution but not on center path
x[:, 5] = np.array([-0.6, -0.4], dtype=np.double)

# opt = GD
opt = BarrierGD

constraints = circle([])
constraints = linearCons([])
print("-------------------Starting Optimization---------------------------")
runAllSolve = False
if runAllSolve:
    for i in range(x.shape[1]):
        x_history, k = opt(np.reshape(x[:, i], (2, 1)), constraints)
        print("Solve {}, Total iterations: {}.".format(i, k))
else:
    i = 4
    x_history, k = opt(np.reshape(x[:, i], (2, 1)), constraints)
    print("Solve {}, Total iterations: {}.".format(i, k))
    print('Calculated Optimal solution x1 = {}, x2 = {}.'.format(
        x_history[0, -1], x_history[1, -1]))
    # print(x_history)
    print("optimal cost: ", f1(x_history[0, -1], x_history[1, -1])[0])
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
    # plt.plot([-np.sqrt(2)/2], [-np.sqrt(2)/2], 'o', label='solution')

    boundaries = constraints.boundary()
    i = 1
    for boundary in boundaries:
        plt.plot(boundary[0, :], boundary[1, :],
                 '--', label='constraint ' + str(i))
        i += 1

    plt.axis('equal')
    plt.legend()
    plt.title("min(x1 + x2)")
    plt.xlabel("x1")
    plt.ylabel("x2")
    plt.grid()
    plt.show(block=False)
    plt.savefig('2D'+constraints.name+'.png')

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
