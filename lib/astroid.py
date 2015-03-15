import math
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

    def __init__(self, minSize, maxSize, minSpeed, maxSpeed, addRate):
        self.minSize = minSize
        self.maxSize = maxSize
        self.minSpeed = minSpeed
        self.maxSpeed = maxSpeed
        self.addRate = addRate

    def cycle(self):
        AstroidField.counter += 1
        if AstroidField.counter == self.addRate:
            AstroidField.counter = 0
            return [Astroid(self.minSize, self.maxSize, self.minSpeed, self.maxSpeed)]
        else:
            return []

class Astroid:

    def __init__(self, minSize, maxSize, minSpeed, maxSpeed):
        self.size = random.randint(minSize, maxSize)
        self.rect = pygame.Rect(random.randint(0, gamewindow.WINDOW_WIDTH-self.size), 0 - self.size, self.size, self.size*.6)
        self.speed = random.randint(minSpeed, maxSpeed)
        self.surface = pygame.transform.scale(ASTROID_IMAGE, (self.size, self.size))
        self.mass = int(self.size^3)
        self.health = int(self.size^3)
        self.angle = 0

    def getRect(self):
        return self.rect

    def getSize(self):
        return self.size

    def getSpeed(self):
        return self.speed

    def getMass(self):
        return self.mass

    def getAngle(self):
        return self.angle

    def move(self):
        self.rect.move_ip(self.speed*math.sin(self.angle), self.speed*math.cos(self.angle))

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


