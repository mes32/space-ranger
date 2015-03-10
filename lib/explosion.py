"""Module corresponding to exploding astroid animations

"""

import pygame

EXPLOSION_IMAGE = pygame.image.load('./resources/images/astroidExplosion.png')

class Explosion:
    """Represents an exploding astroid"""

    def __init__(self, astroid):
        self.rect = astroid.getRect()
        self.speed = astroid.getSpeed()
        self.size = astroid.getSize()
        self.surface = pygame.transform.scale(EXPLOSION_IMAGE, (self.size, self.size))
        self.stage = 1
                       
    def move(self):
        """Move explosion and evolve animation"""
        self.rect.move_ip(0, self.speed)

        # Animate explosion expanding for a few frames/stages
        self.stage += 1
        oldSize = self.size
        self.size = int(oldSize*1.25)
        self.surface = pygame.transform.scale(EXPLOSION_IMAGE, (self.size, self.size))
        self.rect.move_ip(int((oldSize - self.size)/2), int((oldSize - self.size)/2))

    def draw(self, windowSurface):
        """Draws the explosion on the screen"""
        windowSurface.blit(self.surface, self.rect)

    def isOffScreen(self):
        """Returns True if the explosion is past frame 4 of its animation"""
        if self.stage > 4:
            return True
        else:
            return False
