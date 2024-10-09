import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import os
import sys
from main import *


def handle_input():
    global player_pos, yaw, pitch, vertical_speed, is_jumping

    keys = pygame.key.get_pressed()

    # Movement forward and backward
    move_x = math.sin(math.radians(yaw)) * MOVE_SPEED
    move_z = math.cos(math.radians(yaw)) * MOVE_SPEED
    if keys[K_w]:
        player_pos[0] += move_x
        player_pos[2] -= move_z
    if keys[K_s]:
        player_pos[0] -= move_x
        player_pos[2] += move_z

    # Strafe left and right
    strafe_x = math.sin(math.radians(yaw + 90)) * MOVE_SPEED
    strafe_z = math.cos(math.radians(yaw + 90)) * MOVE_SPEED
    if keys[K_a]:
        player_pos[0] -= strafe_x
        player_pos[2] += strafe_z
    if keys[K_d]:
        player_pos[0] += strafe_x
        player_pos[2] -= strafe_z

    # Jumping logic
    if keys[K_SPACE] and player_pos[1] == 0:  # Only jump if on the ground
        vertical_speed = JUMP_FORCE
        is_jumping = True

def handle_mouse():
    global yaw, pitch, mouse_sensitivity

    # Get mouse movement
    mouse_dx, mouse_dy = pygame.mouse.get_rel()

    # Update yaw (turning left/right) and pitch (looking up/down)
    yaw += mouse_dx * mouse_sensitivity
    pitch += mouse_dy * mouse_sensitivity  # Inverted the pitch control

    # Limit pitch (looking up/down) to prevent flipping over
    if pitch > 90:
        pitch = 90
    if pitch < -90:
        pitch = -90