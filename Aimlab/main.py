import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from LoadMesh import LoadMesh
import random
from Camera import FPSCamera

# Initialize pygame and font
pygame.init()
font = pygame.font.Font(None, 36)

# Screen and rendering settings
screen_width, screen_height = 1200, 600
screen = pygame.display.set_mode((screen_width, screen_height), DOUBLEBUF | OPENGL)
pygame.display.set_caption('AimLab-ish FPS Game')

# Game variables
pokemon_mesh = LoadMesh("cube.obj")  # Your target model (cube.obj)
target_position = [random.uniform(-10, 10), random.uniform(-3, 3), random.uniform(-10, -20)]
score = 0
game_over = False
shooting = False

# FPS camera setup
camera = FPSCamera(position=(0, 0, -5))  # Set initial camera position

# OpenGL setup (initialization)
def initialise():
    glClearColor(0.0, 0.6, 1.0, 1)  # Set background color (sky blue)
    glEnable(GL_DEPTH_TEST)  # Enable depth testing for 3D
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, (screen_width / screen_height), 0.1, 50.0)  # Set perspective projection
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()  # Reset modelview matrix

# Draw the target (cube)
def draw_target(x, y, z):
    glPushMatrix()
    glTranslatef(x, y, z)
    glScalef(1.0, 1.0, 1.0)  # Size of the cube
    glColor3f(1.0, 0.0, 0.0)  # Red color for the target
    glBegin(GL_QUADS)
    for v in [
        [-0.5, -0.5, -0.5],
        [0.5, -0.5, -0.5],
        [0.5, 0.5, -0.5],
        [-0.5, 0.5, -0.5],
    ]:
        glVertex3fv(v)
    glEnd()
    glPopMatrix()

# Shooting logic
def shoot():
    global target_position, score
    # Simple distance check to detect shooting (within range of target)
    dist = pygame.Vector3(camera.position.x - target_position[0], camera.position.y - target_position[1], camera.position.z - target_position[2])
    if dist.length() < 2:  # Check if the player is close enough to the target (within range)
        # Reposition the target after it's shot
        target_position = [random.uniform(-10, 10), random.uniform(-3, 3), random.uniform(-10, -20)]
        score += 1

# Render text
def render_text(text, x, y):
    surface = font.render(text, True, (255, 255, 255))
    text_data = pygame.image.tostring(surface, "RGBA", True)
    glRasterPos2f((x / screen_width) * 2 - 1, 1 - (y / screen_height) * 2)
    glDrawPixels(*surface.get_size(), GL_RGBA, GL_UNSIGNED_BYTE, text_data)

# Main game loop
def display():
    global game_over, score

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Apply camera movement
    camera.update(pygame.key.get_pressed(), 0.1, pygame.mouse.get_rel())

    # Draw target
    draw_target(target_position[0], target_position[1], target_position[2])

    # Display score
    render_text(f"Score: {score}", 10, 10)

    if game_over:
        render_text("Game Over!", screen_width // 2 - 100, screen_height // 2)

    pygame.display.flip()

# Main loop
initialise()
running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN:
            if event.key == K_SPACE and not game_over:
                shooting = True

    if shooting:
        shoot()  # Call shooting logic
        shooting = False  # Reset shooting flag

    display()
    pygame.time.wait(50)  # Control game speed (frame rate)

pygame.quit()
