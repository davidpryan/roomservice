import pygame
import os
import random
import time
import math
from pygame.locals import K_SPACE

# Import classes
from Character import Character # characters that walk around
from Building import Building
from Background import Background
from Collider import Collider # no-go zones for walking characters
from Interactable import Interactable # Interactable zones/items for characters

# TODO -- add little reward things?

# Constants
WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1080

IMAGE_SIZE = 100

BUILDING_X = 100
BUILDING_Y = 300

CHARACTER_SIZE = 100

CHARACTER_DIRECTORY = "./characters"
BUILDING_DIRECTORY = "./buildings"
BACKGROUND_DIRECTORY = "./background"
INTERACTABLE_DIRECTORY = "./interactable"

MOVEMENT_SPEED = 16  # Pixels per millisecond
UPDATE_INTERVAL_MS = 10  # Milliseconds (changed from 50)
COLLISION_COOLDOWN_MS = 1000  # Milliseconds (1 second)

NEW_FILES_CHECK_INTERVAL = 5  # Seconds

BUILDING_LOCATIONS = []

COLLIDERS = {}

CIRCLE_COLOR = (200,0,0)
CIRCLE_RADIUS = 10

# TODO -- add ability to add 'enrichment' --> paid???? cooldown between times you can add them?

# Add some basic activities
# Walk -- place to place
# Sit -- hangout
# Appear

# Initialize Pygame
pygame.init()

# Create the Pygame window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# Set the title of the window
pygame.display.set_caption("Character Viewer")

# Lists to track active character filenames
active_character_filenames = []

# Function to get a list of filenames in the directory
def get_filenames(directory):
    filenames = []
    for filename in os.listdir(directory):
        if filename.endswith((".png", ".jpg", ".jpeg", ".gif")):
            filenames.append(filename)
    return filenames

# Function to load characters directories
def load_characters(active_character_filenames):
    character_filenames = get_filenames(CHARACTER_DIRECTORY)
    # Remove active filenames from the list of available filenames
    available_character_filenames = [filename for filename in character_filenames if filename not in active_character_filenames]
    characters = [Character(filename) for filename in available_character_filenames]
    # Update active filenames with the new filenames
    active_character_filenames.extend(available_character_filenames)    
    return characters

# Load initial characters, colliders, backgrounds
characters = load_characters(active_character_filenames)
colliders = []#instantiate_colliders()
background = Background(get_filenames(BACKGROUND_DIRECTORY)[0])

# Track the time for checking new files
last_new_files_check_time = time.time()

# Create a clock object to control the frame rate
clock = pygame.time.Clock()

# Main loop
running = True
state = 'setup' # Start in the 'setup' phase

debug = True

# Initialize
n_clicks = 0
begun = False
circles = []
last_update_time = 0
pos1 = 0
pos2 = 0

# Handles the setup, takes in the various vars and then outputs them
def handle_setup(pos1, pos2, n_clicks, begun, circles, colliders, screen, last_update_time, state):
    print('setup')
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # handle MOUSEBUTTONUP
        if event.type == pygame.MOUSEBUTTONUP: # For getting mouse positions to set colliders
            if begun == True:
                if n_clicks == 0:
                    print('0')
                    # Place initial circle, store first x/y
                    pos1 = pygame.mouse.get_pos()
                    pygame.draw.circle(screen,CIRCLE_COLOR,(pos1[0],pos1[1]),CIRCLE_RADIUS) # DRAW CIRCLE
                    pygame.display.flip()
                    print("first position: " + str(pos1))
                    n_clicks = n_clicks + 1
                elif n_clicks == 1:
                    print('1')                    
                    pos2 = pygame.mouse.get_pos()
                    pygame.draw.circle(screen,CIRCLE_COLOR,(pos2[0],pos2[1]),CIRCLE_RADIUS) # DRAW CIRCLE
                    pygame.display.flip()
                    print("second position: " + str(pos2))
                    n_clicks = n_clicks + 1
                else:# n_clicks == 2:
                    # Create the rect, create a rect
                    new_collider = Collider(pos1[0], pos1[1], pos2[0], pos2[1])
                    colliders.append(new_collider)
                    print('Num colliders:')
                    print(len(colliders))
                    # Clear the screen
                    screen.fill((255, 255, 255))
                    # Draw the background
                    background.draw(screen)
                    n_clicks = 0

        if event.type == pygame.KEYDOWN:
            # Start the setup
            if event.key == pygame.K_SPACE:
                print('start setup')
                begun = True
                n_clicks = 0
                # Clear the screen
                screen.fill((255, 255, 255))
                # Draw the background
                background.draw(screen)
            # Start the simulation
            if event.key == pygame.K_RETURN:
                print('start simulation')
                n_clicks = 0
                last_update_time = time.time()
                # Clear the screen
                screen.fill((255, 255, 255))
                # Draw the background
                background.draw(screen)
                # Change the mode
                state = 'running'
    return pos1, pos2, n_clicks, begun, circles, colliders, screen, last_update_time, state

while running:
    # State == 'setup
    # --------------------------------------------
    if state == 'setup':
        pos1, pos2, n_clicks, begun, circles, colliders, screen, last_update_time, state = handle_setup(pos1, pos2, n_clicks, begun, circles, colliders, screen, last_update_time, state)
    # State == running
    # --------------------------------------------
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # handle MOUSEBUTTONUP
            if event.type == pygame.MOUSEBUTTONUP: # For getting mouse positions to set colliders
                pos = pygame.mouse.get_pos()
                print(pos)
            if event.type == pygame.KEYDOWN:
                # Start the setup
                if event.key == pygame.K_SPACE:
                    print('start setup')
                    begun = True
                    n_clicks = 0
                    colliders = []
                    characters = []
                    # Clear the screen
                    screen.fill((255, 255, 255))
                    # Draw the background
                    background.draw(screen)
                    state = 'setup'

        
        current_time = time.time()
        elapsed_time = current_time - last_update_time

        # Limit the frame rate to approximately 60 FPS
        clock.tick(60)

        if elapsed_time >= UPDATE_INTERVAL_MS / 1000:  # Convert milliseconds to seconds
            # Update character positions and handle bouncing
            for character in characters:
                # Should also handle interactables here...
                character.update(elapsed_time, colliders)

            last_update_time = current_time

        # Check for new characters and buildings at regular intervals
        if current_time - last_new_files_check_time >= NEW_FILES_CHECK_INTERVAL:
            new_characters = load_characters(active_character_filenames)

            # Append new characters to the existing lists
            characters.extend(new_characters)

            # Update active character filenames
            active_character_filenames.extend([character.filename for character in new_characters])

            last_new_files_check_time = current_time
        
# Drawing
# ----------------------------------------------------
    if state == 'setup':
        for c in colliders:
            c.draw(screen)
    # draw characters
    if state != 'setup':
        # # Clear the screen
        screen.fill((255, 255, 255))
        # # Draw the background
        background.draw(screen)
        for character in characters:
            character.draw(screen)
        if debug == True:
            for c in colliders:
                c.draw(screen)

    pygame.display.flip()

pygame.quit()
