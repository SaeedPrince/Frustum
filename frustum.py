import trimesh
import numpy as np

# Parameters for the frustum
top_radius = 1.0
bottom_radius = 2.0
height = 3.0
sides = 32  # Number of sides for the circular base and top

# Create vertices for the top and bottom circles
theta = np.linspace(0, 2 * np.pi, sides, endpoint=False)
top_circle = np.column_stack((top_radius * np.cos(theta), top_radius * np.sin(theta), np.ones(sides) * height))
bottom_circle = np.column_stack((bottom_radius * np.cos(theta), bottom_radius * np.sin(theta), np.zeros(sides)))

# Combine the vertices
vertices = np.vstack((top_circle, bottom_circle))

# Create faces connecting the top and bottom circles
faces = []
for i in range(sides):
    next_i = (i + 1) % sides
    # Triangle 1 (Top i, bottom i, bottom next_i)
    faces.append([i, sides + i, sides + next_i])
    # Triangle 2 (Top i, bottom next_i, top next_i)
    faces.append([i, sides + next_i, next_i])

# Create the mesh
frustum = trimesh.Trimesh(vertices=vertices, faces=faces)

# Visualize the frustum
frustum.show()
