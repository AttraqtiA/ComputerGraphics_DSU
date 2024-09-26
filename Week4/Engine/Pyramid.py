from OpenGL.GL import *
import pygame
from Mesh import *

class Pyramid(Mesh):
    def __init__(self, draw_type):
        self.vertices = [
            (0.5, -0.5, 0.5),   # Base front-right (0)
            (-0.5, -0.5, 0.5),  # Base front-left (1)
            (-0.5, -0.5, -0.5), # Base back-left (2)
            (0.5, -0.5, -0.5),  # Base back-right (3)
            (0.0, 0.5, 0.0)     # Apex (4)
        ]
        self.triangles = [
            0, 1, 4,  # Front
            1, 2, 4,  # Left
            2, 3, 4,  # Back
            3, 0, 4,  # Right

            # Base
            0, 1, 2,  # Base triangle 1
            0, 2, 3  # Base triangle 2
        ]
        self.draw_type = draw_type

    def draw(self):
        for t in range(0, len(self.triangles), 3):
            glBegin(self.draw_type)
            glVertex3fv(self.vertices[self.triangles[t]])
            glVertex3fv(self.vertices[self.triangles[t + 1]])
            glVertex3fv(self.vertices[self.triangles[t + 2]])
            glEnd()
