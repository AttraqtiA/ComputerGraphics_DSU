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

# We need to make a main loop, so that it wont immediately close the window

def init_ortho():
    glMatrixMode(GL_PROJECTION) # Set camera to Projection mode
    glLoadIdentity() # clean everything done before
    # gluOrtho2D(-250, 250, -200, 200) # for the 2 dots with plot_graph
    gluOrtho2D(0, 50, 0, 40) # Setting window coordinates

    # LEFT, RIGHT, BOTTOM, TOP

def plot_graph():
    glBegin(GL_POINTS)
    glVertex2f(0, 0)
    glEnd()

done = False

init_ortho()

glPointSize(50)

while not done:
    for event in pygame.event.get(): # actively check for status / event in the last loop
        if event.type == pygame.QUIT:
            done = True

    # Added code, to add the x = 100 and y = 40 line
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW) # Set matrix for model view
    glLoadIdentity() # clear matrix for model view, i.e., set it to identity

    plot_graph()

    glPointSize(5) # set point size to 5

    # [!] WHAT YOU WANT TO DRAW, PUT IT BETWEEN glBegin and glEnd
    glBegin(GL_POINTS)
    glVertex2i(25, 20)
    glVertex2i(25, 10)
    glVertex2i(15, 20)

    glEnd()

    pygame.display.flip() #  put the content which was drawn in the buffer to the display
    pygame.time.wait(100) # check status every 100 milliseconds
pygame.quit()

