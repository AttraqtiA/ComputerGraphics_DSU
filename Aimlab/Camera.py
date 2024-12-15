# camera.py
import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
import math

class FPSCamera:
    def __init__(self, position, speed=0.1, sensitivity=0.2):
        self.position = pygame.Vector3(position)  # Position of the camera
        self.speed = speed  # Speed of movement
        self.sensitivity = sensitivity  # Mouse sensitivity
        self.pitch = 0  # Vertical rotation (up and down)
        self.yaw = -90  # Horizontal rotation (left and right)
        self.mouse_x, self.mouse_y = 0, 0  # Store mouse position

    def update(self, keys, delta_time, mouse_delta):
        # Handle mouse look
        self.mouse_x, self.mouse_y = mouse_delta
        self.yaw += self.mouse_x * self.sensitivity
        self.pitch -= self.mouse_y * self.sensitivity
        self.pitch = max(-90, min(90, self.pitch))  # Clamp pitch

        # Handle keyboard movement (W, A, S, D, Space, Shift for jumping)
        if keys[pygame.K_w]:
            self.position += self._get_direction() * self.speed * delta_time
        if keys[pygame.K_s]:
            self.position -= self._get_direction() * self.speed * delta_time
        if keys[pygame.K_a]:
            self.position -= self._get_right() * self.speed * delta_time
        if keys[pygame.K_d]:
            self.position += self._get_right() * self.speed * delta_time
        if keys[pygame.K_SPACE]:
            self.position[1] += self.speed * delta_time  # Jump (upward)
        if keys[pygame.K_LSHIFT]:
            self.position[1] -= self.speed * delta_time  # Crouch (downward)

        self._update_view()

    def _update_view(self):
        glRotatef(self.pitch, 1, 0, 0)  # Apply pitch rotation
        glRotatef(self.yaw, 0, 1, 0)    # Apply yaw rotation
        glTranslatef(-self.position.x, -self.position.y, -self.position.z)  # Move camera position

    def _get_direction(self):
        """ Return the direction vector based on current yaw. """
        radian_yaw = math.radians(self.yaw)
        return pygame.Vector3(math.cos(radian_yaw), 0, math.sin(radian_yaw))

    def _get_right(self):
        """ Return the right vector based on current yaw. """
        radian_yaw = math.radians(self.yaw)
        return pygame.Vector3(math.sin(radian_yaw), 0, -math.cos(radian_yaw))
