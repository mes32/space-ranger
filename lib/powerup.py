"""Module corresponding to randomly generated powerups the player can pickup

"""

import random
import pygame
import gamewindow

from gamewindow import WINDOW_WIDTH, WINDOW_HEIGHT

POWERUP_SPEED_MIN = 1   # Minimum speed powerups will fall at (1 pixel per frame)
POWERUP_SPEED_MAX = 4   # Maximum speed powerups will fall at
POWERUP_ADD_RATE = 300  # Rate at which new powerups are added (once every 300 frames)

SHIELD_IMAGE = pygame.image.load('./resources/images/powerupShield.png')
CORE_IMAGE = pygame.image.load('./resources/images/powerupAstroidCore.png')

class PowerupSource:
    """Manages the creation of new powerups.

    Holds a counter that manages the spawning of new Powerups based on 
    POWERUP_ADD_RATE, and randomly selects the powerup type.
    """

    counter = 0

    def cycle(self, shields):
        PowerupSource.counter += 1
        if PowerupSource.counter == POWERUP_ADD_RATE:

            PowerupSource.counter = 0
            speed = random.randint(POWERUP_SPEED_MIN, POWERUP_SPEED_MAX)
            powerUpType = random.randint(0,4)
            if powerUpType == 1 or (shields < 30 and (powerUpType == 2 or powerUpType == 3)):

                powerupSize = SHIELD_IMAGE.get_width()
                rect = pygame.Rect(random.randint(0, WINDOW_WIDTH-powerupSize), 0 - powerupSize, powerupSize, powerupSize)
                return [ShieldPowerup(rect, speed)]
            else:

                powerupSize = CORE_IMAGE.get_width()
                rect = pygame.Rect(random.randint(0, WINDOW_WIDTH-powerupSize), 0 - powerupSize, powerupSize, powerupSize)
                return [AstroidCore(rect, speed)]
        else:
            return []

class Powerup:
    """Represents a powerup the player may collect"""

    def getRect(self):
        """Returns the powerup hitbox"""
        return self.rect

    def move(self):
        """Moves the powerup down the screen for one frame"""
        self.rect.move_ip(0, self.speed)

    def isOffScreen(self):
        """Returns True if the powerup has fallen past the bottom of the screen"""
        if self.rect.top > gamewindow.WINDOW_HEIGHT:
            return True
        else:
            return False

    def draw(self, windowSurface):
        """Draws the powerup on the screen"""
        windowSurface.blit(self.image, self.rect)

class ShieldPowerup(Powerup):
    """Represents a shield recharge powerup"""

    def __init__(self, rect, speed):
        self.image = SHIELD_IMAGE
        self.rect = rect
        self.speed = speed

    def effectPlayer(self, player):
        """Deals this powerup effect to the player when picked up (shields +25)"""

        if player.getShields() > 75:
            player.addScore(10)

        player.addShields(25)

class AstroidCore(Powerup):
    """Represents a score increase powerup"""

    def __init__(self, rect, speed):
        self.image = CORE_IMAGE
        self.rect = rect
        self.speed = speed

    def effectPlayer(self, player):
        """Deals this powerup effect to the player when picked up (score +30)"""
        player.addScore(30)


