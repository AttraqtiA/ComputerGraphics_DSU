from OpenGL.GL import *
from Mesh import *


class LoadMesh(Mesh):
    def __init__(self, filename, draw_type):
        self.vertices = []
        self.triangles = []
        self.filename = filename
        self.draw_type = draw_type
        self.load_drawing()

    def load_drawing(self):
        with open(self.filename) as fp:
            line = fp.readline()  # Read a line
            while line:  # Until the line is not None
                if line.startswith("v "):  # Vertex data
                    vx, vy, vz = [float(value) for value in line[2:].split()]
                    self.vertices.append((vx, vy, vz))

                elif line.startswith("f "):  # Face data
                    # Split face line into vertex indices
                    face_indices = [value.split('/')[0] for value in line[2:].split()]
                    if len(face_indices) < 3:
                        print("Invalid face: less than 3 vertices.")
                        continue

                    # Convert to triangle fan for faces with >3 vertices
                    for i in range(1, len(face_indices) - 1):
                        t1 = int(face_indices[0]) - 1
                        t2 = int(face_indices[i]) - 1
                        t3 = int(face_indices[i + 1]) - 1
                        self.triangles.extend([t1, t2, t3])

                # Ignore other data like vt (texture coordinates) or vn (vertex normals)
                line = fp.readline()  # Read the next line

