import numpy as np
import matplotlib.pyplot as plt

def edge_normals(polygon):
    """Calculate outward normals for each edge of the polygon."""
    normals = []
    for i in range(len(polygon)):
        edge = polygon[(i + 1) % len(polygon)] - polygon[i]
        normals.append(np.array([-edge[1], edge[0]]))  # Outward normal
    return normals

def project_polygon(polygon, axis):
    """Project all vertices of the polygon onto the given axis."""
    dots = np.dot(polygon, axis)
    return min(dots), max(dots)

def overlap(interval_a, interval_b):
    """Return the overlap amount between two intervals."""
    return max(0, min(interval_a[1], interval_b[1]) - max(interval_a[0], interval_b[0]))

def polygon_distance(polygon1, polygon2):
    """Calculate the distance between two convex polygons."""
    all_normals = edge_normals(polygon1) + edge_normals(polygon2)
    min_distance = float('inf')
    max_overlap = 0

    for normal in all_normals:
        proj1 = project_polygon(polygon1, normal)
        proj2 = project_polygon(polygon2, normal)
        if proj1[1] < proj2[0] or proj2[1] < proj1[0]:  # No overlap
            distance = min(abs(proj1[1] - proj2[0]), abs(proj2[1] - proj1[0]))
            min_distance = min(min_distance, distance)
        else:  # Overlap exists
            overlap_amount = overlap(proj1, proj2)
            max_overlap = max(max_overlap, overlap_amount)

    if min_distance == float('inf'):  # Polygons overlap
        return -max_overlap
    return min_distance

def plot_polygon(polygon, color):
    """Plot a single polygon."""
    # Add the first point at the end to close the polygon
    closed_polygon = np.vstack([polygon, polygon[0]])
    plt.plot(closed_polygon[:, 0], closed_polygon[:, 1], color=color)
    plt.scatter(polygon[:, 0], polygon[:, 1], color=color)


# Example usage
example = 3
if example == 1:
    # two triangles
    # dis = -2
    polygon1 = np.array([[0, 0], [2, 0], [1, 1]])
    polygon2 = np.array([[1, 0], [3, 0], [2, 1]])
elif example == 2:
    # distance  =2 
    polygon1 = np.array([[0, 0], [0, 2], [-2, 2], [-2,0 ]])
    polygon2 = np.array([[2, 0], [2, 1], [3, 1], [3, 0]])
elif example == 3:
    # distance = 2
    polygon1 = np.array([[0, 0], [0, 2], [-2, 2], [-2,0 ]])
    polygon2 = np.array([[2, -2], [3, -2], [3, 1], [2, 1] ])
    

distance = polygon_distance(polygon1, polygon2)
print("Distance between polygons:", distance)

plt.figure()
plot_polygon(polygon1, 'blue')
plot_polygon(polygon2, 'green')
plt.xlabel('X axis')
plt.ylabel('Y axis')
plt.title('Convex Polygons')
plt.grid(True)
plt.axis('equal')  # Ensure equal scaling for x and y axes
plt.show()