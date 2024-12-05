import pygame.key
from pygame.locals import *
from OpenGL.GLU import *
from LoadMesh import *
from Camera import *
import random

import time
start_time = time.time()

pygame.init()
font = pygame.font.Font("PokemonFont.ttf", 24)  # Load Pokémon font

def render_text(text, x, y, size=24):
    surface = font.render(text, True, (255, 255, 255))  # White color
    text_data = pygame.image.tostring(surface, "RGBA", True)
    width, height = surface.get_size()

    # Normalize coordinates
    normalized_x = (x / screen_width) * 2 - 1
    normalized_y = (y / screen_height) * 2 - 1

    glRasterPos2f(normalized_x, normalized_y)
    glDrawPixels(width, height, GL_RGBA, GL_UNSIGNED_BYTE, text_data)


screen_width = 1000
screen_height = 800
background_color = (0, 0, 0, 1)
drawing_color = (1, 1, 1, 1)

screen = pygame.display.set_mode((screen_width, screen_height), DOUBLEBUF | OPENGL)
pygame.display.set_caption('Pokemon in Python')
pokeball_mesh = LoadMesh("pokeball.obj", GL_LINE_LOOP)
pokemon_mesh = LoadMesh("nyao.obj", GL_LINE_LOOP)
camera = Camera()

def Light():
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    # Sunlight properties
    light_position = [1.0, 1.0, 1.0, 0.0]  # Directional light
    light_diffuse = [1.0, 1.0, 0.8, 1.0]  # Warm sunlight
    light_ambient = [0.3, 0.3, 0.3, 1.0]
    light_specular = [1.0, 1.0, 1.0, 1.0]

    glLightfv(GL_LIGHT0, GL_POSITION, light_position)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)

    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

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

def draw_score(score):
    glColor3f(1, 1, 0)  # Yellow color
    # Use text rendering library to draw score at the top-left
    render_text(f"Score: {score}", x=10, y=screen_height - 30)  # Top-left corner


def show_caught_message():
    glColor3f(1, 0, 0)  # Red color
    render_text("Pokémon Caught!", x=screen_width // 2, y=screen_height // 2)  # Center


import random

# List of Pokémon models
pokemon_models = ["nyao.obj"]

# Initial Pokémon position
pokemon_position = [random.uniform(-10, 10), random.uniform(-10, 10), random.uniform(-10, 10)]

# Current Pokémon model
current_pokemon = random.choice(pokemon_models)

pokeball_position = [0, -1, 0]
pokeball_speed = 0.1
pokeball_thrown = False

def display():
    global pokeball_position, pokeball_thrown, pokemon_position, current_pokemon, score

    score = 0

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    camera_init()
    draw_world_axes()

    # Draw Pokémon
    glPushMatrix()
    glTranslatef(*pokemon_position)
    pokemon_mesh = LoadMesh(current_pokemon, GL_LINE_LOOP)  # Dynamically load the model
    pokemon_mesh.draw()
    glPopMatrix()

    # Draw Pokéball
    glPushMatrix()
    glTranslatef(*pokeball_position)
    glColor4f(1, 0, 0, 1)  # Red color for Pokéball
    pokeball_mesh.draw()
    glPopMatrix()

    # Move Pokéball if thrown
    if pokeball_thrown:
        pokeball_position[1] += pokeball_speed
        if pokeball_position[1] > 3:  # Reset after throwing
            pokeball_position = [0, -1, 0]
            pokeball_thrown = False

    # Collision Detection
    if (abs(pokeball_position[0] - pokemon_position[0]) < 0.5 and
            abs(pokeball_position[1] - pokemon_position[1]) < 0.5 and
            abs(pokeball_position[2] - pokemon_position[2]) < 0.5):
        # Show "Pokémon Caught!" message
        show_caught_message()

        # Update Pokémon position and model
        pokemon_position = [random.uniform(-10, 10), random.uniform(-10, 10), random.uniform(-10, 10)]
        current_pokemon = random.choice(pokemon_models)

        # Reset pokeball state
        pokeball_thrown = False

        # Increment score (assuming a global or passed variable `score`)
        score += 1


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
            if event.key == K_SPACE and not pokeball_thrown:
                pokeball_thrown = True

    display()
    pygame.display.flip()
    pygame.time.wait(100)
pygame.quit()