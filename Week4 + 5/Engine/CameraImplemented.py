import pygame.key
from pygame.locals import *
from OpenGL.GLU import *
from Cube import *
from LoadMesh import *
from Camera import *
import time
start_time = time.time()

pygame.init()

# COPIED FROM TransformExplorer.py

# project settings
screen_width = 1000
screen_height = 800
background_color = (0, 0, 0, 1)
drawing_color = (1, 1, 1, 1)

screen = pygame.display.set_mode((screen_width, screen_height), DOUBLEBUF | OPENGL)
pygame.display.set_caption('(Teapot/Cube) Transformations in Python')
cube = Cube(GL_LINE_LOOP)
mesh = LoadMesh("cube.obj", GL_LINE_LOOP)
camera = Camera()

def Light():
    ambientLight = [0.25, 0.25, 0.0, 1.0]
    diffuseLight = [0.9, 0.9, 0.0, 1.0]
    lightPos = [-100.0, 130.0, 150.0, 1.0]
    specular = [1.0, 1.0, 1.0, 1.0]
    specref = [1.0, 1.0, 1.0, 1.0]

    glShadeModel(GL_SMOOTH)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glClearDepth(1.0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_CULL_FACE)
    glFrontFace(GL_CCW)
    glEnable(GL_LIGHTING)

    glLightfv(GL_LIGHT0, GL_AMBIENT, ambientLight)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, diffuseLight)
    glLightfv(GL_LIGHT0, GL_POSITION, lightPos)
    glLightfv(GL_LIGHT0, GL_SPECULAR, specular)
    glEnable(GL_LIGHT0)

    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specref)
    glMateriali(GL_FRONT, GL_SHININESS, 10)
    glDepthFunc(GL_LEQUAL)
    #
    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)

def initialise():
    glClearColor(background_color[0], background_color[1], background_color[2], background_color[3])
    glColor(drawing_color)

    # projection
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60, (screen_width / screen_height), 0.1, 500.0)

    Light() # Implement the light function!

def camera_init():
    # modelview
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    glViewport(0, 0, screen.get_width(), screen.get_height())
    glEnable(GL_DEPTH_TEST)
    camera.update(screen.get_width(), screen.get_height()) # For the mouse to stay in the center

