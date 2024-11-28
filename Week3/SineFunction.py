# Draw a graph of the following equation
# y = sin(x)/x   for x=0.1, 0.2, 0.3,....4
# Take a screenshot of the result and upload it here

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

pygame.display.set_caption('OpenGL in Python: sin(x)/x Graph')

# We need to make a main_FromProf loop, so that it wont immediately close the window

def init_ortho():
    glMatrixMode(GL_PROJECTION) # Set camera to Projection mode
    glLoadIdentity() # clean everything done before
    gluOrtho2D(0, 4, -1, 1) # Setting window coordinates

    # LEFT, RIGHT, BOTTOM, TOP

def plot_graph():
    glBegin(GL_POINTS)
    px : GL_DOUBLE
    py : GL_DOUBLE
    for px in np.arange(0.1, 4, 0.1):  # x = 0.1, 0.2, 0.3,....4
        py = math.sin(px) / px
        glVertex2f(px, py)

    glEnd()

done = False

init_ortho()

while not done:
    for event in pygame.event.get(): # actively check for status / event in the last loop
        if event.type == pygame.QUIT:
            done = True

    # Added code, to add the x = 100 and y = 40 line
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW) # Set matrix for model view
    glLoadIdentity() # clear matrix for model view, i.e., set it to identity

    plot_graph()

    glPointSize(3) # set point size to 5

    pygame.display.flip() #  put the content which was drawn in the buffer to the display
    pygame.time.wait(100) # check status every 100 milliseconds
pygame.quit()

