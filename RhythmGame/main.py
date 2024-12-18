import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from Note import Note
from Chart import chart
from LoadMesh import LoadMesh
from colorama import Fore, Style

import time

# Initialize Pygame and GLUT
pygame.init()

# Screen settings
screen_width = 840
screen_height = 520
background_color = (1, 1, 1, 1)
drawing_color = (1, 1, 1, 1)

# Start display
screen = pygame.display.set_mode((screen_width, screen_height), DOUBLEBUF | OPENGL)
pygame.display.set_caption('Rhythm Game in OpenGL')

arrowMesh = LoadMesh('arrow.obj')
arrow_lane = 1  # Start at Lane 1

# Global variables
notes = []  # To hold notes
start_time = time.time()
eye = [0, 0, 2.5]  # Starting camera position
combo = 0
accuracy = ""  # Text feedback: Perfect, Miss, etc.
lane_accuracies = {1: "", 2: "", 3: "", 4: ""}  # 4 lanes
score = 0
rank_colors = {
    "All Perfect": Fore.LIGHTYELLOW_EX,
    "S": Fore.YELLOW,
    "A": Fore.MAGENTA,
    "B": Fore.BLUE,
}

def check_collision(note, lane):
    global combo, score
    target_x = -1.3
    current_time = time.time() - start_time
    time_difference = abs(note.x - target_x)

    if abs(note.x - target_x) < 0.4 and note.lane == lane:
        time_difference_ms = time_difference * 1000
        if time_difference_ms < 200:
            note.score = 500
            lane_accuracies[lane] = Fore.YELLOW + "Perfect!" + Style.RESET_ALL
        elif time_difference_ms < 300:
            note.score = 400
            lane_accuracies[lane] = Fore.MAGENTA + "Great!" + Style.RESET_ALL
        elif time_difference_ms < 400:
            note.score = 300
            lane_accuracies[lane] = Fore.GREEN + "Good!" + Style.RESET_ALL
        else:
            lane_accuracies[lane] = Fore.RED + "Miss!" + Style.RESET_ALL
            return False

        score += note.score
        combo += 1
        print(f"Score: {score}, Combo: {combo}, Accuracy: {lane_accuracies[lane]}")
        return True
    return False

def remove_missed_notes():
    global combo, accuracy
    missed_notes = []  # List of notes that were missed

    current_time = time.time()  # Get the current time

    for note in notes:
        if note.x < -1.2 and not note.hit:  # Note is out of range and hasn't been hit
            if note.missed_time is None:  # If it's the first time missing the note
                note.missed_time = current_time  # Set the time when it was missed

            # 100ms before note disappears
            if current_time - note.missed_time > 0.1:
                missed_notes.append(note)  # Add to the missed notes list

    # Handle missed notes after the delay
    if missed_notes:
        accuracy = Fore.RED + "Miss!" + Style.RESET_ALL
        combo = 0  # Reset combo when a note is missed
        for note in missed_notes:
            notes.remove(note)  # Remove the note after the delay
        print(f"Score: {score}, Combo: {combo} | Accuracy: {accuracy}")

def calculate_rank(total_score, max_possible_score):
    percentage = (total_score / max_possible_score) * 100
    if percentage == 100:
        return "All Perfect"
    elif percentage >= 90:
        return "S"
    elif percentage >= 80:
        return "A"
    else:
        return "B"

def handle_input():
    global arrow_lane
    keys = pygame.key.get_pressed()
    hit_this_frame = False  # Flag to track if we've already hit a note this frame

    if keys[pygame.K_a]:  # Lane 1
        arrow_lane = 1  # Move arrow to Lane 1
        for note in notes:
            if not note.hit and not hit_this_frame and check_collision(note, lane=1):  # Only hit once per frame per note
                note.hit = True
                hit_this_frame = True
                break  # Once we hit one note, stop checking the others in this frame

    if keys[pygame.K_d]:  # Lane 2
        arrow_lane = 2
        for note in notes:
            if not note.hit and not hit_this_frame and check_collision(note, lane=2):
                note.hit = True
                hit_this_frame = True
                break

    if keys[pygame.K_j]:  # Lane 3
        arrow_lane = 3
        for note in notes:
            if not note.hit and not hit_this_frame and check_collision(note, lane=3):
                note.hit = True
                hit_this_frame = True
                break

    if keys[pygame.K_l]:  # Lane 4
        arrow_lane = 4
        for note in notes:
            if not note.hit and not hit_this_frame and check_collision(note, lane=4):
                note.hit = True
                hit_this_frame = True
                break

