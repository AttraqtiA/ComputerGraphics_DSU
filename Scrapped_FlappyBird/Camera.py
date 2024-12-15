import pygame
from OpenGL.GLU import *

class Camera:
    def __init__(self):
        # Position the camera for a fixed side-view angle
        self.eye = pygame.math.Vector3(0, 0, 10)  # Fixed distance from the scene
        self.look = pygame.math.Vector3(0, 0, -5)  # Look at the gameplay area
        self.up = pygame.math.Vector3(0, 1, 0)  # Up direction remains consistent

    def update(self):
        # Set the camera to always view from the side without player control
        gluLookAt(
            self.eye.x, self.eye.y, self.eye.z,  # Camera position
            self.look.x, self.look.y, self.look.z,  # Where the camera looks
            self.up.x, self.up.y, self.up.z,  # Up direction
        )
