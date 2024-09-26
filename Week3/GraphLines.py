import math
import numpy as np
import pygame
from pygame.locals import *  # key pressing, key capture, etc
from OpenGL.GL import *
from OpenGL.GLU import *
from Utils import *  # Assuming this has the map_value function

pygame.init()

screen_width = 500
screen_height = 400
ortho_width = 4
ortho_height = 1
ortho_left = 0
ortho_right = 4
ortho_top = -1
ortho_bottom = 1

screen = pygame.display.set_mode((screen_width, screen_height), DOUBLEBUF | OPENGL)
pygame.display.set_caption('OpenGL in Python: Draw Lines')

# Initialize the orthogonal projection
def init_ortho():
    glMatrixMode(GL_PROJECTION)  # Set camera to Projection mode
    glLoadIdentity()  # Clean everything done before
    gluOrtho2D(ortho_left, ortho_right, ortho_top, ortho_bottom)  # Set OpenGL window coordinates

# Plot the points (dots)
def plot_point():
    glBegin(GL_POINTS)
    for p in lines:
        glVertex2i(p[0], p[1])
    glEnd()

# Plot lines connecting the points with GL_LINES & GL_LINE_LOOP & GL_LINE_STRIP
def plot_lines():
    for l in lines:
        glBegin(GL_LINE_STRIP)
        for coords in l:
            glVertex2f(coords[0], coords[1])
        glEnd()

def plot_graph():
    glBegin(GL_POINTS)
    px : GL_DOUBLE
    py : GL_DOUBLE
    for px in np.arange(0, 4, 0.005):  # original
        py = math.exp(-px) * math.cos(2 * math.pi * px)
        glVertex2f(px, py)

    glEnd()

# Mapping function to map screen coordinates (Pygame) to OpenGL coordinates
def map_value(from_min, from_max, to_min, to_max, value):
    return to_min + (to_max - to_min) * ((value - from_min) / (from_max - from_min))


init_ortho()

done = False
lines = []  # Array to save the dots' history
line = []
mouse_down = False

while not done:
    p = None
    for event in pygame.event.get():  # Actively check for status / event in the last loop
        if event.type == pygame.QUIT:
            done = True
        elif event.type == MOUSEBUTTONDOWN: # MOUSEBUTTONDOWN or MOUSEMOTION
            mouse_down = True
            line = [] # resets the line
            lines.append(line)
        elif event.type == MOUSEBUTTONUP:
            mouse_down = False
        elif event.type == MOUSEMOTION and mouse_down:
            p = pygame.mouse.get_pos()
            mapped_x = map_value(0, screen_width, ortho_left, ortho_right, p[0])
            mapped_y = map_value(0, screen_height, ortho_bottom, ortho_top, p[1])
            line.append((mapped_x, mapped_y))

    # Clear screen
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)  # Set matrix for model view
    glLoadIdentity()  # Clear matrix for model view (identity)

    # Plot the lines based on points added
    plot_graph()

    pygame.display.flip()  # Put the content which was drawn in the buffer to the display
    # pygame.time.wait(100)  # removed for smoother line

pygame.quit()
