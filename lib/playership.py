"""Module corresponding to player attributes and spaceship avatar

"""

import pygame
import playershot
from pygame.locals import *
from gamewindow import *

PLAYER_SPEED = 5   # Rate at which player avatar moves on screen (pixels/per-game-cycle)

PLAYER_IMAGE_STANDARD = pygame.image.load('./resources/images/playerSpaceship.png')            # Standard image for player's spaceship

PLAYER_IMAGE_SHIELD_BLINK = pygame.image.load('./resources/images/playerSpaceshipHit.png')     # An image of the player's spaceship with shields responding to damage

PLAYER_IMAGE_EXPLOSION = pygame.image.load('./resources/images/playerSpaceshipExplosion.png')  # An image of the player's spaceship exploding

class PlayerShip:
    """Represents the player's avatar (a space ship)"""

    def __init__(self):
        self.image = PLAYER_IMAGE_STANDARD
        self.hitbox = self.image.get_rect()
        self.hitbox.topleft = ((WINDOW_WIDTH / 2) - self.hitbox.centerx, WINDOW_HEIGHT - 50)
        self.selectedWeapon = playershot.PlasmaCannons()

        self.isDestroyed = False
        self.shields = 100
        self.shieldBlink = 0
        self.score = 0

        self.movingLeft = self.movingRight = self.movingUp = self.movingDown = False

    def reset(self):
        """Resets the location and image"""
        self.image = PLAYER_IMAGE_STANDARD
        self.hitbox = self.image.get_rect()
        self.hitbox.topleft = (WINDOW_WIDTH / 2, WINDOW_HEIGHT - 50)
        self.shieldBlink = 0
        self.movingLeft = self.movingRight = self.movingUp = self.movingDown = False

    def move(self):
        if self.movingLeft and self.notLeftEdge():
            self.hitbox.move_ip(-1 * PLAYER_SPEED, 0)
        if self.movingRight and self.notRightEdge():
            self.hitbox.move_ip(PLAYER_SPEED, 0)
        if self.movingUp and self.notTopEdge():
            self.hitbox.move_ip(0, -1 * PLAYER_SPEED)
        if self.movingDown and self.notBottomEdge():
            self.hitbox.move_ip(0, PLAYER_SPEED)

    def keydownMove(self, event_key):
        if event_key == K_LEFT or event_key == ord('a'):
            self.movingRight = False
            self.movingLeft = True
        if event_key == K_RIGHT or event_key == ord('d'):
            self.movingLeft = False
            self.movingRight = True
        if event_key == K_UP or event_key == ord('w'):
            self.movingDown = False
            self.movingUp = True
        if event_key == K_DOWN or event_key == ord('s'):
            self.movingUp = False
            self.movingDown = True
        if event_key == ord('2'):
            self.selectedWeapon = playershot.Railgun()
        if event_key == ord('1'):
            self.selectedWeapon = playershot.PlasmaCannons()

    def keyupMove(self, event_key):
        if event_key == K_LEFT or event_key == ord('a'):
            self.movingLeft = False
        if event_key == K_RIGHT or event_key == ord('d'):
            self.movingRight = False
        if event_key == K_UP or event_key == ord('w'):
            self.movingUp = False
        if event_key == K_DOWN or event_key == ord('s'):
            self.movingDown = False

    def mouseMove(self, event):
        """Move the avatar on the screen based on mouse movement events"""
        self.hitbox.move_ip(event.pos[0] - self.hitbox.centerx, event.pos[1] - self.hitbox.centery)

        # Keep avatar inside the bounds of the screen
        if self.hitbox.top < 0:
            height = self.hitbox.height
            self.hitbox.top = 0
            self.hitbox.bottom = height
        elif self.hitbox.bottom > WINDOW_HEIGHT:
            height = self.hitbox.height
            self.hitbox.bottom = WINDOW_HEIGHT
            self.hitbox.top = WINDOW_HEIGHT - height
        if self.hitbox.left < 0:
            width = self.hitbox.width
            self.hitbox.left = 0
            self.hitbox.right = width
        elif self.hitbox.right > WINDOW_WIDTH:
            width = self.hitbox.width
            self.hitbox.right = WINDOW_WIDTH
            self.hitbox.left = WINDOW_WIDTH - width

    def notLeftEdge(self):
        """Return True if the avatar is not past the leftward edge of the screen"""
        if self.hitbox.left > 0:
            return True
        else:
            return False

    def notRightEdge(self):
        """Return True if the avatar is not past the rightward edge of the screen"""
        if self.hitbox.right < WINDOW_WIDTH:
            return True
        else:
            return False

    def notTopEdge(self):
        """Return True if the avatar is not past the top edge of the screen"""
        if self.hitbox.top > 0:
            return True
        else:
            return False

    def notBottomEdge(self):
        """Return True if the avatar is not past the bottom edge of the screen"""
        if self.hitbox.bottom < WINDOW_HEIGHT:
            return True
        else:
            return False

    def mouseCursorFollow(self):
        """Repositions the mouse cursor to follow the player avatar"""
        pygame.mouse.set_pos(self.hitbox.centerx, self.hitbox.centery)

    def draw(self, windowSurface):
        """Draws the player avatar on the screen with an up-to-date image"""
        self.updateImage()
        windowSurface.blit(self.image, self.hitbox)

    def updateImage(self):
        """Updates the image used for the player avatar.

        Show shields blinking when hit and the ship exploding when destroyed.
        """
        if self.isDestroyed == True:
            self.image = PLAYER_IMAGE_EXPLOSION
        elif self.shieldBlink > 0:
            self.shieldBlink -= 1
            self.image = PLAYER_IMAGE_SHIELD_BLINK
        else:
            self.image = PLAYER_IMAGE_STANDARD

    def cycleWeapon(self):
        return self.selectedWeapon.cycle(self.getHitbox())

    def getHitbox(self):
        """Returns the hitbox attribute for the player avatar"""
        return self.hitbox

    def getScore(self):
        """Returns the player's current score"""
        return self.score

    def addScore(self, s):
        """Increases the player's current score by a given amount"""
        self.score += s

    def getShields(self):
        """Returns the current value for spaceship's shields"""
        return self.shields

    def subShields(self, minus):
        """Increases the spaceship's shields by a given amount"""
        self.shields -= minus

        # If damage would make shields negative the ship is destroyed
        if self.shields < 0:
            self.isDestroyed = True
            self.shields = 0

        # Shields visibly "blink" in response to damage for 8 cylces
        else:
            self.shieldBlink = 8

    def addShields(self, plus):
        """Increases the spaceship's shields by a given amount"""
        self.shields += plus

        # Shields cannot excede 100% but give bonus to score
        if self.shields > 100:
            self.shields = 100
            self.score += 10

    def isDestroyed(self):
        """Indicates whether the player's spaceship has been destroyed"""
        return isDestroyed

