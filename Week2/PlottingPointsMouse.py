import math
import numpy as np
import pygame

from pygame.locals import * # key pressing, key capture, etc

from OpenGL.GL import *
from OpenGL.GLU import *

pygame.init()

screen_width = 500
screen_height = 400

#Display the screen
screen = pygame.display.set_mode((screen_width, screen_height), DOUBLEBUF | OPENGL)
# DOUBLEBUF is important!

pygame.display.set_caption('OpenGL in Python :3')

# We need to make a main_FromProf loop, so that it wont immediately close the window

def init_ortho():
    glMatrixMode(GL_PROJECTION) # Set camera to Projection mode
    glLoadIdentity() # clean everything done before
    # gluOrtho2D(-250, 250, -200, 200) # for the 2 dots with plot_graph
    gluOrtho2D(0, 500, 400, 0) # Setting window coordinates

    # LEFT, RIGHT, BOTTOM, TOP

done = False

init_ortho()

# GIVEN PROBLEM TO SOLVE
# Now, run again: the points are not disappearing. But, the positions are flipped in the Y
# direction.
# This is because pygame has the (0,0) point at the upper left corner, while pyOpenGL has the
# (0,0) point at the lower left corner.
# How can we solve this problem?

glPointSize(5)

points = [] # Array to save the dots history

def plot_point():
    glBegin(GL_POINTS)
    for p in points: # looping through the array, translating it to visible dots
        glVertex2i(p[0], p[1])
    glEnd()

while not done:
    for event in pygame.event.get(): # actively check for status / event in the last loop
        if event.type == pygame.QUIT:
            done = True
        elif event.type == MOUSEBUTTONDOWN:
            points.append(pygame.mouse.get_pos())

    # Added code, to add the x = 100 and y = 40 line
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW) # Set matrix for model view
    glLoadIdentity() # clear matrix for model view, i.e., set it to identity

    plot_point()

    pygame.display.flip() #  put the content which was drawn in the buffer to the display
    pygame.time.wait(100) # check status every 100 milliseconds
pygame.quit()

