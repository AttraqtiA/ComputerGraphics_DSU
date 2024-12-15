from OpenGL.GL import *
import pygame

class LoadMesh:
    def __init__(self, filename):
        self.vertices = []
        self.faces = []
        self.load_mesh(filename)

    def load_mesh(self, filename):
        with open(filename, 'r') as f:
            for line in f:
                if line.startswith('v '):
                    vertex = [float(x) for x in line.split()[1:]]
                    self.vertices.append(vertex)
                elif line.startswith('f '):
                    face = [int(x.split('/')[0]) - 1 for x in line.split()[1:]]
                    self.faces.append(face)

    def draw(self):
        glBegin(GL_TRIANGLES)
        for face in self.faces:
            for vertex_index in face:
                if vertex_index < 0 or vertex_index >= len(self.vertices):
                    print(f"Error: Vertex index {vertex_index} is out of range")
                    continue
                vertex = self.vertices[vertex_index]
                glVertex3fv(vertex)
        glEnd()