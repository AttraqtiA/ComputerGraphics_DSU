import pygame
from pygame.locals import *  # key pressing, key capture, etc
from OpenGL.GL import *
from OpenGL.GLU import *
from Utils import *  # Assuming this has the map_value function

pygame.init()

screen_width = 500
screen_height = 400
ortho_width = 640
ortho_height = 480

screen = pygame.display.set_mode((screen_width, screen_height), DOUBLEBUF | OPENGL)
pygame.display.set_caption('OpenGL in Python: Draw Lines')

# Initialize the orthogonal projection
def init_ortho():
    glMatrixMode(GL_PROJECTION)  # Set camera to Projection mode
    glLoadIdentity()  # Clean everything done before
    gluOrtho2D(0, ortho_width, 0, ortho_height)  # Set OpenGL window coordinates

# Plot the points (dots)
def plot_point():
    glBegin(GL_POINTS)
    for p in lines:
        glVertex2i(p[0], p[1])
    glEnd()

# Plot lines connecting the points with GL_LINES & GL_LINE_LOOP & GL_LINE_STRIP
def plot_lines():
    for l in lines:
        glBegin(GL_LINE_STRIP)
        for coords in l:
            glVertex2f(coords[0], coords[1])
        glEnd()

def save_drawing():
    f = open("drawing.txt", "w") # open a file for writing
    f.write(str(len(lines)) + "\n") # wrtites the number of lines drawn
    for l in lines:
        f.write(str(len(l)) + "\n") # writes the number of points in the line drawn
        for coords in l:
            f.write(str(coords[0]) + " " + str(coords[1]) + "\n") # writes the coordinates of the line
    f.close() # close the file
    print("Drawing Saved") # saving the file!

def load_drawing():
    f = open("drawing.txt", "r") # open the file for reading
    num_of_lines = int(f.readline()) # read in the number of lines
    global lines
    global line
    lines = []
    line = []

    for l in range(num_of_lines):
        line=[]
        lines.append(line)
        num_of_coords = int(f.readline()) # get the number of coords in the line
        for coord_number in range(num_of_coords): # loop through the points in the line
            px, py = [float(value) for value in next(f).split()]
            line.append((px, py))
            print(str(px) + ", " + str(py))

# Mapping function to map screen coordinates (Pygame) to OpenGL coordinates
def map_value(from_min, from_max, to_min, to_max, value):
    return to_min + (to_max - to_min) * ((value - from_min) / (from_max - from_min))


init_ortho()

done = False
lines = []  # Array to save the dots' history
line = []
mouse_down = False

while not done:
    p = None
    for event in pygame.event.get():  # Actively check for status / event in the last loop
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s: # SAVE when key S is pressed!
                save_drawing()
            if event.key == pygame.K_l: # LOAD the previous saved drawing when key L is pressed!
                load_drawing()
            if event.key == pygame.K_SPACE: # CLEAR everything when Spacebar is pressed
                lines = []
        elif event.type == MOUSEBUTTONDOWN: # MOUSEBUTTONDOWN or MOUSEMOTION
            mouse_down = True
            line = [] # resets the line
            lines.append(line)
        elif event.type == MOUSEBUTTONUP:
            mouse_down = False
        elif event.type == MOUSEMOTION and mouse_down:
            p = pygame.mouse.get_pos()
            mapped_x = map_value(0, screen_width, 0, ortho_width, p[0])
            mapped_y = map_value(0, screen_height, 0, ortho_height, screen_height - p[1])
            line.append((mapped_x, mapped_y))

    # Clear screen
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)  # Set matrix for model view
    glLoadIdentity()  # Clear matrix for model view (identity)

    # Plot the lines based on points added
    plot_lines()

    pygame.display.flip()  # Put the content which was drawn in the buffer to the display
    # pygame.time.wait(100)  # removed for smoother line

pygame.quit()
