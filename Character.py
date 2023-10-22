import pygame
import os
import random
import time
import math
from pygame.locals import K_SPACE
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

MOVEMENT_SPEED = 16  # Pixels per millisecond
UPDATE_INTERVAL_MS = 30  # Milliseconds (changed from 50)
COLLISION_COOLDOWN_MS = 1000  # Milliseconds (1 second)
 
NEW_FILES_CHECK_INTERVAL = 5  # Seconds

BUILDING_LOCATIONS = []

# TODO -- add spawning

# TODO -- add interact timer (i.e, have them interact with a point)

# TODO -- add emote over heads depending on the context (i.e., interactions, etc.)

# How long the rect animation goes, for spawning them in
# Ray of light comes down, flashes a color, wipes back down to reveal the character sprite
# TODO --> add this spawn animation
SPAWN_TIMER = 2000 # in milliseconds
INTERACT_TIMER = 2000 # in milliseconds 

white = (255, 255, 255)
red = (255, 0, 0)
yellow = (255, 255, 0)


# Check for colliders
# Class to encapsulate character behavior
class Character:
    def __init__(self, filename):
        self.image = pygame.transform.scale(pygame.image.load(os.path.join(CHARACTER_DIRECTORY, filename)), (IMAGE_SIZE, IMAGE_SIZE))
        self.position = [303,400]#[random.randint(0, WINDOW_WIDTH - IMAGE_SIZE), random.randint(0, WINDOW_HEIGHT - IMAGE_SIZE)]
        self.direction = [random.uniform(1, -1), random.uniform(1, -1)]
        self.collision_cooldown = 0  # Cooldown timer for collision response
        self.spawn_cooldown = SPAWN_TIMER
        self.interact_cooldown = INTERACT_TIMER
        self.state = None # Could track collision/interact/spawn here instead!
        self.filename = filename

    def update(self, elapsed_time, colliders):
        x, y = self.position
        dx, dy = self.direction
        print(self.collision_cooldown)
        # If collided recently...
        if self.collision_cooldown > 0:
            # Move directly away from the last collided building
            delta_x = dx * MOVEMENT_SPEED * elapsed_time
            delta_y = dy * MOVEMENT_SPEED * elapsed_time
            x += delta_x
            y += delta_y

            self.collision_cooldown -= elapsed_time

            self.position = [x, y]
            self.direction = [dx, dy]
            # After cooldown, reset direction
            if self.collision_cooldown <= 0:
                self.direction = [random.uniform(1, -1), random.uniform(1, -1)]
        # If haven't collided recently
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
            for collider in colliders:
                if self.collide_with(collider.rect):
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

        #screen.blit(self.image, (0, 0))