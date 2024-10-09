import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import os
import sys

def draw_box(color, size, position, rotation):
    # Save the current matrix
    glPushMatrix()
    
    # Apply translation to the position
    glTranslatef(position[0], position[1], position[2])
    
    # Apply rotation (assuming rotation is a tuple of (rx, ry, rz))
    glRotatef(rotation[0], 1, 0, 0)  # Rotate around x-axis
    glRotatef(rotation[1], 0, 1, 0)  # Rotate around y-axis
    glRotatef(rotation[2], 0, 0, 1)  # Rotate around z-axis

    glBegin(GL_QUADS)

    # Set the color
    glColor3f(*color)

    # Calculate the half dimensions
    half_size_x = size[0] / 2
    half_size_y = size[1] / 2
    half_size_z = size[2] / 2

    # Define vertices for the cuboid
    vertices = [
        # Front face
        (-half_size_x, -half_size_y, -half_size_z),
        ( half_size_x, -half_size_y, -half_size_z),
        ( half_size_x,  half_size_y, -half_size_z),
        (-half_size_x,  half_size_y, -half_size_z),
        
        # Back face
        (-half_size_x, -half_size_y,  half_size_z),
        ( half_size_x, -half_size_y,  half_size_z),
        ( half_size_x,  half_size_y,  half_size_z),
        (-half_size_x,  half_size_y,  half_size_z),

        # Left face
        (-half_size_x, -half_size_y, -half_size_z),
        (-half_size_x, -half_size_y,  half_size_z),
        (-half_size_x,  half_size_y,  half_size_z),
        (-half_size_x,  half_size_y, -half_size_z),

        # Right face
        ( half_size_x, -half_size_y, -half_size_z),
        ( half_size_x, -half_size_y,  half_size_z),
        ( half_size_x,  half_size_y,  half_size_z),
        ( half_size_x,  half_size_y, -half_size_z),

        # Top face
        (-half_size_x,  half_size_y, -half_size_z),
        ( half_size_x,  half_size_y, -half_size_z),
        ( half_size_x,  half_size_y,  half_size_z),
        (-half_size_x,  half_size_y,  half_size_z),

        # Bottom face
        (-half_size_x, -half_size_y, -half_size_z),
        ( half_size_x, -half_size_y, -half_size_z),
        ( half_size_x, -half_size_y,  half_size_z),
        (-half_size_x, -half_size_y,  half_size_z),
    ]

    # Draw each face
    for i in range(6):
        for j in range(4):
            glVertex3f(vertices[i * 4 + j][0],
                       vertices[i * 4 + j][1],
                       vertices[i * 4 + j][2])

    glEnd()

    # Restore the previous matrix
    glPopMatrix()
