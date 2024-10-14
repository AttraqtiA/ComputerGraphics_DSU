import pygame
from OpenGL.GLU import *
from math import *

class Camera:
    def __init__(self):
        self.eye = pygame.math.Vector3(0, 0, -10)
        self.up = pygame.math.Vector3(0, 1, 0)
        self.right = pygame.math.Vector3(1, 0, 0) # direction to camera's right
        self.forward = pygame.math.Vector3(0, 0, 1) # camera's looking direction
        self.look = self.eye + self.forward
        self.yaw = -90
        self.pitch = 0
        self.last_mouse = pygame.math.Vector2(0, 0)

    def rotate(self, yaw, pitch):
        self.yaw += yaw
        self.pitch += pitch
        self.forward.x = cos(radians(self.yaw)) * cos(radians(self.pitch))
        self.forward.y = sin(radians(self.pitch))
        self.forward.z = sin(radians(self.yaw)) * cos(radians(self.pitch))
        self.forward = self.forward.normalize()
        self.right = self.forward.cross(pygame.Vector3(0, 1, 0)).normalize()
        self.up = self.right.cross(self.forward).normalize()

    def update(self):
        # Mouse rotation implementation with yaw, pitch, and roll
        mouse_pos = pygame.mouse.get_pos()
        mouse_change = self.last_mouse - pygame.math.Vector2(mouse_pos)
        self.last_mouse = mouse_pos

        self.rotate(mouse_change.x, mouse_change.y)

        # Arrow keys
        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN]:
            self.eye -= self.forward
        if keys[pygame.K_UP]:
            self.eye += self.forward
        if keys[pygame.K_RIGHT]:
            self.eye += self.right
        if keys[pygame.K_LEFT]:
            self.eye -= self.right

        # Update camera position AFTER the eye has moved
        self.look = self.eye + self.forward
        gluLookAt(self.eye.x, self.eye.y, self.eye.z,
                  self.look.x, self.look.y, self.look.z,
                  self.up.x, self.up.y, self.up.z)



