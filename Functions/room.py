import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import os
import sys

def draw_room():
    glBegin(GL_QUADS)

    # Floor
    glColor3f(0.5, 0.5, 0.5)
    glVertex3f(-5, -1, -5)
    glVertex3f(5, -1, -5)
    glVertex3f(5, -1, 5)
    glVertex3f(-5, -1, 5)

    # Ceiling
    glColor3f(0.7, 0.7, 0.7)
    glVertex3f(-5, 5, -5)
    glVertex3f(5, 5, -5)
    glVertex3f(5, 5, 5)
    glVertex3f(-5, 5, 5)

    # Walls
    glColor3f(0.8, 0.3, 0.3)
    # Front wall
    glVertex3f(-5, -1, -5)
    glVertex3f(5, -1, -5)
    glVertex3f(5, 5, -5)
    glVertex3f(-5, 5, -5)

    # Back wall
    glVertex3f(-5, -1, 5)
    glVertex3f(5, -1, 5)
    glVertex3f(5, 5, 5)
    glVertex3f(-5, 5, 5)

    # Left wall
    glVertex3f(-5, -1, -5)
    glVertex3f(-5, -1, 5)
    glVertex3f(-5, 5, 5)
    glVertex3f(-5, 5, -5)

    # Right wall
    glVertex3f(5, -1, -5)
    glVertex3f(5, -1, 5)
    glVertex3f(5, 5, 5)
    glVertex3f(5, 5, -5)

    glEnd()