def draw_world_axes():
    glLineWidth(4)
    glBegin(GL_LINES)
    glColor(1, 0, 0) # Red
    glVertex3d(-1000, 0, 0)
    glVertex3d(1000, 0, 0)
    glColor(0, 1, 0) # Blue
    glVertex3d(0, -1000, 0)
    glVertex3d(0, 1000, 0)
    glColor(0, 0, 1) # Green
    glVertex3d(0, 0, -1000)
    glVertex3d(0, 0, 1000)
    glEnd()

    # x positive sphere
    sphere = gluNewQuadric()
    glColor(1, 0, 0)
    glPushMatrix()
    glTranslated(1, 0, 0)
    gluSphere(sphere, 0.05, 10, 10)
    glPopMatrix()

    # y positive sphere
    sphere = gluNewQuadric()
    glColor(0, 0, 1)
    glPushMatrix()
    glTranslated(0, 1, 0)
    gluSphere(sphere, 0.05, 10, 10)
    glPopMatrix()

    # z positive sphere
    sphere = gluNewQuadric()
    glColor(0, 1, 0)
    glPushMatrix()
    glTranslated(0, 0, 1)
    gluSphere(sphere, 0.05, 10, 10)
    glPopMatrix()

    glLineWidth(1)
    glColor(1, 1, 1)

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    camera_init()
    draw_world_axes()

    t = time.time() - start_time
    year_period = 10.0  # 5 seconds for simulating 1 year
    year = (t / year_period)

    # # Push dan Pop itu biar translationnya gak bocor ke cube lain, atau bisa juga diundo translationnya, cek pdf
    # glPushMatrix()
    # glTranslated(1, 0, 0)
    # mesh.draw()
    # glPopMatrix()

    # glPushMatrix()
    # glColor4f(0, 0, 1, 1)
    # glRotatef(year * 360.0, 0.0, 1.0, 0.0)
    # glTranslatef(3.0, 0.0, 0.0)
    # mesh.draw()
    # glPopMatrix()

    day = 360 * year
    moon_sid = (365 / 27.3) * year
    # glPushMatrix()
    # glRotatef(day * 360.0, 0.0, 1.0, 0.0)
    # mesh.draw()
    # glPopMatrix()


    # SUN system
    glColor4f(1.0, 1.0, 0.0, 1) # color of Yellow
    sphere_sun = gluNewQuadric()
    gluSphere(sphere_sun, 0.8, 20, 15) # Sun sphere

    # EARTH system, rotation around the sun
    glPushMatrix()
    glColor4f(0.0, 0.0, 1.0, 1)
    glRotatef(year * 360.0, 0.0, 1.0, 0.0)
    glTranslated(3, 0, 0)
    sphere_earth = gluNewQuadric()
    gluSphere(sphere_earth, 0.3, 10, 8)

    # MOON system
    glPushMatrix()
    glRotatef(moon_sid * 360.0, 0.0, 1.0, 0.0)
    glTranslatef(1, 0, 0)
    # glRotatef(90, 1.0, 0, 0)
    glColor4f(0.4, 0.5, 0.6, 1)
    sphere_moon = gluNewQuadric()
    gluSphere(sphere_moon, 0.1, 10, 8)

    glPopMatrix()
    glPopMatrix() # close both

    # MARS system, rotation around the sun
    glPushMatrix()
    glColor4f(1.0, 0.5, 0.0, 1)
    glRotatef(year * 360.0 / 1.88, 0.0, 1.0, 0.0)
    glTranslated(4.5, 0, 0)
    sphere_mars = gluNewQuadric()
    gluSphere(sphere_mars, 0.2, 10, 8)
    glPopMatrix()

    # JUPITER system, rotating around the Sun
    glPushMatrix()
    glColor4f(1.0, 0.5, 0.0, 1)  # Orange color for Jupiter
    glRotatef(year * 360.0 / 11.86, 0.0, 1.0, 0.0)  # Jupiter's orbit around the Sun (slower than Mars)
    glTranslatef(6.5, 0, 0)  # Set distance of Jupiter from the Sun

    sphere_jupiter = gluNewQuadric()
    gluSphere(sphere_jupiter, 0.5, 15, 12)  # Jupiter sphere

    # Io Moon system, rotating around Jupiter
    glPushMatrix()  # Start Io transformation around Jupiter
    glColor4f(1.0, 0.8, 0.0, 1)  # Yellow-orange color for Io
    glRotatef(year * 360.0 * 12, 0.0, 1.0, 0.0)  # Io's fast orbit around Jupiter
    glTranslatef(0.8, 0, 0)  # Distance of Io from Jupiter
    sphere_io = gluNewQuadric()
    gluSphere(sphere_io, 0.1, 10, 8)  # Io sphere
    glPopMatrix()  # End Io transformation

    # Europa Moon system, rotating around Jupiter
    glPushMatrix()  # Start Europa transformation around Jupiter
    glColor4f(0.8, 0.8, 1.0, 1)  # Pale blue color for Europa
    glRotatef(year * 360.0 * 4, 0.0, 1.0, 0.0)  # Europa's slower orbit around Jupiter
    glTranslatef(1.5, 0, 0)  # Distance of Europa from Jupiter
    sphere_europa = gluNewQuadric()
    gluSphere(sphere_europa, 0.1, 10, 8)  # Europa sphere
    glPopMatrix()  # End Europa transformation

    glPopMatrix()  # End Jupiter transformation around the Sun


done = False
initialise()

# Grab the mouse inside window, hide cursor too
pygame.event.set_grab(True)
pygame.mouse.set_visible(False)

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.mouse.set_visible(True)
                pygame.event.set_grab(False)
            if event.key == K_SPACE:
                pygame.mouse.set_visible(False)
                pygame.event.set_grab(True)

    display()
    pygame.display.flip()
    pygame.time.wait(100)
pygame.quit()