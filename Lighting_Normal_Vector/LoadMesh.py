# Import OpenGL library for 3D graphics rendering.
# Import the pygame library for creating games and multimedia applications.
# Import the Mesh class from the Mesh module.
from Mesh import *


# Define a class named 'LoadMesh' that inherits from the 'Mesh' class.
class LoadMesh(Mesh):
    # Constructor of the LoadMesh class.
    def __init__(self, filename, draw_type):
        # Initialize normals, vertices, and triangles as empty lists.
        self.normals = []
        self.vertices = []
        self.triangles = []
        # Store the filename from which the mesh will be loaded.
        self.filename = filename
        # Set the drawing type (e.g., GL_TRIANGLES, GL_LINES).
        self.draw_type = draw_type
        # Call the method to load mesh data from the file.
        self.load_drawing()

    # Method to load mesh data from a file.
    def load_drawing(self):
        # Open the file in read mode.
        with open(self.filename) as fp:
            # Read the first line from the file.
            line = fp.readline()
            # Continue reading lines until the end of the file.
            while line:
                # If the line starts with 'v', it describes a vertex.
                if line.startswith("v "):
                    # Split the line and convert the vertex coordinates to float.
                    vx, vy, vz = [float(value) for value in line[2:].split()]
                    # Append the vertex tuple to the vertices list.
                    self.vertices.append((vx, vy, vz))

                # If the line starts with 'vn', it describes a normal vector.
                elif line.startswith("vn "):
                    # Split the line and convert the normal vector components to float.
                    nx, ny, nz = [float(value) for value in line[3:].split()]
                    # Append the normal vector tuple to the normals list.
                    self.normals.append((nx, ny, nz))

                # If the line starts with 'f', it describes a face of the mesh.
                elif line.startswith("f "):
                    # Split the line into vertex indices for the face.
                    t1, t2, t3 = [value for value in line[2:].split()]
                    # For each vertex index, extract the position index, convert to int, and adjust for 0-based
                    # indexing.
                    self.triangles.append([int(value) for value in t1.split('/')][0] - 1)
                    self.triangles.append([int(value) for value in t2.split('/')][0] - 1)
                    self.triangles.append([int(value) for value in t3.split('/')][0] - 1)
                # Read the next line in the file.
                line = fp.readline()
