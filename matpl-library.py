import trimesh
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np

# The same frustum creation code
top_radius = 1.0
bottom_radius = 2.0
height = 3.0
sides = 32

theta = np.linspace(0, 2 * np.pi, sides, endpoint=False)
top_circle = np.column_stack((top_radius * np.cos(theta), top_radius * np.sin(theta), np.ones(sides) * height))
bottom_circle = np.column_stack((bottom_radius * np.cos(theta), bottom_radius * np.sin(theta), np.zeros(sides)))

vertices = np.vstack((top_circle, bottom_circle))
faces = []
for i in range(sides):
    next_i = (i + 1) % sides
    faces.append([i, sides + i, sides + next_i])
    faces.append([i, sides + next_i, next_i])

frustum = trimesh.Trimesh(vertices=vertices, faces=faces)

# Plot using matplotlib
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot each triangle
for face in frustum.faces:
    tri = frustum.vertices[face]
    poly = Poly3DCollection([tri], color='cyan', alpha=0.7)
    ax.add_collection3d(poly)

ax.auto_scale_xyz([vertices[:, 0].min(), vertices[:, 0].max()],
                  [vertices[:, 1].min(), vertices[:, 1].max()],
                  [vertices[:, 2].min(), vertices[:, 2].max()])

plt.show()
