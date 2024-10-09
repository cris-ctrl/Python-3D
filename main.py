import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import os
import sys
from Functions.boxes import draw_box
from Functions.room import draw_room
from Functions.input import handle_input, handle_mouse
# Define constants for movement, jump, and sensitivity
FOV = 90
MOVE_SPEED = 0.1
TURN_SPEED = 2
GRAVITY = -0.02
JUMP_FORCE = 0.5

# Variable to control mouse sensitivity
mouse_sensitivity = 0.1

# Initialize player's position and orientation
player_pos = [0.0, 0.0, 5.0]  # Starting at (x=0, y=0, z=5)
yaw = 0.0   # Horizontal rotation
pitch = 0.0  # Vertical rotation (look up/down)
is_jumping = False  # Track if player is jumping
vertical_speed = 0  # Speed of vertical movement (used for jumping)
fullscreen = False  # Track if the game is in fullscreen mode





def apply_gravity():
    global player_pos, vertical_speed, is_jumping

    if is_jumping:
        player_pos[1] += vertical_speed
        vertical_speed += GRAVITY  # Apply gravity

        # Stop jumping if player lands on the ground
        if player_pos[1] <= 0:
            player_pos[1] = 0
            is_jumping = False
            vertical_speed = 0

fullscreen = False  # Track fullscreen state

def toggle_fullscreen():
    global fullscreen
    fullscreen = not fullscreen  # Toggle fullscreen state
    
    if fullscreen:
        pygame.display.set_mode((0, 0), DOUBLEBUF | OPENGL | FULLSCREEN)
    else:
        pygame.display.set_mode((1200, 1200), DOUBLEBUF | OPENGL)
    
    # Update the viewport and aspect ratio
    update_viewport()

def update_viewport():
    width, height = pygame.display.get_surface().get_size()
    
    # Set the new viewport size
    glViewport(0, 0, width, height)
    
    # Adjust the projection to match the new aspect ratio
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    aspect_ratio = width / height
    gluPerspective(FOV, aspect_ratio, 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)




def main():
    pygame.init()
    display = (1200, 1200)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    glMatrixMode(GL_PROJECTION)
    gluPerspective(FOV, (display[0] / display[1]), 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)

    glEnable(GL_DEPTH_TEST)

    clock = pygame.time.Clock()

    # Hide mouse and lock it to the center of the window
    pygame.mouse.set_visible(False)    # Hide mouse
    pygame.event.set_grab(True)        # Lock mouse inside window

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_F11:
                    toggle_fullscreen()

        # Handle mouse input
        handle_mouse()

        # Handle keyboard input
        handle_input()

        # Apply gravity and handle jumping
        apply_gravity()

        # Update the camera view based on player's position and orientation
        glLoadIdentity()
        glRotatef(pitch, 1, 0, 0)  # Pitch rotation (up/down)
        glRotatef(yaw, 0, 1, 0)    # Yaw rotation (left/right)
        glTranslatef(-player_pos[0], -player_pos[1], -player_pos[2])

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        #draw_obj_model('models/cube/cube.obj', color=(0.5, 0.8, 0.2), scale=(1, 1, 1), rotation=(0, 45, 0), position=(0, 0, -5))
        #draw_obj_model('untitled1.obj', color=(0.5, 0.8, 1), scale=(1, 1, 1), rotation=(0, 45, 0), position=(3, 0, 5))


        #draw_room()
        draw_box((1,0,0), (10,5,1), (0,0,12), (0,0,0))
        draw_box((0,1,0), (10,5,1), (12,0,0), (0,-45,0))
        draw_box((0,0,1),(30,0.5,30),(0,-2,0),(0,0,0))
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
