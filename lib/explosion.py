"""Module corresponding to exploding astroid animations

"""

import math
import pygame

EXPLOSION_IMAGE = pygame.image.load('./resources/images/astroidExplosion.png')

class Explosion:
    """Represents an exploding astroid"""

    def __init__(self, astroid):

        self.size = astroid.getSize()
        self.originalSize = self.size
        self.surface = pygame.transform.scale(EXPLOSION_IMAGE, (self.size, self.size))

        self.rect = astroid.getRect()
        self.startX = astroid.getStartX()
        self.startY = astroid.getStartY()

        self.speed = astroid.getSpeed()
        self.angle = astroid.getAngle()
        self.step = astroid.getStep()

        self.stage = 1
                       
    def move(self):
        """Move explosion and evolve animation"""

        self.step += 1
        self.stage += 1
        
        x = self.rect.x
        y = self.rect.y

        trueX = self.startX + self.speed*self.step*math.sin(math.radians(self.angle))
        trueY = self.startY + self.speed*self.step*math.cos(math.radians(self.angle))

        self.size = int(self.originalSize*1.2**self.stage)
        self.surface = pygame.transform.scale(EXPLOSION_IMAGE, (self.size, self.size))

        deltaX = trueX - x - (self.size-self.originalSize)/2
        deltaY = trueY - y - (self.size-self.originalSize)/2

        self.rect.move_ip(deltaX, deltaY)

    def draw(self, windowSurface):
        """Draws the explosion on the screen"""
        windowSurface.blit(self.surface, self.rect)

    def isOffScreen(self):
        """Returns True if the explosion is past frame 4 of its animation"""
        if self.stage > 4:
            return True
        else:
            return False
