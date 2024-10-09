import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import os
import sys

def draw_box(position, size, color):
    glPushMatrix()
    glTranslatef(position[0], position[1], position[2])
    
    # Define the vertices of the box
    half_size = size / 2.0
    vertices = [
        [half_size, half_size, -half_size],
        [half_size, -half_size, -half_size],
        [half_size, half_size, half_size],
        [half_size, -half_size, half_size],
        [-half_size, half_size, -half_size],
        [-half_size, -half_size, -half_size],
        [-half_size, half_size, half_size],
        [-half_size, -half_size, half_size],
    ]

    # Store the vertices for later use
    box_vertices = vertices

    # Draw the box using quads
    glBegin(GL_QUADS)
    
    # Define faces with color
    glColor3f(color[0], color[1], color[2])
    
    # Front face
    glVertex3f(*vertices[0])
    glVertex3f(*vertices[1])
    glVertex3f(*vertices[3])
    glVertex3f(*vertices[2])
    
    # Back face
    glVertex3f(*vertices[4])
    glVertex3f(*vertices[6])
    glVertex3f(*vertices[5])
    glVertex3f(*vertices[7])
    
    # Left face
    glVertex3f(*vertices[4])
    glVertex3f(*vertices[5])
    glVertex3f(*vertices[1])
    glVertex3f(*vertices[0])
    
    # Right face
    glVertex3f(*vertices[2])
    glVertex3f(*vertices[3])
    glVertex3f(*vertices[7])
    glVertex3f(*vertices[6])
    
    # Top face
    glVertex3f(*vertices[4])
    glVertex3f(*vertices[0])
    glVertex3f(*vertices[2])
    glVertex3f(*vertices[6])
    
    # Bottom face
    glVertex3f(*vertices[1])
    glVertex3f(*vertices[5])
    glVertex3f(*vertices[7])
    glVertex3f(*vertices[3])
    
    glEnd()
    
    glPopMatrix()

    # Return the vertices for the box
    return box_vertices
