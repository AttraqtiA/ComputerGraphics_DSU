# Import the OpenGL library for rendering 3D graphics.
from OpenGL.GL import *

# Define a class named 'Mesh' to represent a 3D mesh object.
class Mesh:
    # The constructor (__init__) method is called when an instance of Mesh is created.
    def __init__(self):
        # Define the vertices of the mesh. Each vertex is a tuple of 3 elements (x, y, z).
        self.vertices = [
            (0.5, -0.5, 0.5),
            (-0.5, -0.5, 0.5),
            (0.5, 0.5, 0.5),
            (-0.5, 0.5, 0.5),
            (0.5, 0.5, -0.5),
            (-0.5, 0.5, -0.5)
        ]
        # Define the indices of the vertices that make up each triangle of the mesh.
        self.triangles = [0, 2, 3, 0, 3, 1]
        # Set the type of drawing for the mesh, in this case, a line loop.
        self.draw_type = GL_LINE_LOOP
        # Initialize an empty list for normals (used for lighting and shading).
        self.normals = []

    # Define the draw method to render the mesh.
    def draw(self):
        # Loop through the triangles array in steps of 3, as each triangle has 3 vertices.
        for t in range(0, len(self.triangles), 3):
            # Begin drawing with the specified draw type (GL_LINE_LOOP).
            glBegin(self.draw_type)
            # Iterate over the three vertices of each triangle.
            for i in range(3):
                # Get the index of the vertex in the vertices list.
                index = self.triangles[t + i]
                # Check if a normal vector is defined for this vertex.
                if len(self.normals) > index:  # Check if normal exists
                    # Set the normal vector for this vertex.
                    glNormal3fv(self.normals[index])
                # Define the position of the vertex.
                glVertex3fv(self.vertices[index])
            # End the drawing of the current triangle.
            glEnd()
