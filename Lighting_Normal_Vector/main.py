# Import time module for tracking time-related tasks.
import time
# Import constants from pygame.locals for easier use of pygame's features.
from pygame.locals import *
# Import the Camera and LoadMesh classes from their respective modules.
from Camera import *
from LoadMesh import *

# Record the start time of the program.
start_time = time.time()

# Initialize the pygame library.
pygame.init()

# Define settings for the window and rendering.
screen_width = 1000
screen_height = 800
background_color = (0, 0, 0, 1)  # RGBA color for the background
drawing_color = (1, 1, 1, 1)  # RGBA color for the drawing

# Set up the display mode for pygame with OpenGL and double buffering.
screen = pygame.display.set_mode((screen_width, screen_height), DOUBLEBUF | OPENGL)
# Set the window title.
pygame.display.set_caption('OpenGL in Python')
# Create a new LoadMesh instance for loading a mesh file.
mesh = LoadMesh("teapot.obj", GL_POLYGON)
# Create a new Camera instance.
camera = Camera()


# Function to initialize OpenGL settings.
def initialise():
    # Set the clear color for OpenGL.
    glClearColor(background_color[0], background_color[1], background_color[2], background_color[3])
    # Set the color for drawing.
    glColor(drawing_color)

    # Set up the projection matrix for 3D rendering.
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    # Set the perspective for the 3D projection.
    gluPerspective(60, (screen_width / screen_height), 0.1, 100.0)
    # Call the function to set up lighting.
    Light()


# Function to set up lighting in the scene.
def Light():
    # Define various lighting properties.
    ambientLight = [0.2, 0.2, 0, 1]
    diffuseLight = [0.9, 0.2, 0.2]
    specular = [1, 1, 1, 1]
    specref = [1, 1, 1, 1]
    lightPos = [-100, 130, 150, 1]
    # Set up the lighting model and enable various OpenGL features.
    glShadeModel(GL_SMOOTH)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_CULL_FACE)
    glFrontFace(GL_CCW)
    glEnable(GL_LIGHTING)
    # Configure and enable the light source.
    glLightfv(GL_LIGHT0, GL_AMBIENT, ambientLight)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, diffuseLight)
    glLightfv(GL_LIGHT0, GL_SPECULAR, specular)
    glLightfv(GL_LIGHT0, GL_POSITION, lightPos)
    glEnable(GL_LIGHT0)
    # Enable color materials and set material properties.
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specref)
    glMateriali(GL_FRONT, GL_SHININESS, 10)


# Function to initialize the camera settings.
def camera_init():
    # Set up the modelview matrix.
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glViewport(0, 0, screen.get_width(), screen.get_height())
    glEnable(GL_DEPTH_TEST)
    # Update the camera with the current screen dimensions.
    camera.update(screen.get_width(), screen.get_height())


# Function to draw the world axes for reference.
def draw_world_axes():
    # Draw the X, Y, and Z axes with different colors.
    glLineWidth(4)
    glBegin(GL_LINES)
    # X axis in red
    glColor(1, 0, 0)
    glVertex3d(-1000, 0, 0)
    glVertex3d(1000, 0, 0)
    # Y axis in green
    glColor(0, 1, 0)
    glVertex3d(0, -1000, 0)
    glVertex3d(0, 1000, 0)
    # Z axis in blue
    glColor(0, 0, 1)
    glVertex3d(0, 0, -1000)
    glVertex3d(0, 0, 1000)
    glEnd()
    # Draw small spheres at the positive ends of the axes.
    glColor(1, 0, 0)  # Red sphere for X axis
    draw_sphere(1, 0, 0)
    glColor(0, 1, 0)  # Green sphere for Y axis
    draw_sphere(0, 1, 0)
    glColor(0, 0, 1)  # Blue sphere for Z axis
    draw_sphere(0, 0, 1)
    glLineWidth(1)
    glColor(1, 1, 1)  # Reset the drawing color


# Function to draw a sphere at a given position.
def draw_sphere(x, y, z):
    sphere = gluNewQuadric()
    glPushMatrix()
    glTranslated(x, y, z)
    gluSphere(sphere, 0.05, 10, 10)
    glPopMatrix()


# Function to handle the rendering and display.
def display():
    # Clear the color and depth buffers.
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    # Initialize the camera.
    camera_init()
    # Draw the world axes.
    draw_world_axes()

    # Calculate the elapsed time since the start of the program.
    t = time.time() - start_time
    year_period = 5.0
    year = (t / year_period)
    # Perform a rotation transformation based on the elapsed time.
    glPushMatrix()
    glRotatef(year * 360.0, 0.0, 1.0, 0.0)  # Rotate around the Y axis
    # Draw the loaded mesh.
    mesh.draw()
    glPopMatrix()


# Main loop of the program.
done = False
initialise()
while not done:
    # Handle events like window closing and key presses.
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
    # Call the display function to render the scene.
    display()
    # Update the display.
    pygame.display.flip()
# Quit pygame when exiting the main_FromProf loop.
pygame.quit()
