import pygame.key
from pygame.locals import *
from OpenGL.GLU import *
from OpenGL.GL import *
from OpenGL.GLUT import * # applying texture
from LoadMesh import *
from Camera import *
import time
start_time = time.time()

pygame.init()

# Project settings & variables
screen_width = 1440
screen_height = 720
background_color = (0, 0, 0, 1)
drawing_color = (1, 1, 1, 1)

screen = pygame.display.set_mode((screen_width, screen_height), DOUBLEBUF | OPENGL)
pygame.display.set_caption('Space Fighter Game')
gunMesh = LoadMesh("laser_gun.obj", GL_TRIANGLES)
crosshair_texture = load_texture("crosshair.png")

camera = Camera()

# Track bullets (cylinders)
bullets = []

class Bullet:
    def __init__(self, position, direction, speed=0.2):
        self.position = list(position)  # Start position (x, y, z)
        self.direction = direction  # Normalized direction (dx, dy, dz)
        self.speed = speed  # Speed of the bullet

    def update(self):
        # Move the bullet forward in the direction
        self.position[0] += self.direction[0] * self.speed
        self.position[1] += self.direction[1] * self.speed
        self.position[2] += self.direction[2] * self.speed

    def draw(self):
        # Draw the bullet as a small cylinder using gluCylinder
        quadric = gluNewQuadric()
        glPushMatrix()
        glTranslatef(*self.position)  # Move to the bullet's position
        glColor3f(1.0, 0.0, 0.0)  # Red bullet
        glRotatef(-90, 1, 0, 0)  # Align cylinder along Z-axis
        gluCylinder(quadric, 0.05, 0.05, 0.5, 16, 16)  # Base radius, top radius, height, slices, stacks
        glPopMatrix()
        gluDeleteQuadric(quadric)  # Clean up the quadric object


def load_texture(file_path):
    texture_surface = pygame.image.load(file_path).convert_alpha()  # Preserve transparency
    texture_data = pygame.image.tostring(texture_surface, "RGBA", True)
    width, height = texture_surface.get_size()

    glEnable(GL_TEXTURE_2D)
    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)

    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    return texture_id


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

    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)


def render_crosshair(texture_id):
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)  # Handle transparency

    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(0, screen_width, 0, screen_height, -1, 1)

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, texture_id)

    # Position and size
    x = screen_width // 2
    y = screen_height // 2
    crosshair_size = 16

    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex2f(x - crosshair_size, y - crosshair_size)  # Bottom-left
    glTexCoord2f(1, 0); glVertex2f(x + crosshair_size, y - crosshair_size)  # Bottom-right
    glTexCoord2f(1, 1); glVertex2f(x + crosshair_size, y + crosshair_size)  # Top-right
    glTexCoord2f(0, 1); glVertex2f(x - crosshair_size, y + crosshair_size)  # Top-left
    glEnd()

    glDisable(GL_TEXTURE_2D)
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

    glDisable(GL_BLEND)  # Disable blending after drawing


def shoot_bullet():
    # Gun position and direction
    gun_position = [0, 0, -3]  # Adjust based on gun's position
    bullet_direction = [0, 0, -1]  # Forward direction in view space
    bullets.append(Bullet(gun_position, bullet_direction))


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

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    camera_init()

    # # Gun on the FPS POV position
    # glPushMatrix()
    #
    # glScalef(1, 1, 1)
    # # Bottom-right corner of the screen
    # glTranslatef(0.6, -0.3, -4)
    # glRotatef(-90, 0, 1, 0)
    # # render_gun_with_texture(gunMesh, load_texture("laser_gun_diffuse.png"))  # Use the texture
    # gunMesh.draw()
    #
    # glPopMatrix()

    # Render bullets
    for bullet in bullets:
        bullet.draw()

    # Render crosshair
    # render_crosshair(crosshair_texture)


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
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                shoot_bullet()

    # Update bullets
    for bullet in bullets:
        bullet.update()

    # Remove bullets that go out of view
    bullets = [bullet for bullet in bullets if bullet.position[2] > -50]

    display()
    pygame.display.flip()
    pygame.time.wait(10)

pygame.quit()