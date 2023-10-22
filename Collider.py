import pygame
import os
import random
import time
import math
from pygame.locals import K_SPACE

COLLIDER_COLOR = (200,0,0)

# Class to encapsulate colliders

# Takes the top coordinates of the top left and top right, and creates a rect
class Collider:
    def __init__(self, x1, y1, x2, y2):
        self.x_size = x2 - x1
        self.y_size = y2 - y1
        self.position = [x1,y1]
        self.rect = pygame.Rect(self.position[0], self.position[1], self.x_size, self.y_size)

    def draw(self, screen):
        pygame.draw.rect(screen, COLLIDER_COLOR, self.rect)

    

