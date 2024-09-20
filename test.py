import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np


def plot_reflections():
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Define the initial vector A
    A = np.array([1, 1, 1])

    # Define mirrors (normal vectors)
    mirror_x = np.array([1, 0, 0])
    mirror_y = np.array([0, 1, 0])
    mirror_z = np.array([0, 0, 1])

    # Calculate the reflections
    B = A - 2 * np.dot(A, mirror_x) * mirror_x
    C = B - 2 * np.dot(B, mirror_y) * mirror_y
    D = C - 2 * np.dot(C, mirror_z) * mirror_z

    # Plot initial vector A
    ax.quiver(0, 0, 0, A[0], A[1], A[2], color='r', label='Initial Vector A', linewidth=2)

    # Plot reflection B
    ax.quiver(A[0], A[1], A[2], B[0] - A[0], B[1] - A[1], B[2] - A[2], color='g', label='After 1st Reflection B',
              linewidth=2)

    # Plot reflection C
    ax.quiver(A[0], A[1], A[2], C[0] - A[0], C[1] - A[1], C[2] - A[2], color='b', label='After 2nd Reflection C',
              linewidth=2)

    # Plot reflection D
    ax.quiver(A[0], A[1], A[2], D[0] - A[0], D[1] - A[1], D[2] - A[2], color='m', label='After 3rd Reflection D',
              linewidth=2)

    # Plot mirrors (planes)
    xx, yy = np.meshgrid(np.linspace(-2, 2, 10), np.linspace(-2, 2, 10))

    # Plane perpendicular to x-axis (yz-plane)
    ax.plot_surface(np.zeros_like(xx), xx, yy, alpha=0.2, color='gray')

    # Plane perpendicular to y-axis (xz-plane)
    ax.plot_surface(xx, np.zeros_like(yy), yy, alpha=0.2, color='gray')

    # Plane perpendicular to z-axis (xy-plane)
    ax.plot_surface(xx, yy, np.zeros_like(xx), alpha=0.2, color='gray')

    # Set labels
    ax.set_xlabel('X axis')
    ax.set_ylabel('Y axis')
    ax.set_zlabel('Z axis')

    # Set limits
    ax.set_xlim([-2, 2])
    ax.set_ylim([-2, 2])
    ax.set_zlim([-2, 2])

    # Set legend
    ax.legend()

    plt.show()


plot_reflections()
