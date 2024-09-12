import pygame

from pygame.locals import * # key pressing, key capture, etc

# INITIAL FILE, BEFORE UPDATED IN HelloOpenGL.py
pygame.init()

screen_width = 1000
screen_height = 800

#Display the screen
screen = pygame.display.set_mode((screen_width, screen_width), DOUBLEBUF | OPENGL)
# DOUBLEBUF is important!

pygame.display.set_caption('OpenGL in Python :3')

# We need to make a main loop, so that it won't immediately close the window

done = False

while not done:
    for event in pygame.event.get(): # actively check for status / event in the last loop
        if event.type == pygame.QUIT:
            done = True
    pygame.display.flip() #  put the content which was drawn in the buffer to the display
    pygame.time.wait(100) # check status every 100 milliseconds
pygame.quit()

