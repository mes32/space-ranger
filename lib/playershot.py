import pygame

SHOT_IMAGE = pygame.image.load('./resources/images/shot.png')

SHOT_ADD_RATE = 6
SHOT_SPEED = 10
DAMAGE_PER_SHOT = 5  # originally 3 DAMAGE per shot

class Railgun:
    counter = 0

    def cycle(self, playerHitbox):
        Railgun.counter += 1
        if Railgun.counter == SHOT_ADD_RATE:
            Railgun.counter = 0
            return [RailgunProjectile(playerHitbox)]
        else:
            return []

class RailgunProjectile:

    def __init__(self, playerHitbox):
        self.rect = pygame.Rect(playerHitbox.centerx-3, playerHitbox.centery-12, 5, 16)

    def getRect(self):
        return self.rect

    def move(self):
        self.rect.move_ip(0, -SHOT_SPEED)

    def isOffScreen(self):
        if self.rect.bottom < 0:
            return True
        else:
            return False

    def draw(self, windowSurface):
        windowSurface.blit(SHOT_IMAGE, self.rect)

    def getDamage(self):
        return DAMAGE_PER_SHOT

