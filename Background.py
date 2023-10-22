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

# Class to encapsulate background behavior
class Background:
    def __init__(self, filename):
        self.image = pygame.transform.scale(pygame.image.load(os.path.join(BACKGROUND_DIRECTORY, filename)), (WINDOW_WIDTH, WINDOW_HEIGHT))

    def draw(self, screen):
        screen.blit(self.image, [0,0])
