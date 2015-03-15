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

    def __init__(self, minSize, maxSize, minSpeed, maxSpeed, sigmaDegrees, addRate):
        self.minSize = minSize
        self.maxSize = maxSize
        self.minSpeed = minSpeed
        self.maxSpeed = maxSpeed
        self.sigmaDegrees = sigmaDegrees
        self.addRate = addRate

    def cycle(self):
        AstroidField.counter += 1
        if AstroidField.counter == self.addRate:
            AstroidField.counter = 0
            return [Astroid(self.minSize, self.maxSize, self.minSpeed, self.maxSpeed, self.sigmaDegrees)]
        else:
            return []

class Astroid:

    def __init__(self, minSize, maxSize, minSpeed, maxSpeed, sigmaDegrees):

        self.size = random.randint(minSize, maxSize)
        self.surface = pygame.transform.scale(ASTROID_IMAGE, (self.size, self.size))
        self.mass = int(self.size^3)
        self.health = int(self.size^3)

        self.rect = pygame.Rect(random.randint(0, gamewindow.WINDOW_WIDTH-self.size), 0 - self.size, self.size, self.size*.6)
        self.startX = self.rect.x
        self.startY = self.rect.y

        self.speed = random.randint(minSpeed, maxSpeed)
        self.angle = random.gauss(0, sigmaDegrees)
        self.step = 0

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

    def getStartX(self):
        return self.startX

    def getStartY(self):
        return self.startY

    def getStep(self):
        return self.step

    def move(self):
        self.step += 1
        
        x = self.rect.x
        y = self.rect.y

        trueX = self.startX + self.speed*self.step*math.sin(math.radians(self.angle))
        trueY = self.startY + self.speed*self.step*math.cos(math.radians(self.angle))

        deltaX = trueX - x
        deltaY = trueY - y

        self.rect.move_ip(deltaX, deltaY)

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


