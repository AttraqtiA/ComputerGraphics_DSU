import numpy as np
import pygame
from pygame.locals import *  # key pressing, key capture, etc
from OpenGL.GL import *
from OpenGL.GLU import *
from Utils import *  # Assuming this has the map_value function

pygame.init()

screen_width = 500
screen_height = 400
ortho_width = 640
ortho_height = 480

screen = pygame.display.set_mode((screen_width, screen_height), DOUBLEBUF | OPENGL)
pygame.display.set_caption('OpenGL in Python: POLYGONS EDITION')

# Initialize the orthogonal projection
def init_ortho():
    glMatrixMode(GL_PROJECTION)  # Set camera to Projection mode
    glLoadIdentity()  # Clean everything done before
    gluOrtho2D(0, ortho_width, 0, ortho_height)  # Set OpenGL window coordinates

done = False

init_ortho()

points = []  # Array to save the dots' history

# Plot polygon connecting points
def plot_polygon():
    glColor(0, 1, 0, 1) # Adds color GREEN
    glBegin(GL_TRIANGLES) # GL_POLYGON & GL_TRIANGLES & GL_TRIANGLE_STRIP
    for p in points:  # Looping through the array, translating it to visible dots
        glVertex2f(p[0], p[1])
    glEnd()
    glColor(1, 0, 0, 1) # Color RED
    for i in np.arange(0, len(points) - 2, 3): # i iterates through 0, 3, 6, 9
        glBegin(GL_LINE_LOOP)
        glVertex2f(points[i][0], points[i][1]) # first vertex of triangle
        glVertex2f(points[i + 1][0], points[i + 1][1]) # second
        glVertex2f(points[i + 2][0], points[i + 2][1]) # third
        glEnd()

glLineWidth(3)

# def plot_polygon(): # This one would make it expand on every click after 3, just uncomment it if u forget
#     glColor(0, 1, 0, 1) # Adds color GREEN
#     glBegin(GL_TRIANGLE_FAN) # GL_TRIANGLE_FAN
#     for p in points:
#         glVertex2f(p[0], p[1])
#     glEnd()

# Quads or 4 sisi bangun datar
# def plot_polygon():
#     glColor(0, 1, 0, 1) # Adds color GREEN
#     glBegin(GL_QUADS) # GL_QUADS & GL_QUAD_STRIP
#     for p in points:
#         glVertex2f(p[0], p[1])
#     glEnd()

# Correct mapping function for Y-axis inversion
def map_value(from_min, from_max, to_min, to_max, value):
    return to_min + (to_max - to_min) * ((value - from_min) / (from_max - from_min))

while not done:
    p = None
    for event in pygame.event.get():  # Actively check for status / event in the last loop
        if event.type == pygame.QUIT:
            done = True
        elif event.type == MOUSEBUTTONDOWN:
            p = pygame.mouse.get_pos()

            # OpenGL: The origin (0,0) is at the BOTTOM-LEFT corner, and Y increases as you move up.
            mapped_x = map_value(0, screen_width, 0, ortho_width, p[0])
            mapped_y = map_value(0, screen_height, 0, ortho_height, screen_height - p[1])
            points.append((mapped_x, mapped_y))

    # Clear screen
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)  # Set matrix for model view
    glLoadIdentity()  # Clear matrix for model view (identity)

    plot_polygon()  # Plot the polygon based on points added

    pygame.display.flip()  # Put the content which was drawn in the buffer to the display
    pygame.time.wait(100)  # Check status every 100 milliseconds

pygame.quit()
