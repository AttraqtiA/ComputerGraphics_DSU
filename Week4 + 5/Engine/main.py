import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from Mesh import *
from Cube import *
from Pyramid import *
from LoadMesh import *

pygame.init()

# project settings
screen_width = 1000
screen_height = 800
background_color = (0, 0, 0, 1)
drawing_color = (1, 1, 1, 1)

screen = pygame.display.set_mode((screen_width, screen_height), DOUBLEBUF | OPENGL)
pygame.display.set_caption('OpenGL in Python')

# mesh = Mesh() # Declare object/class
#cube = Cube(GL_LINE_LOOP) # GL_POLYGON for solid / filled cube
# pyramid = Pyramid(GL_LINE_LOOP)
loadMesh = LoadMesh("donut.obj", GL_LINE_LOOP)

def initialise():
    glClearColor(background_color[0], background_color[1], background_color[2], background_color[3])
    glColor(drawing_color)

    # projection
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60, (screen_width / screen_height), 0.1, 1000.0)

    # modelview
    glMatrixMode(GL_MODELVIEW)
    glTranslate(0, 0, -5)
    glLoadIdentity()
    glViewport(0, 0, screen.get_width(), screen.get_height())
    glEnable(GL_DEPTH_TEST)
    glTranslate(0, -1, -5)


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glRotatef(1, 10, 0, 1)
    glPushMatrix()

    # cube.draw()
    loadMesh.draw()
    # pyramid.draw()

    glPopMatrix()


done = False
initialise()
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    display()
    pygame.display.flip()
    pygame.time.wait(100)
pygame.quit()