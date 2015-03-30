"""Module corresponding to the player's ship exhaust

"""

import random
import pygame

IMAGE_LONG_100_A = pygame.image.load('./resources/images/exhaustLong_100.png')
IMAGE_LONG_100_B = pygame.transform.flip(IMAGE_LONG_100_A, True, False)
IMAGE_LONG_85_A  = pygame.image.load('./resources/images/exhaustLong_85.png')
IMAGE_LONG_85_B  = pygame.transform.flip(IMAGE_LONG_85_A, True, False)
IMAGE_LONG_65_A  = pygame.image.load('./resources/images/exhaustLong_65.png')
IMAGE_LONG_65_B  = pygame.transform.flip(IMAGE_LONG_65_A, True, False)

IMAGE_MEDIUM_100_A = pygame.transform.scale(IMAGE_LONG_100_A, (8, 18))
IMAGE_MEDIUM_100_B = pygame.transform.scale(IMAGE_LONG_100_B, (8, 18))
IMAGE_MEDIUM_85_A  = pygame.transform.scale(IMAGE_LONG_85_A,  (8, 18))
IMAGE_MEDIUM_85_B  = pygame.transform.scale(IMAGE_LONG_85_B,  (8, 18))
IMAGE_MEDIUM_65_A  = pygame.transform.scale(IMAGE_LONG_65_A,  (8, 18))
IMAGE_MEDIUM_65_B  = pygame.transform.scale(IMAGE_LONG_65_B,  (8, 18))

IMAGE_SHORT_100_A = pygame.transform.scale(IMAGE_LONG_100_A, (9, 10))
IMAGE_SHORT_100_B = pygame.transform.scale(IMAGE_LONG_100_B, (9, 10))
IMAGE_SHORT_85_A  = pygame.transform.scale(IMAGE_LONG_85_A,  (9, 10))
IMAGE_SHORT_85_B  = pygame.transform.scale(IMAGE_LONG_85_B,  (9, 10))
IMAGE_SHORT_65_A  = pygame.transform.scale(IMAGE_LONG_65_A,  (9, 10))
IMAGE_SHORT_65_B  = pygame.transform.scale(IMAGE_LONG_65_B,  (9, 10))

LONG_IMAGES_LIST = [
    IMAGE_LONG_100_A,
    IMAGE_LONG_100_B,
    IMAGE_LONG_85_A,
    IMAGE_LONG_85_B,
    IMAGE_LONG_65_A,
    IMAGE_LONG_65_B
]

MEDIUM_IMAGES_LIST = [
    IMAGE_MEDIUM_100_A,
    IMAGE_MEDIUM_100_B,
    IMAGE_MEDIUM_85_A,
    IMAGE_MEDIUM_85_B,
    IMAGE_MEDIUM_65_A,
    IMAGE_MEDIUM_65_B
]

SHORT_IMAGES_LIST = [
    IMAGE_SHORT_100_A,
    IMAGE_SHORT_100_B,
    IMAGE_SHORT_85_A,
    IMAGE_SHORT_85_B,
    IMAGE_SHORT_65_A,
    IMAGE_SHORT_65_B
]

class Exhaust:
    """Represents a stream of the player ship's exhaust"""

    def __init__(self, player):
        self.player = player

    def setImageShort(self):
        """Set exhaust image to a randomly selected short length flame"""
        randInd = random.randint(0, 5)
        self.image = SHORT_IMAGES_LIST[randInd]
        self.hitbox = self.image.get_rect()

    def setImageMedium(self):
        """Set exhaust image to a randomly selected medium length flame"""
        randInd = random.randint(0, 5)
        self.image = MEDIUM_IMAGES_LIST[randInd]
        self.hitbox = self.image.get_rect()

    def setImageLong(self):
        """Set exhaust image to a randomly selected long length flame"""
        randInd = random.randint(0, 5)
        self.image = LONG_IMAGES_LIST[randInd]
        self.hitbox = self.image.get_rect()


    def draw(self, windowSurface):
        """Draw the exhaust relative to player's hitbox"""

        playerHitbox = self.player.getHitbox()
        movingUp = self.player.isMovingUp()
        movingDown = self.player.isMovingDown()

        # Update flame image based on player's vertical motion
        if movingUp:
            self.setImageLong()
        elif movingDown:
            self.setImageShort()
        else:
            self.setImageMedium()

        # Set relative position and draw to screen
        self.hitbox.top = playerHitbox.bottom
        self.hitbox.centerx = playerHitbox.centerx
        windowSurface.blit(self.image, self.hitbox)

