import random
import pygame
import gamewindow

ASTROID_SIZE_MIN = 15
ASTROID_SIZE_MAX = 45

ASTROID_SPEED_MIN = 1
ASTROID_SPEED_MAX = 7

ASTROID_ADD_RATE = 6

ASTROID_IMAGE = pygame.image.load('./resources/images/astroid.png')

class AstroidField:
    counter = 0

    def cycle(self):
        AstroidField.counter += 1
        if AstroidField.counter == ASTROID_ADD_RATE:
            AstroidField.counter = 0
            return [Astroid()]
        else:
            return []

class Astroid:

    def __init__(self):
        self.size = random.randint(ASTROID_SIZE_MIN, ASTROID_SIZE_MAX)
        self.rect = pygame.Rect(random.randint(0, gamewindow.WINDOW_WIDTH-self.size), 0 - self.size, self.size, self.size*.6)
        self.speed = random.randint(ASTROID_SPEED_MIN, ASTROID_SPEED_MAX)
        self.surface = pygame.transform.scale(ASTROID_IMAGE, (self.size, self.size))
        self.mass = int(self.size^3)
        self.health = int(self.size^3)

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

    def takeDamage(self, damage):
        self.health -= damage

    def isDestroyed(self):
        if self.health <= 0:
            return True
        else:
            return False


