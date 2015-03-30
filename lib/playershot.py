"""Module corresponding to the player's weapon fire (i.e. shots)

"""

import pygame

PLASMA_PROJECTILE_IMAGE = pygame.image.load('./resources/images/plasmaShot.png')
PLASMA_CYCLE_RATE = 4         # Rate of fire (one shot per 4 frames)
PLASMA_PROJECTILE_SPEED = 7   # Speed of shot movement (7 pixels per frame)
PLASMA_PROJECTILE_DAMAGE = 2  # Damage to astroids

RAILGUN_PROJECTILE_IMAGE = pygame.image.load('./resources/images/railgunShot.png')
RAILGUN_CYCLE_RATE = 12         # Rate of fire (one shot per 12 frames)
RAILGUN_PROJECTILE_SPEED = 10   # Speed of shot movement (10 pixels per frame)
RAILGUN_PROJECTILE_DAMAGE = 10  # Damage to astroids

class Weapon:
    """Represents the source of the player's fire.

    Holds a counter that manages the spawning of new Projectile based on rate. 
    """

    def __init__(self, player):
        self.player = player
        self.rateOfFire = 0
        self.counter = 0

    def reset(self):
        """Resets the weapon firing counter (needed when changing weapons)"""
        self.counter = 0

    def fire(self, playerHitbox):
        """Creates a new projectile relative to the player's hitbox"""
        return []

    def cycle(self):
        """Cycles the weapon firing (creating new projectiles) as needed"""

        if self.counter % self.rateOfFire == 0:
            self.counter = 1
            return self.fire(self.player.getHitbox())
        else:
            self.counter += 1
            return []


class PlasmaCannons(Weapon):
    """Represents the source of the player's fire (cannons).

    Holds a counter that manages the spawning of new PlasmaProjectile based on 
    PLASMA_CYCLE_RATE. 
    """

    def __init__(self, player):
        self.player = player
        self.rateOfFire = PLASMA_CYCLE_RATE
        self.counter = 0

    def fire(self, playerHitbox):
        """Creates a new PlasmaProjectile relative to the player's hitbox"""
        return [PlasmaProjectile.newLeft(playerHitbox), PlasmaProjectile.newRight(playerHitbox)]

class Railgun(Weapon):
    """Represents the source of the player's fire (a railgun).

    Holds a counter that manages the spawning of new RailgunProjectile based on 
    RAILGUN_CYCLE_RATE. 
    """

    def __init__(self, player):
        self.player = player
        self.rateOfFire = RAILGUN_CYCLE_RATE
        self.counter = 0

    def fire(self, playerHitbox):
        """Creates a new RailgunProjectile relative to the player's hitbox"""
        return [RailgunProjectile(playerHitbox)]

class Projectile:
    """Represents projectiles fired by the player"""

    def __init__(self, playerHitbox):
        self.rect = pygame.Rect(playerHitbox.centerx-3, playerHitbox.centery-12, 5, 16)
        self.image = RAILGUN_PROJECTILE_IMAGE
        self.damage = 0
        self.speed = 0

    def getRect(self):
        """Returns the hitbox for this projectile"""
        return self.rect

    def move(self):
        """Moves the projectile location up the screen based on RAILGUN_PROJECTILE_SPEED"""
        self.rect.move_ip(0, -self.speed)

    def isOffScreen(self):
        """Returns True if projectile has moved beyond the top of the screen"""
        if self.rect.bottom < 0:
            return True
        else:
            return False

    def draw(self, windowSurface):
        """Draws the projectile sprite on the screen"""
        windowSurface.blit(self.image, self.rect)

    def getDamage(self):
        """Returns the damage delt by this projectile"""
        return self.damage

class PlasmaProjectile(Projectile):
    """Represents projectiles fired by the PlasmaCannons class"""

    def __init__(self, playerHitbox, left):
        if left:
            self.rect = pygame.Rect(playerHitbox.centerx-16, playerHitbox.centery-3, 5, 16)
        else:
            self.rect = pygame.Rect(playerHitbox.centerx+11, playerHitbox.centery-3, 5, 16)
        self.image = PLASMA_PROJECTILE_IMAGE
        self.damage = PLASMA_PROJECTILE_DAMAGE
        self.speed = PLASMA_PROJECTILE_SPEED

    @staticmethod
    def newLeft(playerHitbox):
        """Creates a new projectile to the left of the player"""
        return PlasmaProjectile(playerHitbox, True)

    @staticmethod
    def newRight(playerHitbox):
        """Creates a new projectile to the right of the player"""
        return PlasmaProjectile(playerHitbox, False)

class RailgunProjectile(Projectile):
    """Represents the projectiles fired by the Railgun class"""

    def __init__(self, playerHitbox):
        self.rect = pygame.Rect(playerHitbox.centerx-3, playerHitbox.centery-12, 5, 16)
        self.image = RAILGUN_PROJECTILE_IMAGE
        self.damage = RAILGUN_PROJECTILE_DAMAGE
        self.speed = RAILGUN_PROJECTILE_SPEED

