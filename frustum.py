import numpy as np
import trimesh

def create_frustum(center_pos, h, r1, r2, sides=12):
    """
    Creates a frustum using trimesh with smooth side faces and outward-pointing normals.

    Parameters:
    - center_pos: Tuple[float, float, float] -> The center position of the top face.
    - h: float -> The height of the frustum.
    - r1: float -> The radius of the top face (larger circle).
    - r2: float -> The radius of the bottom face (smaller circle).
    - sides: int -> The number of sides for the regular polygon (default: 12).
    
    Returns:
    - trimesh.Trimesh object representing the frustum.
    """
    
    # Decompose center position
    center_x, center_y, center_z = center_pos
    
    # Generate theta angles for regular polygons
    theta = np.linspace(0, 2 * np.pi, sides, endpoint=False)
    
    # Top and bottom face vertices
    top_vertices = np.column_stack((r1 * np.cos(theta) + center_x,
                                    r1 * np.sin(theta) + center_y,
                                    np.ones(sides) * (center_z + h)))
    
    bottom_vertices = np.column_stack((r2 * np.cos(theta) + center_x,
                                       r2 * np.sin(theta) + center_y,
                                       np.ones(sides) * center_z))
    
    # Combine vertices
    vertices = np.vstack((top_vertices, bottom_vertices))
    
    # Faces for the side walls
    faces = []
    for i in range(sides):
        next_i = (i + 1) % sides
        # Triangle 1: side face (top, bottom, next bottom)
        faces.append([i, sides + i, sides + next_i])
        # Triangle 2: side face (top, next bottom, next top)
        faces.append([i, sides + next_i, next_i])
    
    # Create triangles for top face (fan triangulation)
    top_center = len(vertices)
    vertices = np.vstack((vertices, [center_x, center_y, center_z + h]))  # Center of the top face
    for i in range(sides):
        next_i = (i + 1) % sides
        faces.append([top_center, i, next_i])
    
    # Create triangles for bottom face (fan triangulation)
    bottom_center = len(vertices)
    vertices = np.vstack((vertices, [center_x, center_y, center_z]))  # Center of the bottom face
    for i in range(sides):
        next_i = (i + 1) % sides
        faces.append([bottom_center, sides + next_i, sides + i])

    # Create the mesh
    frustum = trimesh.Trimesh(vertices=vertices, faces=faces)

    # Ensure outward normals for top and bottom
    frustum.fix_normals()
    
    # Smooth the normals for the side faces for a natural appearance
    frustum.face_normals = trimesh.util.unitize(frustum.face_normals)
    
    return frustum


def rotate_frustum(frustum_mesh, axis, angle_deg):
    """
    Rotates the frustum around the specified axis by a given angle.

    Parameters:
    - frustum_mesh: trimesh.Trimesh -> The frustum mesh to rotate.
    - axis: str -> The axis around which to rotate ('x', 'y', or 'z').
    - angle_deg: float -> The angle of rotation in degrees.
    
    Returns:
    - trimesh.Trimesh object with the applied rotation.
    """
    # Convert angle from degrees to radians
    angle_rad = np.radians(angle_deg)
    
    # Create the rotation matrix based on the axis
    if axis == 'x':
        rotation_matrix = trimesh.transformations.rotation_matrix(angle_rad, [1, 0, 0])
    elif axis == 'y':
        rotation_matrix = trimesh.transformations.rotation_matrix(angle_rad, [0, 1, 0])
    elif axis == 'z':
        rotation_matrix = trimesh.transformations.rotation_matrix(angle_rad, [0, 0, 1])
    else:
        raise ValueError("Axis must be one of 'x', 'y', or 'z'")
    
    # Apply the rotation to the mesh
    frustum_mesh.apply_transform(rotation_matrix)
    
    return frustum_mesh


# Example usage:
center_pos = (0, 0, 0)  # Center at the origin
h = 5.0  # Height of the frustum
r1 = 4.0  # Top radius (larger circle)
r2 = 2.0  # Bottom radius (smaller circle)

# Create the frustum mesh
frustum_mesh = create_frustum(center_pos, h, r1, r2)

# Apply a 60-degree rotation to get a better bottom view
frustum_mesh = rotate_frustum(frustum_mesh, axis='x', angle_deg=60)

# Visualize the frustum in trimesh
frustum_mesh.show()
