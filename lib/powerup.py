import random
import pygame
import gamewindow
from gamewindow import *

POWERUP_SPEED_MIN = 1
POWERUP_SPEED_MAX = 4
POWERUP_ADD_RATE = 300

SHIELD_IMAGE = pygame.image.load('./resources/images/powerupShield.png')
CORE_IMAGE = pygame.image.load('./resources/images/powerupAstroidCore.png')

class PowerupSource:
    counter = 0
    def cycle(self, shields):
        PowerupSource.counter += 1
        if PowerupSource.counter == POWERUP_ADD_RATE:
            PowerupSource.counter = 0
            powerUpType = random.randint(0,4)
            if powerUpType == 1 or (shields < 30 and (powerUpType == 2 or powerUpType == 3)):
                return [Powerup('shield')]
            else:
                return [Powerup('plus')]
        else:
            return []

class Powerup:

    def __init__(self, ptype):
        self.ptype = ptype

        if ptype == 'shield':
            self.surface = SHIELD_IMAGE
        else:
            self.surface = CORE_IMAGE
        powerupSize = self.surface.get_width()
        self.rect = pygame.Rect(random.randint(0, WINDOW_WIDTH-powerupSize), 0 - powerupSize, powerupSize, powerupSize)
        self.speed = random.randint(POWERUP_SPEED_MIN, POWERUP_SPEED_MAX)

    def getRect(self):
        return self.rect

    def getSize(self):
        return self.size

    def getSpeed(self):
        return self.speed

    def getMass(self):
        return self.mass

    def move(self):
        self.rect.move_ip(0, self.speed)

    def isOffScreen(self):
        if self.rect.top > gamewindow.WINDOW_HEIGHT:
            return True
        else:
            return False

    def draw(self, windowSurface):
        windowSurface.blit(self.surface, self.rect)

    def getType(self):
        return self.ptype

