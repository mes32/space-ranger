"""Module corresponding to the astroid hazards

"""

import math
import random
import pygame
import gamewindow

ASTROID_IMAGE = pygame.image.load('./resources/images/astroid.png')

class AstroidField:
    """Manages the creation of new astroids.

    Holds a counter that manages the spawning of new Astroids based on 
    addRate, and handles the randomization of Astroid properties.
    """

    def __init__(self, sizeRange, speedRange, sigmaDegrees, addRate):
        self.counter = 0
        self.minSize = sizeRange[0]
        self.maxSize = sizeRange[1]
        self.minSpeed = speedRange[0]
        self.maxSpeed = speedRange[1]
        self.sigmaDegrees = sigmaDegrees
        self.addRate = addRate

    def cycle(self):
        """Create new Astroids as needed"""

        self.counter += 1
        if self.counter == self.addRate:
            # Return a new Astroid

            self.counter = 0

            # Find randomized Astroid properties
            size = random.randint(self.minSize, self.maxSize)
            speed = random.randint(self.minSpeed, self.maxSpeed)
            angle = random.gauss(0, self.sigmaDegrees)
            return [Astroid(size, speed, angle)]
        else:
            # Return nothing
            return []

class Astroid:

    def __init__(self, size, speed, angle):

        self.size = size
        self.image = pygame.transform.scale(ASTROID_IMAGE, (self.size, self.size))
        self.mass = int(self.size^3)
        self.durability = int(self.size^3)

        self.rect = pygame.Rect(random.randint(0, gamewindow.WINDOW_WIDTH-self.size), 0 - self.size, self.size, self.size*.6)
        self.startX = self.rect.x
        self.startY = self.rect.y

        self.speed = speed
        self.angle = angle
        self.step = 0

    def getRect(self):
        """Returns the Astroid's hitbox"""
        return self.rect

    def getSize(self):
        """Returns the Astroid's diameter"""
        return self.size

    def getSpeed(self):
        """Returns the speed the Astroid moves at"""
        return self.speed

    def getMass(self):
        """Returns the mass of the Astroid determines damage to player on collisions"""
        return self.mass

    def getAngle(self):
        """Returns the Astroid's angle (in degrees). Deviation from moving straight down the screen"""
        return self.angle

    def getStartX(self):
        """Returns the Astroid's starting X (horizontal) position"""
        return self.startX

    def getStartY(self):
        """Returns the Astroid's starting Y (vertical) position"""
        return self.startY

    def getStep(self):
        """Returns the Astroid's internal step count as it moves"""
        return self.step

    def move(self):
        """Moves the Astroid around the screen based on starting position, angle, and speed"""

        self.step += 1
        
        x = self.rect.x
        y = self.rect.y

        trueX = self.startX + self.speed*self.step*math.sin(math.radians(self.angle))
        trueY = self.startY + self.speed*self.step*math.cos(math.radians(self.angle))

        deltaX = trueX - x
        deltaY = trueY - y

        self.rect.move_ip(deltaX, deltaY)

    def isOffScreen(self):
        """Returns true if the Astroid has moved past the bottom of the screen"""
        if self.rect.top > gamewindow.WINDOW_HEIGHT:
            return True
        else:
            return False

    def draw(self, windowSurface):
        """Draws the Astroid on the screen at the current location"""
        windowSurface.blit(self.image, self.rect)

    def takeDamage(self, damage):
        """Updates the Astroid's durability based on damage taken"""
        self.durability -= damage

    def isDestroyed(self):
        """Returns true if the Astroid's durability is exhausted"""
        if self.durability <= 0:
            return True
        else:
            return False


