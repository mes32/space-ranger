
import pygame

EXPLOSION_IMAGE = pygame.image.load('./resources/images/astroidExplosion.png')

class Explosion:

    def __init__(self, astroid):
        self.rect = astroid.getRect()
        self.speed = astroid.getSpeed()
        self.size = astroid.getSize()
        self.surface = pygame.transform.scale(EXPLOSION_IMAGE, (self.size, self.size))
        self.stage = 1
                       
    def move(self):
        self.rect.move_ip(0, self.speed)

        self.stage += 1
        oldSize = self.size
        self.size = int(oldSize*1.25)
        self.surface = pygame.transform.scale(EXPLOSION_IMAGE, (self.size, self.size))
        self.rect.move_ip(int((oldSize - self.size)/2), int((oldSize - self.size)/2))


    def draw(self, windowSurface):
        windowSurface.blit(self.surface, self.rect)

    def isOffScreen(self):
        if self.stage > 4:
            return True
        else:
            return False
