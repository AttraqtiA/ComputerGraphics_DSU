from OpenGL.GL import *
from OpenGL.GLU import *

class Note:
    def __init__(self, lane, y_pos, speed=0.05):
        self.lane = lane  # 1: top, 2: bottom
        self.x = 2.5  # Start further right
        self.y = y_pos
        self.z = 0
        self.radius = 0.2
        self.speed = speed  # Movement speed
        self.hit = False
        self.missed_time = None
        self.quadric = gluNewQuadric()  # Create quadric object for spheres

    def update_position(self):
        self.x -= self.speed

    def draw(self):
        glPushMatrix()
        glTranslatef(self.x, self.y, self.z)
        glColor3f(1, 0, 0)  # Red color for notes
        gluSphere(self.quadric, self.radius, 20, 20)
        glPopMatrix()
