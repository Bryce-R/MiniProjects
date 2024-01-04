import numpy as np
import matplotlib.pyplot as plt
import copy
from PointLineSegmentDistance import point

# https://cp-algorithms.com/geometry/minkowski.html
# https://cse442-17f.github.io/Gilbert-Johnson-Keerthi-Distance-Algorithm/


def reorder_polygon(polygon):
    pos = 0
    for i in range(len(polygon)):
        if polygon[i][1] < polygon[0][1] or (
            polygon[i][1] == polygon[0][1] and polygon[i][0] < polygon[0][0]
        ):
            pos = i
    return np.roll(polygon, -pos, axis=0)


def reverse(polygon):
    reverse_polygon = copy.deepcopy(polygon)
    for i in range(len(reverse_polygon)):
        reverse_polygon[i][0] *= -1
        reverse_polygon[i][1] *= -1
    return reverse_polygon


def minkowski(poly1, poly2):
    p1 = reorder_polygon(poly1)
    p2 = reorder_polygon(poly2)
    p1 = np.append(p1, np.array([p1[0]]), axis=0)
    p2 = np.append(p2, np.array([p2[0]]), axis=0)
    p1 = np.append(p1, np.array([p1[1]]), axis=0)
    p2 = np.append(p2, np.array([p2[1]]), axis=0)
    # print(p1, p2)

    i = 0
    j = 0
    sumPoly = np.empty([0, 2], dtype=float)
    while i < len(p1) - 2 or j < len(p2) - 2:
        sumPoly = np.append(
            sumPoly, [[p1[i][0] + p2[j][0], p1[i][1] + p2[j][1]]], axis=0
        )
        cross = np.cross(
            [p1[i + 1][0] - p1[i][0], p1[i + 1][1] - p1[i][1]],
            [p2[j + 1][0] - p2[j][0], p2[j + 1][1] - p2[j][1]],
        )
        if cross >= 0 and i < len(p1) - 2:
            i += 1
        if cross <= 0 and j < len(p2) - 2:
            j += 1
    # print(sumPoly)
    return sumPoly


def minkowski_difference(poly1, poly2):
    p1 = reorder_polygon(poly1)
    p2 = reorder_polygon(reverse(poly2))
    # print(reverse(poly2))
    p1 = np.append(p1, np.array([p1[0]]), axis=0)
    p2 = np.append(p2, np.array([p2[0]]), axis=0)
    p1 = np.append(p1, np.array([p1[1]]), axis=0)
    p2 = np.append(p2, np.array([p2[1]]), axis=0)
    # print(p1, p2)

    i = 0
    j = 0
    sumPoly = np.empty([0, 2], dtype=float)
    while i < len(p1) - 2 or j < len(p2) - 2:
        sumPoly = np.append(
            sumPoly, [[p1[i][0] + p2[j][0], p1[i][1] + p2[j][1]]], axis=0
        )
        cross = np.cross(
            [p1[i + 1][0] - p1[i][0], p1[i + 1][1] - p1[i][1]],
            [p2[j + 1][0] - p2[j][0], p2[j + 1][1] - p2[j][1]],
        )
        if cross >= 0 and i < len(p1) - 2:
            i += 1
        if cross <= 0 and j < len(p2) - 2:
            j += 1
    # print(sumPoly)
    return sumPoly


def plot_polygon(polygon, color, legend):
    """Plot a single polygon."""
    # Add the first point at the end to close the polygon
    closed_polygon = np.vstack([polygon, polygon[0]])
    plt.plot(closed_polygon[:, 0], closed_polygon[:, 1], color=color, label=legend)
    plt.scatter(polygon[:, 0], polygon[:, 1], color=color)


# Example usage
example = 5
if example == 1:
    # two triangles
    # dis = -2
    polygon1 = np.array([[0, 0], [2, 0], [1, 1]])
    polygon2 = np.array([[1, 0], [3, 0], [2, 1]])
elif example == 2:
    # distance = 2
    polygon1 = np.array([[0, 0], [0, 2], [-2, 2], [-2, 0]])
    polygon2 = np.array([[2, 0], [2, 1], [3, 1], [3, 0]])
elif example == 3:
    # distance = 2
    polygon1 = np.array([[0, 0], [0, 2], [-2, 2], [-2, 0]])
    polygon2 = np.array([[2, -2], [3, -2], [3, 1], [2, 1]])
elif example == 4:
    # CCW
    polygon1 = np.array([[-3, 1], [-2, 2], [-4, 2]])
    polygon2 = np.array([[2, 1], [4, 1], [4, 3], [2, 3]])
elif example == 5:
    # CCW
    theta = np.pi / 2.0 + 0.1
    radius = 2
    polygon1 = np.array(
        [
            [0.0, 0.0],
            [2 * np.cos(theta + np.pi / 3), 2 * np.sin(theta + np.pi / 3)],
            [2 * np.cos(theta + np.pi * 0.667), 2 * np.sin(theta + np.pi * 0.667)],
        ]
    )
    polygon2 = np.array([[2, 1], [4, 1], [4, 3], [2, 3]])

# sumPoly = minkowski(polygon1, polygon2)
diffPoly = minkowski_difference(polygon1, polygon2)

plt.figure()
plot_polygon(polygon1, "blue", "p1")
plot_polygon(polygon2, "green", "p2")
# plot_polygon(reverse(polygon2), "green", "reverse_p2")
# plot_polygon(sumPoly, "red")

plot_polygon(diffPoly, "red", "minkowski diff")
plt.xlabel("X axis")
plt.ylabel("Y axis")
plt.title("Convex Polygons")
plt.grid(True)
plt.axis("equal")  # Ensure equal scaling for x and y axes
plt.legend()
# plt.legend(nrow=1, mode="expand", shadow=True, fancybox=True)
plt.show()
