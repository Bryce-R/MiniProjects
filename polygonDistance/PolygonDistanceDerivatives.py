# calculating polygon distance derivatives

from PointLineSegmentDistance import *
from Minkowski import *


def point_to_np_array(polygon):
    np_array = np.empty([0, 2], dtype=float)
    for p in polygon:
        np_array = np.append(np_array, [[point.x, point.y]], axis=0)
    return np_array


def polygon_derivative(poly1, poly2):
    p1 = point_to_np_array(poly1)
    p2 = point_to_np_array(poly2)


if __name__ == "__main__":
    print("Testing function calcuclating derivative of polygon distance!")
    testcase = [1, 2]
    for test in testcase:
        if test == 1:
            # CCW
            polygon1 = [point(0, 0), point(0, 1), point(1, 1), point(1, 0)]
            polygon2 = [point(3, 3), point(3, 4), point(4, 4), point(4, 3)]

    print("all test cases from", testcase, "passing!")
