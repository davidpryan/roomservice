import pygame
import os
import random
import time
import math
from pygame.locals import K_SPACE


# Constants
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 1000

IMAGE_SIZE = 100

BUILDING_X = 100
BUILDING_Y = 300

CHARACTER_SIZE = 100

CHARACTER_DIRECTORY = "./characters"
BUILDING_DIRECTORY = "./buildings"
BACKGROUND_DIRECTORY = "./background"

MOVEMENT_SPEED = 16  # Pixels per millisecond
UPDATE_INTERVAL_MS = 30  # Milliseconds (changed from 50)
COLLISION_COOLDOWN_MS = 1000  # Milliseconds (1 second)

NEW_FILES_CHECK_INTERVAL = 5  # Seconds

BUILDING_LOCATIONS = []

def get_building_locations():
    # Could do this programatically, but why not just set it vOv
    return [[100,100],[200,100],[300,100],[600,100],[700,100],[800,100]
            , [100,400],[200,400],[300,400],[600,400],[700,400],[800,400]
            ]
    
BUILDING_LOCATIONS = get_building_locations()
# Initialize Pygame
pygame.init()

# Create the Pygame window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# Set the title of the window
pygame.display.set_caption("Character Viewer")

# Function to get a list of filenames in the directory
def get_filenames(directory):
    filenames = []
    for filename in os.listdir(directory):
        if filename.endswith((".png", ".jpg", ".jpeg", ".gif")):
            filenames.append(filename)
    return filenames

# Function to load characters and buildings from directories
def load_characters_and_buildings(active_character_filenames, active_building_filenames):
    character_filenames = get_filenames(CHARACTER_DIRECTORY)
    building_filenames = get_filenames(BUILDING_DIRECTORY)
    
    # Remove active filenames from the list of available filenames
    available_character_filenames = [filename for filename in character_filenames if filename not in active_character_filenames]
    available_building_filenames = [filename for filename in building_filenames if filename not in active_building_filenames]
    
    characters = [Character(filename) for filename in available_character_filenames]

    buildings = []
    # Add up to enough buildings to fill in every building location
    i = 0
    print('lens')
    print(len(BUILDING_LOCATIONS))
    print(len(available_building_filenames))
    while i < len(BUILDING_LOCATIONS) and i < len(available_building_filenames):

        buildings.extend([Building(available_building_filenames[i], BUILDING_LOCATIONS[i][0], BUILDING_LOCATIONS[i][1]) ])
        print(BUILDING_LOCATIONS[i][0])
        print(BUILDING_LOCATIONS[i][1])
        i = i + 1
    
    # Update active filenames with the new filenames
    active_character_filenames.extend(available_character_filenames)
    active_building_filenames.extend(available_building_filenames)
    
    return characters, buildings

# Class to encapsulate character behavior
class Character:
    def __init__(self, filename):
        self.image = pygame.transform.scale(pygame.image.load(os.path.join(CHARACTER_DIRECTORY, filename)), (IMAGE_SIZE, IMAGE_SIZE))
        self.position = [random.randint(0, WINDOW_WIDTH - IMAGE_SIZE), random.randint(0, WINDOW_HEIGHT - IMAGE_SIZE)]
        self.direction = [random.choice([1, -1]), random.choice([1, -1])]
        self.collision_cooldown = 0  # Cooldown timer for collision response
        self.filename = filename

    def update(self, elapsed_time, buildings):
        x, y = self.position
        dx, dy = self.direction

        if self.collision_cooldown > 0:
            # Move directly away from the last collided building
            delta_x = dx * MOVEMENT_SPEED * elapsed_time
            delta_y = dy * MOVEMENT_SPEED * elapsed_time
            x += delta_x
            y += delta_y

            self.collision_cooldown -= elapsed_time

            # After cooldown, reset direction
            if self.collision_cooldown <= 0:
                self.direction = [random.choice([1, -1]), random.choice([1, -1])]
        else:
            # Update character position based on speed and elapsed time
            delta_x = dx * MOVEMENT_SPEED * elapsed_time
            delta_y = dy * MOVEMENT_SPEED * elapsed_time

            x += delta_x
            y += delta_y

            # Check for collisions with window edges and bounce
            if x < 0 or x > WINDOW_WIDTH - IMAGE_SIZE:
                dx = -dx
            if y < 0 or y > WINDOW_HEIGHT - IMAGE_SIZE:
                dy = -dy

            # Check for collisions with buildings and change direction
            for building in buildings:
                if self.collide_with(building.rect):
                    dx = -dx
                    dy = -dy
                    self.collision_cooldown = COLLISION_COOLDOWN_MS / 1000  # Set cooldown timer
                    break

            self.position = [x, y]
            self.direction = [dx, dy]

    def draw(self, screen):
        screen.blit(self.image, self.position)

    def collide_with(self, rect):
        character_rect = pygame.Rect(self.position[0], self.position[1], IMAGE_SIZE, IMAGE_SIZE)
        return character_rect.colliderect(rect)

# Class to encapsulate building behavior
class Building:
    def __init__(self, filename, x, y):
        self.image = pygame.transform.scale(pygame.image.load(os.path.join(BUILDING_DIRECTORY, filename)), (BUILDING_X, BUILDING_Y))
        self.position = [x,y]
        self.rect = pygame.Rect(self.position[0], self.position[1], BUILDING_X, BUILDING_Y)
        self.filename = filename

    def draw(self, screen):
        screen.blit(self.image, self.position)
        print(self.position)

# Class to encapsulate background behavior
class Background:
    def __init__(self, filename):
        self.image = pygame.transform.scale(pygame.image.load(os.path.join(BACKGROUND_DIRECTORY, filename)), (WINDOW_WIDTH, WINDOW_HEIGHT))

    def draw(self, screen):
        screen.blit(self.image, (0, 0))

# Lists to track active character and building filenames
active_character_filenames = []
active_building_filenames = []

# Load initial characters, buildings, and background
characters, buildings = load_characters_and_buildings(active_character_filenames, active_building_filenames)
background = Background(get_filenames(BACKGROUND_DIRECTORY)[0])

# Track the time for checking new files
last_new_files_check_time = time.time()

# Create a clock object to control the frame rate
clock = pygame.time.Clock()

# Main loop
running = True
last_update_time = time.time()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    current_time = time.time()
    elapsed_time = current_time - last_update_time

    # Limit the frame rate to approximately 60 FPS
    clock.tick(60)

    if elapsed_time >= UPDATE_INTERVAL_MS / 1000:  # Convert milliseconds to seconds
        # Update character positions and handle bouncing
        for character in characters:
            character.update(elapsed_time, buildings)

        last_update_time = current_time

    # Check for new characters and buildings at regular intervals
    if current_time - last_new_files_check_time >= NEW_FILES_CHECK_INTERVAL:
        new_characters, new_buildings = load_characters_and_buildings(active_character_filenames, active_building_filenames)

        # Append new characters and buildings to the existing lists
        characters.extend(new_characters)
        buildings.extend(new_buildings)

        # Update active character and building filenames
        active_character_filenames.extend([character.filename for character in new_characters])
        active_building_filenames.extend([building.filename for building in new_buildings])

        last_new_files_check_time = current_time

    # Clear the screen
    screen.fill((255, 255, 255))

    # Draw the background
    background.draw(screen)

    # Draw the buildings
    for building in buildings:
        building.draw(screen)

    # Draw the characters at their updated positions
    for character in characters:
        character.draw(screen)

    pygame.display.flip()

pygame.quit()
