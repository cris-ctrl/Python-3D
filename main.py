import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import os
import sys
from Functions.boxes import draw_box
from Functions.room import draw_room

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
    if keys[K_SPACE] and not is_jumping:  # Only jump if not already jumping
        vertical_speed = JUMP_FORCE
        is_jumping = True

def apply_gravity():
    global player_pos, vertical_speed, is_jumping

    # Always apply gravity regardless of jump state
    if is_jumping or player_pos[1] > 0:  # Apply gravity if jumping or falling
        vertical_speed += GRAVITY  # Apply gravity
        player_pos[1] += vertical_speed  # Update player's vertical position

        # Stop falling if player lands on the ground
        if player_pos[1] <= -70:
            player_pos[1] = -70  # Set player position to ground level
            is_jumping = False  # Reset jumping state
            vertical_speed = 0  # Reset vertical speed

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

class OBJModel:
    def __init__(self):
        self.vertices = []
        self.texcoords = []
        self.normals = []
        self.faces = []

    def load_obj(filename):
    vertices = []
    texture_coords = []
    normals = []
    
    with open(filename, 'r') as file:
        for line in file:
            if line.startswith('v '):  # Vertex
                parts = line.strip().split()[1:4]
                vertices.append([float(parts[0]), float(parts[1]), float(parts[2])])
            elif line.startswith('vt '):  # Texture coordinate
                parts = line.strip().split()[1:3]
                texture_coords.append([float(parts[0]), float(parts[1])])
            elif line.startswith('vn '):  # Normal
                parts = line.strip().split()[1:4]
                normals.append([float(parts[0]), float(parts[1]), float(parts[2])])
            elif line.startswith('f '):  # Face
                # Process faces if needed, this part may not change much.
                pass

    # After loading the OBJ, convert vertices into a numpy array if you plan to manipulate them later
    vertices_matrix = np.array(vertices, dtype='float32')

    return vertices_matrix, texture_coords, normals


    def render(self, color=(1, 1, 1), position=(0, 0, 0)):
        glPushMatrix()  # Save the current transformation matrix

        # Apply the position transformation
        glTranslatef(*position)
        # Set the color
        glColor3f(*color)

        for face in self.faces:
            glBegin(GL_QUADS)  # Use GL_QUADS for quadrilaterals
            for vertex_index in face:
                vertex = self.vertices[vertex_index]
                glVertex3f(*vertex)
            glEnd()

        glPopMatrix()  # Restore the previous transformation matrix


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


    # Load the OBJ model
    cube = OBJModel()
    cube.load_obj("Models/Cube/cube.obj")

    running = True
    #Main loop
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

        cube.render(color=(0.5,0.8,0.2), position=(3,0,5))

        #draw_room()
        draw_box((1,0,0), (10,5,1), (0,0,12), (0,0,0))
        draw_box((0,1,0), (10,5,1), (12,0,0), (0,-45,0))
        draw_box((0,0,1),(30,0.5,30),(0,-2,0),(0,0,0))
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
