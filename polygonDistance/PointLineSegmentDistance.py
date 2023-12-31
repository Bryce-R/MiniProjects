# distance from point to a line segment
import numpy as np
import matplotlib.pyplot as plt
import copy


# algorithm: https://paulbourke.net/geometry/pointlineplane/
# stackoverflow discussion: https://stackoverflow.com/questions/849211/shortest-distance-between-a-point-and-a-line-segment


class point:
    x = 0.0
    y = 0.0

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "x: " + str(self.x) + ", y: " + str(self.y) + "."

    def distance(self, other):
        return np.hypot(self.x - other.x, self.y - other.y)

    def __sub__(self, other):
        result = point(0, 0)
        result.x = self.x - other.x
        result.y = self.y - other.y
        return result

    def __add__(self, other):
        result = point(0, 0)
        result.x = self.x + other.x
        result.y = self.y + other.y
        return result

    def __mul__(self, other):
        result = point(0, 0)
        result.x = self.x * other
        result.y = self.y * other
        return result

    def np_array(self):
        result = np.array([self.x, self.y])


def point_distance_to_line_segment(point, linePoint1, linePoint2):
    # print(point, linePoint1, linePoint2)
    DUPLICATE_EPS = 1e-5

    # line segment two points are very close
    if linePoint1.distance(linePoint2) < DUPLICATE_EPS:
        return point.distance(linePoint1)

    ratio = (
        (point.x - linePoint1.x) * (linePoint2.x - linePoint1.x)
        + (point.y - linePoint1.y) * (linePoint2.y - linePoint1.y)
    ) / (linePoint1.distance(linePoint2)) ** 2

    if ratio <= 0:
        # print("using linePoint1")
        return point.distance(linePoint1)
    elif ratio >= 1:
        # print("using linePoint2")
        return point.distance(linePoint2)
    else:
        # print("ratio:", ratio)
        return (linePoint1 + (linePoint2 - linePoint1) * ratio).distance(point)


if __name__ == "__main__":
    print("Testing function calcuclating distance from point to line segment!")
    testcase = [1, 2]
    for test in testcase:
        if test == 1:
            p1 = point(0, 0)
            l1 = point(-2, 2)
            l2 = point(2, 2)
            distance = point_distance_to_line_segment(p1, l1, l2)
            assert distance == 2.0
        elif test == 2:
            p1 = point(0, 0)
            l1 = point(0, 2)
            l2 = point(2, 0)
            assert point_distance_to_line_segment(p1, l1, l2) == np.sqrt(2.0)
    print("all test cases from", testcase, "passing!")
