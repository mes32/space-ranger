"""Module corresponding to the player's weapon fire (i.e. shots)

"""

import pygame

SHOT_IMAGE = pygame.image.load('./resources/images/shot.png')

SHOT_ADD_RATE = 6    # Rate of fire (one shot per 6 frames)
SHOT_SPEED = 10      # Speed of shot movement (10 pixels per frame)
DAMAGE_PER_SHOT = 5  # Damage delt to astroids (originally 3)

class Railgun:
    """Represents the source of the player's fire (a railgun).

    Holds a counter that manages the spawning of new RailgunProjectile based on 
    SHOT_ADD_RATE. 
    """
    counter = 0
    def cycle(self, playerHitbox):
        Railgun.counter += 1
        if Railgun.counter == SHOT_ADD_RATE:
            Railgun.counter = 0
            return [RailgunProjectile(playerHitbox)]
        else:
            return []

class RailgunProjectile:
    """Represents the projectiles fired by the Railgun class"""

    def __init__(self, playerHitbox):
        self.rect = pygame.Rect(playerHitbox.centerx-3, playerHitbox.centery-12, 5, 16)

    def getRect(self):
        """Returns the hitbox for this projectile"""
        return self.rect

    def move(self):
        """Moves the projectile location up the screen based on SHOT_SPEED"""
        self.rect.move_ip(0, -SHOT_SPEED)

    def isOffScreen(self):
        """Returns True if projectile has moved beyond the top of the screen"""
        if self.rect.bottom < 0:
            return True
        else:
            return False

    def draw(self, windowSurface):
        """Draws the projectile sprite on the screen"""
        windowSurface.blit(SHOT_IMAGE, self.rect)

    def getDamage(self):
        """Returns the damage delt by this projectile"""
        return DAMAGE_PER_SHOT