def draw_gradient_background():
    glDisable(GL_DEPTH_TEST)  # Disable depth testing for background
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(0, 1, 0, 1, -1, 1)  # Set up 2D orthographic projection

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    glBegin(GL_QUADS)
    # Top vertices (lighter gray)
    glColor3f(0.9, 0.9, 0.9)  # Light gray
    glVertex2f(0, 1)          # Top-left
    glVertex2f(1, 1)          # Top-right

    # Bottom vertices (darker gray)
    glColor3f(0.5, 0.5, 0.5)  # Darker gray
    glVertex2f(1, 0)          # Bottom-right
    glVertex2f(0, 0)          # Bottom-left
    glEnd()

    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glEnable(GL_DEPTH_TEST)  # Re-enable depth testing

def draw_lane_dividers():
    glColor3f(0, 0, 0)  # Black color for the dividers

    dividers = [
        1.0,
        0.5,
        0.0,
        -0.5,
        -1.0
    ]

    glPushMatrix()
    for y_pos in dividers:
        glBegin(GL_QUADS)
        # Draw a thin horizontal rectangle as the divider
        glVertex3f(-1.5, y_pos + 0.01, 0.1)  # Left-top
        glVertex3f(2.5, y_pos + 0.01, 0.1)   # Right-top
        glVertex3f(2.5, y_pos - 0.01, 0.1)   # Right-bottom
        glVertex3f(-1.5, y_pos - 0.01, 0.1)  # Left-bottom
        glEnd()
    glPopMatrix()

def Light():
    ambientLight = [0.25, 0.25, 0.25, 1.0]
    diffuseLight = [0.9, 0.9, 0.9, 1.0]
    lightPos = [-100.0, 130.0, 150.0, 1.0]
    specular = [1.0, 1.0, 1.0, 1.0]
    specref = [1.0, 1.0, 1.0, 1.0]

    glShadeModel(GL_SMOOTH)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    glLightfv(GL_LIGHT0, GL_AMBIENT, ambientLight)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, diffuseLight)
    glLightfv(GL_LIGHT0, GL_POSITION, lightPos)
    glLightfv(GL_LIGHT0, GL_SPECULAR, specular)

    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specref)
    glMateriali(GL_FRONT, GL_SHININESS, 32)  # Adjust shininess for effect

def initialise():
    glClearColor(*background_color)
    glColor(*drawing_color)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60, (screen_width / screen_height), 0.1, 500.0)
    Light()

