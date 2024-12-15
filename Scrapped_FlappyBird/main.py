import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from LoadMesh import LoadMesh
import random

# Initialize pygame and font
pygame.init()
font = pygame.font.Font(None, 36)  # Use a default font for now

# Screen and rendering settings
screen_width, screen_height = 1200, 600
screen = pygame.display.set_mode((screen_width, screen_height), DOUBLEBUF | OPENGL)
pygame.display.set_caption('Flappy Pokémon')

# Load assets
pokemon_mesh = LoadMesh("cube.obj")

# Game variables
pokemon_position = [0, 0, -5]  # Initial position
gravity = 0.005
flap_strength = 0.1
vertical_velocity = 0
pillar_gap = 2.5  # Adjusted gap for better playability
pillar_width = 0.5
pillars = []
score = 0
game_over = False
restart_delay = 2000  # Delay before restart in milliseconds


# Initialize OpenGL
def initialise():
    glClearColor(0.0, 0.6, 1.0, 1)  # Sky blue background
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, (screen_width / screen_height), 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    Light()


# Lighting setup
def Light():
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    light_position = [10.0, 10.0, 5.0, 1.0]
    light_diffuse = [1.0, 1.0, 1.0, 1.0]
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)


# Render text
def render_text(text, x, y):
    surface = font.render(text, True, (255, 255, 255))
    text_data = pygame.image.tostring(surface, "RGBA", True)
    glRasterPos2f((x / screen_width) * 2 - 1, 1 - (y / screen_height) * 2)
    glDrawPixels(*surface.get_size(), GL_RGBA, GL_UNSIGNED_BYTE, text_data)


# Draw a pillar
def draw_pillar(x, height, y_offset):
    glPushMatrix()
    glTranslatef(x, y_offset, pokemon_position[2])
    glScalef(pillar_width, height, 1)
    glColor3f(0.3, 0.8, 0.3)  # Green pillars
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


# Reset the game
def reset_game():
    global pokemon_position, vertical_velocity, pillars, score, game_over
    pokemon_position = [0, 0, -5]
    vertical_velocity = 0
    pillars = []
    score = 0
    game_over = False
    glClearColor(0.0, 0.6, 1.0, 1)  # Reset background color


# Main game loop
def display():
    global pokemon_position, vertical_velocity, pillars, score, game_over

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Draw Pokémon
    glPushMatrix()
    glTranslatef(*pokemon_position)
    pokemon_mesh.draw()
    glPopMatrix()

    # Apply gravity and update position
    if not game_over:
        vertical_velocity -= gravity
        pokemon_position[1] += vertical_velocity

    # Generate new pillars
    if not pillars or pillars[-1][0] < 8:
        # Ensure the gap appears fully within the screen height
        max_gap_offset = 2  # Adjust this value for playability
        gap_start = random.uniform(-max_gap_offset, max_gap_offset)
        pillars.append([10, 6, gap_start, False])  # [x-position, height, gap_start, scored_flag]

    # Draw pillars and move them
    for pillar in pillars:
        pillar[0] -= 0.03  # Speed of the bird moving!
        top_height = 4 - (pillar[2] + pillar_gap / 2)  # Top pillar height
        bottom_height = 4 + (pillar[2] - pillar_gap / 2)  # Bottom pillar height

        # Top pillar (starts from the gap upwards)
        draw_pillar(pillar[0], top_height, pillar[2] + pillar_gap / 2)

        # Bottom pillar (starts from the bottom up to the gap)
        draw_pillar(pillar[0], bottom_height, -4)

    # Remove off-screen pillars
    pillars = [p for p in pillars if p[0] > -10]

    # Check for collisions
    for pillar in pillars:
        if abs(pokemon_position[0] - pillar[0]) < pillar_width:
            if pokemon_position[1] < pillar[2] - (pillar[1] + pillar_gap) or pokemon_position[1] > pillar[2]:
                game_over = True

    # Check for out-of-bounds
    if pokemon_position[1] < -4 or pokemon_position[1] > 4:
        game_over = True

    # Update score
    if not game_over:
        for pillar in pillars:
            if not pillar[3] and pillar[0] < pokemon_position[0]:
                pillar[3] = True
                score += 1

    # Display score and game-over message
    render_text(f"Score: {score}", 10, 10)
    if game_over:
        glClearColor(1.0, 0.0, 0.0, 1)  # Red background for game-over
        render_text("Game Over!", screen_width // 2 - 100, screen_height // 2)

    pygame.display.flip()


# Main loop
initialise()
running = True
last_game_over_time = None
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN:
            if event.key == K_SPACE and not game_over:
                vertical_velocity = flap_strength

    # Automatically restart after game-over delay
    if game_over:
        if last_game_over_time is None:
            last_game_over_time = pygame.time.get_ticks()
        elif pygame.time.get_ticks() - last_game_over_time > restart_delay:
            reset_game()
            last_game_over_time = None

    display()
    pygame.time.wait(10)

pygame.quit()