import pygame.key
from pygame.locals import *
from OpenGL.GLU import *
from Cube import *
from LoadMesh import *

pygame.init()

# project settings
screen_width = 1000
screen_height = 800
background_color = (0, 0, 0, 1)
drawing_color = (1, 1, 1, 1)

screen = pygame.display.set_mode((screen_width, screen_height), DOUBLEBUF | OPENGL)
pygame.display.set_caption('Transformations in Python')
cube = Cube(GL_LINE_LOOP)
mesh = LoadMesh("cube.obj", GL_LINE_LOOP)

eye = [0, 4, 5] # starting eye position!

def initialise():
    glClearColor(background_color[0], background_color[1], background_color[2], background_color[3])
    glColor(drawing_color)

    # projection
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60, (screen_width / screen_height), 0.1, 500.0)

def init_camera():
    # modelview
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    # glTranslated(1, 1, -2) # modifying the Camera's x, y, and z~
    glViewport(0, 0, screen.get_width(), screen.get_height())
    glEnable(GL_DEPTH_TEST)
    gluLookAt(eye[0], eye[1], eye[2], 0, 0, 0, 0, 1, 0)  # to move the camera back in the positive z direction (or facing us)
    # 0, 4, 5 --> move in positive z direction
    # 0, 0, 0 --> look at the (0, 0, 0) point
    # 0, 1, 0 --> camera is facing up in the Y axis


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    init_camera()
    glPushMatrix()

    # Now we make 2 cubes! (ORIGINAL material pdf)
    mesh.draw()
    glTranslated(0, 1, -5) # applying the camera translate to the NEXT cube
    glRotated(45, 0, 0, 1) # This would touch the cube, rotating it 45 degree around z-axis
    glScalef(0.5, 2, 1) # scaling the cube, making it into balok, etc

    mesh.draw()
    glPopMatrix()


    # # The assignment asked for 3 cubes
    # # Draw 3 cubes, where the first cube sits at (0,0,-2)
    # # second cube sits at (1,1,-3), third cube sits at (-0.5,-0.5,-4).
    # glTranslated(0, 0, -2) # applying the camera translate to the NEXT cube
    # mesh.draw()
    # glTranslated(1, 1, -1) # matrix multiplication!
    # mesh.draw()
    # glTranslated(-1.5, -1.5, -1)
    # mesh.draw()

    # glPopMatrix()


done = False
initialise()
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    # adding key to move the camera
    keys = pygame.key.get_pressed()
    if keys[pygame.K_DOWN]:
        eye[2] += 1

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        eye[2] -= 1

    display()
    pygame.display.flip()
    pygame.time.wait(100)
pygame.quit()