import pygame
from gamewindow import *

PLAYER_SPEED = 5

PLAYER_IMAGE_STANDARD = pygame.image.load('./resources/images/playerSpaceship.png')
PLAYER_IMAGE_SHIELD_BLINK = pygame.image.load('./resources/images/playerSpaceshipHit.png')
PLAYER_IMAGE_EXPLOSION = pygame.image.load('./resources/images/playerSpaceshipExplosion.png')


class PlayerShip:
    def __init__(self):
        self.image = PLAYER_IMAGE_STANDARD
        self.hitbox = self.image.get_rect()
        self.hitbox.topleft = (WINDOW_WIDTH / 2, WINDOW_HEIGHT - 50)
        self.isDestroyed = False
        self.shields = 100
        self.shieldBlink = 0
        self.score = 0

    def reset(self):
        self.image = PLAYER_IMAGE_STANDARD
        self.hitbox = self.image.get_rect()
        self.hitbox.topleft = (WINDOW_WIDTH / 2, WINDOW_HEIGHT - 50)
        self.shieldBlink = 0


    def moveLeft(self):
        self.hitbox.move_ip(-1 * PLAYER_SPEED, 0)

    def moveRight(self):
        self.hitbox.move_ip(PLAYER_SPEED, 0)

    def moveUp(self):
        self.hitbox.move_ip(0, -1 * PLAYER_SPEED)

    def moveDown(self):
        self.hitbox.move_ip(0, PLAYER_SPEED)

    def mouseMove(self, event):
        self.hitbox.move_ip(event.pos[0] - self.hitbox.centerx, event.pos[1] - self.hitbox.centery)


    def notLeftEdge(self):
        if self.hitbox.left > 0:
            return True
        else:
            return False

    def notRightEdge(self):
        if self.hitbox.right < WINDOW_WIDTH:
            return True
        else:
            return False

    def notTopEdge(self):
        if self.hitbox.top > 0:
            return True
        else:
            return False

    def notBottomEdge(self):
        if self.hitbox.bottom < WINDOW_HEIGHT:
            return True
        else:
            return False

    def mouseCursorFollow(self):
        pygame.mouse.set_pos(self.hitbox.centerx, self.hitbox.centery)

    def draw(self, windowSurface):
        self.updateImage()
        windowSurface.blit(self.image, self.hitbox)

    def updateImage(self):
        if self.isDestroyed == True:
            self.image = PLAYER_IMAGE_EXPLOSION
        elif self.shieldBlink > 0:
            self.shieldBlink -= 1
            self.image = PLAYER_IMAGE_SHIELD_BLINK
        else:
            self.image = PLAYER_IMAGE_STANDARD

    def getHitbox(self):
        return self.hitbox

    def getScore(self):
        return self.score

    def addScore(self, s):
        self.score += s

    def getShields(self):
        return self.shields

    def subShields(self, minus):
        self.shields -= minus
        if self.shields <= 0:
            self.shields = 0
            self.isDestroyed = True
        else:
            self.shieldBlink = 8

    def addShields(self, plus):
        self.shields += plus
        if self.shields > 100:
            self.shields = 100
            self.score += 10

    def isDestroyed(self):
        return isDestroyed