def init_camera():
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glViewport(0, 0, screen.get_width(), screen.get_height())
    glEnable(GL_DEPTH_TEST)
    gluLookAt(eye[0], eye[1], eye[2], 0, 0, 0, 0, 1, 0)

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    draw_gradient_background()
    draw_lane_dividers()

    init_camera()

    quadric = gluNewQuadric()

    # Draw the arrow beside the lanes
    glPushMatrix()
    glDisable(GL_LIGHTING)
    # Determine Y position based on the current lane
    arrow_y_pos = 0.75 if arrow_lane == 1 else 0.25 if arrow_lane == 2 else -0.25 if arrow_lane == 3 else -0.75
    glTranslatef(-2.0, arrow_y_pos, 0)
    glRotatef(90, 1, 0, 0)
    glScalef(0.002, 0.002, 0.002) # original obj file is too large
    glColor3f(0.0, 1.0, 1.0)
    arrowMesh.draw()
    glEnable(GL_LIGHTING) # ENABLE LIGHTING for the next sphere renders
    glPopMatrix()

    # LANE 1
    if lane_accuracies[1] == Fore.YELLOW + "Perfect!" + Style.RESET_ALL:
        lane1_color = (1, 1, 0)  # Yellow for Perfect
    elif lane_accuracies[1] == Fore.MAGENTA + "Great!" + Style.RESET_ALL:
        lane1_color = (0.5, 0, 0.5)  # Purple for Great
    elif lane_accuracies[1] == Fore.GREEN + "Good!" + Style.RESET_ALL:
        lane1_color = (0, 1, 0)  # Green for Good
    else:
        lane1_color = (0, 0, 1)  # Blue for default (Miss or no hit yet)

    glColor3f(*lane1_color)
    glPushMatrix()
    glTranslatef(-1.3, 0.75, 0)  # Lane 1 target position
    gluSphere(quadric, 0.2, 20, 20)
    glPopMatrix()

    # LANE 2
    if lane_accuracies[2] == Fore.YELLOW + "Perfect!" + Style.RESET_ALL:
        lane2_color = (1, 1, 0)
    elif lane_accuracies[2] == Fore.MAGENTA + "Great!" + Style.RESET_ALL:
        lane2_color = (0.5, 0, 0.5)
    elif lane_accuracies[2] == Fore.GREEN + "Good!" + Style.RESET_ALL:
        lane2_color = (0, 1, 0)
    else:
        lane2_color = (0, 0, 1)

    glColor3f(*lane2_color)
    glPushMatrix()
    glTranslatef(-1.3, 0.25, 0)
    gluSphere(quadric, 0.2, 20, 20)
    glPopMatrix()

    # LANE 3
    if lane_accuracies[3] == Fore.YELLOW + "Perfect!" + Style.RESET_ALL:
        lane3_color = (1, 1, 0)
    elif lane_accuracies[3] == Fore.MAGENTA + "Great!" + Style.RESET_ALL:
        lane3_color = (0.5, 0, 0.5)
    elif lane_accuracies[3] == Fore.GREEN + "Good!" + Style.RESET_ALL:
        lane3_color = (0, 1, 0)
    else:
        lane3_color = (0, 0, 1)

    glColor3f(*lane3_color)
    glPushMatrix()
    glTranslatef(-1.3, -0.25, 0)
    gluSphere(quadric, 0.2, 20, 20)
    glPopMatrix()

    # LANE 4
    if lane_accuracies[4] == Fore.YELLOW + "Perfect!" + Style.RESET_ALL:
        lane4_color = (1, 1, 0)
    elif lane_accuracies[4] == Fore.MAGENTA + "Great!" + Style.RESET_ALL:
        lane4_color = (0.5, 0, 0.5)  # Purple for Great
    elif lane_accuracies[4] == Fore.GREEN + "Good!" + Style.RESET_ALL:
        lane4_color = (0, 1, 0)
    else:
        lane4_color = (0, 0, 1)

    glColor3f(*lane4_color)
    glPushMatrix()
    glTranslatef(-1.3, -0.75, 0)
    gluSphere(quadric, 0.2, 20, 20)
    glPopMatrix()

    # Add new notes based on the chart and timing
    current_time = time.time() - start_time
    for note_data in chart:
        if not note_data.get("spawned") and current_time >= note_data["time"]:
            y_pos = 0.75 if note_data["lane"] == 1 else 0.25 if note_data["lane"] == 2 else -0.25 if note_data["lane"] == 3 else -0.75
            notes.append(Note(note_data["lane"], y_pos=y_pos))
            note_data["spawned"] = True

    # Update and draw notes
    for note in notes:
        if not note.hit:
            note.update_position()
            note.draw()


# Main loop
done = False
initialise()
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    handle_input()
    remove_missed_notes()
    display()
    pygame.display.flip()
    pygame.time.wait(10)

    # Check if all notes are hit or missed
    if all(note.hit or note.x < -1.2 for note in notes) and len(notes) == len(chart):
        done = True
        max_possible_score = len(chart) * 500
        rank = calculate_rank(score, max_possible_score)
        print(f"Final Score: {score}/{max_possible_score}, Max Combo: {combo}, Rank: {rank_colors[rank]}{rank}{Style.RESET_ALL}")

# Close the game
pygame.quit()