import pygame
from OpenGL.raw.WGL.ARB.buffer_region import WGL_DEPTH_BUFFER_BIT_ARB

from pygame.locals import * # key pressing, key capture, etc

from OpenGL.GL import *
from OpenGL.GLU import *

pygame.init()

screen_width = 1000
screen_height = 800

#Display the screen
screen = pygame.display.set_mode((screen_width, screen_width), DOUBLEBUF | OPENGL)
# DOUBLEBUF is important!

pygame.display.set_caption('OpenGL in Python :3')

# We need to make a main loop, so that it wont immediately close the window

def init_ortho():
    glMatrixMode(GL_PROJECTION) # Set camera to Projection mode
    glLoadIdentity() # clean everything done before
    gluOrtho2D(0, 320, 0, 300) # Setting window coordinates

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

    glPointSize(5) # set point size to 5
    glBegin(GL_POINTS)
    glVertex2i(100, 40)
    glEnd()

    pygame.display.flip() #  put the content which was drawn in the buffer to the display
    pygame.time.wait(100) # check status every 100 milliseconds
pygame.quit()

