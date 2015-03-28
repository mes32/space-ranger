"""Module corresponding to player attributes and spaceship avatar

"""

import pygame
import playerexhaust
import playershot

from pygame.locals import *
from gamewindow import WINDOW_WIDTH, WINDOW_HEIGHT

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

        self.plasmaCannons = playershot.PlasmaCannons(self)
        self.railgun = playershot.Railgun(self)
        self.selectedWeapon = self.plasmaCannons

        self.destroyed = False
        self.shields = 100
        self.shieldBlink = 0
        self.score = 0

        self.exhaust = playerexhaust.Exhaust(self)
        self.movingLeft = self.movingRight = self.movingUp = self.movingDown = False

    def reset(self):
        """Resets the location and image"""
        self.image = PLAYER_IMAGE_STANDARD
        self.hitbox = self.image.get_rect()
        self.hitbox.topleft = (WINDOW_WIDTH / 2, WINDOW_HEIGHT - 50)
        self.shieldBlink = 0
        self.movingLeft = self.movingRight = self.movingUp = self.movingDown = False

    def move(self):
        """Moves the location of the player based on movement inputs, keeping them in the bounds of the screen"""

        if self.movingLeft and not self.onLeftEdge():
            self.hitbox.move_ip(-1 * PLAYER_SPEED, 0)
        elif self.movingRight and not self.onRightEdge():
            self.hitbox.move_ip(PLAYER_SPEED, 0)

        if self.movingUp and not self.onTopEdge():
            self.hitbox.move_ip(0, -1 * PLAYER_SPEED)
        elif self.movingDown and not self.onBottomEdge():
            self.hitbox.move_ip(0, PLAYER_SPEED)

        self.mouseCursorFollow()

    def keydownMove(self, event_key):
        """Updates player based on key down events"""
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
            self.selectedWeapon = self.railgun
            self.selectedWeapon.reset()
        if event_key == ord('1'):
            self.selectedWeapon = self.plasmaCannons
            self.selectedWeapon.reset()

    def keyupMove(self, event_key):
        """Updates player based on key up events"""
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
        mouseX = event.pos[0]
        mouseY = event.pos[1]
        self.hitbox.move_ip(mouseX - self.hitbox.centerx, mouseY - self.hitbox.centery)

        # Keep avatar inside the bounds of the screen
        if self.onTopEdge():
            height = self.hitbox.height
            self.hitbox.top = 0
            self.hitbox.bottom = height
        elif self.onBottomEdge():
            height = self.hitbox.height
            self.hitbox.bottom = WINDOW_HEIGHT
            self.hitbox.top = WINDOW_HEIGHT - height

        if self.onLeftEdge():
            width = self.hitbox.width
            self.hitbox.left = 0
            self.hitbox.right = width
        elif self.onRightEdge():
            width = self.hitbox.width
            self.hitbox.right = WINDOW_WIDTH
            self.hitbox.left = WINDOW_WIDTH - width

        # Set movement for puposes of exhaust animation
        #if mouseY == self.hitbox.centery:
        #    self.movingUp = False
        #    self.movingDown = False
        #if mouseY > self.hitbox.centery:
        #    self.movingUp = True
        #elif mouseY < self.hitbox.centery:
        #    self.movingDown = True

    def onLeftEdge(self):
        """Return True if the avatar is not past the leftward edge of the screen"""
        if self.hitbox.left <= 0:
            return True
        else:
            return False

    def onRightEdge(self):
        """Return True if the avatar is not past the rightward edge of the screen"""
        if self.hitbox.right >= WINDOW_WIDTH:
            return True
        else:
            return False

    def onTopEdge(self):
        """Return True if the avatar is not past the top edge of the screen"""
        if self.hitbox.top <= 0:
            return True
        else:
            return False

    def onBottomEdge(self):
        """Return True if the avatar is not past the bottom edge of the screen"""
        if self.hitbox.bottom >= WINDOW_HEIGHT:
            return True
        else:
            return False

    def isMovingUp(self):
        return self.movingUp

    def isMovingDown(self):
        return self.movingDown

    def mouseCursorFollow(self):
        """Repositions the mouse cursor to follow the player avatar"""
        pygame.mouse.set_pos(self.hitbox.centerx, self.hitbox.centery)

    def draw(self, windowSurface):
        """Draws the player avatar on the screen with an up-to-date image"""
        self.updateImage()
        if not self.destroyed:
            self.exhaust.draw(windowSurface)
        windowSurface.blit(self.image, self.hitbox)

    def updateImage(self):
        """Updates the image used for the player avatar.

        Show shields blinking when hit and the ship exploding when destroyed.
        """
        if self.destroyed == True:
            self.image = PLAYER_IMAGE_EXPLOSION
        elif self.shieldBlink > 0:
            self.shieldBlink -= 1
            self.image = PLAYER_IMAGE_SHIELD_BLINK
        else:
            self.image = PLAYER_IMAGE_STANDARD

    def cycleWeapon(self):
        return self.selectedWeapon.cycle()

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
            self.destroyed = True
            self.shields = 0

        # Shields visibly "blink" in response to damage for 8 cylces
        else:
            self.shieldBlink = 8

    def addShields(self, plus):
        """Increases the spaceship's shields by a given amount"""
        self.shields += plus

        self.shieldBlink = 3

        # Shields cannot excede 100% but give bonus to score
        if self.shields > 100:
            self.shields = 100

    def isDestroyed(self):
        """Indicates whether the player's spaceship has been destroyed"""
        return self.destroyed

