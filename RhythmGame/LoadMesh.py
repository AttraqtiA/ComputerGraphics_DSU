from OpenGL.GL import *
from OpenGL.GLUT import *
import pygame

class LoadMesh:
    def __init__(self, filename, draw_type=GL_TRIANGLES):
        self.vertices = []
        self.faces = []
        self.texture_coords = []
        self.faces_with_uv = []
        self.draw_type = draw_type
        self.scale_factor = 1  # Scaling factor for the mesh
        self.load_mesh(filename)

    def load_mesh(self, filename):
        with open(filename, 'r') as f:
            for line in f:
                if line.startswith('v '):
                    vertex = [float(x) for x in line.split()[1:]]
                    self.vertices.append([v * self.scale_factor for v in vertex])
                elif line.startswith('vt '):  # Texture coordinates
                    uv = [float(x) for x in line.split()[1:]]
                    self.texture_coords.append(uv)
                elif line.startswith('f '):
                    face = []
                    uv_face = []
                    for item in line.split()[1:]:
                        vertex_data = item.split('/')
                        face.append(int(vertex_data[0]) - 1)  # Vertex index
                        if len(vertex_data) > 1 and vertex_data[1]:  # UV index
                            uv_face.append(int(vertex_data[1]) - 1)
                    self.faces.append(face)
                    if uv_face:
                        self.faces_with_uv.append(uv_face)

    def draw(self, texture_id=None, position=(0, 0, 0), scale=1.0):
        glPushMatrix()
        glTranslatef(*position)
        glScalef(scale, scale, scale)

        if texture_id:
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, texture_id)
        else:
            glDisable(GL_TEXTURE_2D)

        glBegin(self.draw_type)  # GL_TRIANGLES will render filled faces
        for i, face in enumerate(self.faces):
            for j, vertex_index in enumerate(face):
                if texture_id and self.faces_with_uv:
                    uv_index = self.faces_with_uv[i][j]
                    if uv_index < len(self.texture_coords):
                        glTexCoord2f(*self.texture_coords[uv_index])
                glVertex3fv(self.vertices[vertex_index])  # Draw vertex
        glEnd()

        glPopMatrix()
        glDisable(GL_TEXTURE_2D)


# Utility to load texture
def load_texture(image_file):
    texture_surface = pygame.image.load(image_file)
    texture_data = pygame.image.tostring(texture_surface, "RGB", True)
    width, height = texture_surface.get_rect().size

    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, texture_data)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    return texture_id
