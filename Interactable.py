import pygame
import os
import random
import time
import math
from pygame.locals import K_SPACE

INTERACTABLE_DIRECTORY = './interactable'
# Takes filename and the top coordinates of the top left and top right, and creates a rect
class Interactable:
    def __init__(self, filename, interact_type, x1, y1, x2, y2):
        self.size = [x2 - x1, y2-y1]
        self.position = [x1,y1]
        self.rect = pygame.Rect(self.position[0], self.position[1], self.size[0], self.size[1])
        self.image = pygame.transform.scale(pygame.image.load(os.path.join(INTERACTABLE_DIRECTORY, filename)), (self.size[0], self.size[1]))
        self.filename = filename
        self.type = interact_type

    def draw(self, screen):
        screen.blit(self.image, self.position)
