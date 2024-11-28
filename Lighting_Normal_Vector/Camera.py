# Import the pygame library for creating games and multimedia applications.
import pygame
# Import the GLU module from the OpenGL library for utility functions.
from OpenGL.GLU import *
# Import mathematical functions from the math module.
from math import *

# Define a class named 'Camera' to represent a camera in a 3D space.
class Camera:
    # Constructor of the Camera class.
    def __init__(self):
        # Initialize the camera's position in the 3D space.
        self.eye = pygame.math.Vector3(0, 0, 0)
        # Set the camera's up direction (usually along the y-axis).
        self.up = pygame.math.Vector3(0, 1, 0)
        # Set the camera's right direction (usually along the x-axis).
        self.right = pygame.math.Vector3(1, 0, 0)
        # Set the camera's forward direction (initially pointing along the z-axis).
        self.forward = pygame.math.Vector3(0, 0, 5)
        # Determine where the camera is looking at by adding the forward vector to the eye position.
        self.look = self.eye + self.forward
        # Initialize the yaw (rotation around the y-axis) and pitch (rotation around the x-axis) angles.
        self.yaw = -90
        self.pitch = 0
        # Store the last mouse position.
        self.last_mouse = pygame.math.Vector2(0, 0)
        # Set the sensitivity of the mouse movement.
        self.mouse_sensitivityX = 0.1
        self.mouse_sensitivityY = 0.1
        # Set the sensitivity for camera movement through keyboard keys.
        self.key_sensitivity = 0.001

    # Define the method to rotate the camera based on yaw and pitch angles.
    def rotate(self, yaw, pitch):
        # Update the yaw and pitch based on the input.
        self.yaw += yaw
        self.pitch += pitch

        # Clamp the pitch angle to prevent flipping the camera upside down.
        if self.pitch > 89.00:
            self.pitch = 89.00
        if self.pitch < -89.00:
            self.pitch = -89.00

        # Update the forward vector based on the new yaw and pitch angles.
        self.forward.x = cos(radians(self.yaw)) * cos(radians(self.pitch))
        self.forward.y = sin(radians(self.pitch))
        self.forward.z = sin(radians(self.yaw)) * cos(radians(self.pitch))
        # Normalize the forward vector to ensure it's a unit vector.
        self.forward = self.forward.normalize()

        # Recalculate the right and up vectors based on the new forward vector.
        self.right = self.forward.cross(pygame.Vector3(0, 1, 0)).normalize()
        self.up = self.right.cross(self.forward).normalize()

    # Define the method to update the camera's position and orientation.
    def update(self, w, h):
        # Return if the mouse is visible (not capturing mouse events).
        if pygame.mouse.get_visible():
            return
        # Get the current mouse position.
        mouse_pos = pygame.mouse.get_pos()
        # Calculate the change in mouse position.
        mouse_change = self.last_mouse - pygame.math.Vector2(mouse_pos)
        # Reset the mouse position to the center of the window.
        pygame.mouse.set_pos(w / 2, h / 2)
        # Update the last mouse position.
        self.last_mouse = pygame.mouse.get_pos()

        # Rotate the camera based on the change in mouse position and sensitivity settings.
        self.rotate(mouse_change.x * self.mouse_sensitivityX, mouse_change.y * self.mouse_sensitivityY)

        # Handle keyboard input for moving the camera.
        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN]:
            self.eye -= self.forward * self.key_sensitivity * 400
        if keys[pygame.K_UP]:
            self.eye += self.forward * self.key_sensitivity * 400
        if keys[pygame.K_RIGHT]:
            self.eye += self.right * self.key_sensitivity * 400
        if keys[pygame.K_LEFT]:
            self.eye -= self.right * self.key_sensitivity * 400

        # Update the look-at point of the camera.
        self.look = self.eye + self.forward
        # Set the camera's position and orientation in the OpenGL context.
        gluLookAt(self.eye.x, self.eye.y, self.eye.z,
                  self.look.x, self.look.y, self.look.z,
                  self.up.x, self.up.y, self.up.z)
