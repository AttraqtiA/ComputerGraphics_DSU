import pygame
from pygame.locals import * # key pressing, key capture, etc
from OpenGL.GL import *
from OpenGL.GLU import *
from Utils import *

pygame.init()

screen_width = 500
screen_height = 400
ortho_width = 640
ortho_height = 480

screen = pygame.display.set_mode((screen_width, screen_height), DOUBLEBUF | OPENGL)

pygame.display.set_caption('OpenGL in Python :3')

def init_ortho():
    glMatrixMode(GL_PROJECTION) # Set camera to Projection mode
    glLoadIdentity() # clean everything done before
    # gluOrtho2D(-250, 250, -200, 200) # for the 2 dots with plot_graph
    gluOrtho2D(0, ortho_width, 0, ortho_height) # Setting window coordinates

    # LEFT, RIGHT, BOTTOM, TOP

done = False

init_ortho()

glPointSize(5)

points = [] # Array to save the dots history

def plot_point():
    glBegin(GL_POINTS)
    for p in points: # looping through the array, translating it to visible dots
        glVertex2f(p[0], p[1])
    glEnd()

while not done:
    p = None
    for event in pygame.event.get(): # actively check for status / event in the last loop
        if event.type == pygame.QUIT:
            done = True
        elif event.type == MOUSEBUTTONDOWN:
            p = pygame.mouse.get_pos()
            mapped_x = map_value(0, screen_width, 0, ortho_width, p[0])
            mapped_y = map_value(0, screen_height, 0, ortho_height, screen_height - p[1])
            points.append((mapped_x, mapped_y))

    # Added code, to add the x = 100 and y = 40 line
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW) # Set matrix for model view
    glLoadIdentity() # clear matrix for model view, i.e., set it to identity

    plot_point()

    pygame.display.flip() #  put the content which was drawn in the buffer to the display
    pygame.time.wait(100) # check status every 100 milliseconds
pygame.quit()

