"""Module corresponding to the player's ship exhaust

"""

import random
import pygame

SHORT_IMAGES_LIST = [
    pygame.image.load('./resources/images/exhaustShortA.png'), 
    pygame.image.load('./resources/images/exhaustShortB.png'), 
    pygame.image.load('./resources/images/exhaustShortC.png'), 
    pygame.image.load('./resources/images/exhaustShortD.png'), 
    pygame.image.load('./resources/images/exhaustShortE.png'), 
    pygame.image.load('./resources/images/exhaustShortF.png')
]

MEDIUM_IMAGES_LIST = [
    pygame.image.load('./resources/images/exhaustMediumA.png'), 
    pygame.image.load('./resources/images/exhaustMediumB.png'), 
    pygame.image.load('./resources/images/exhaustMediumC.png'), 
    pygame.image.load('./resources/images/exhaustMediumD.png'), 
    pygame.image.load('./resources/images/exhaustMediumE.png'), 
    pygame.image.load('./resources/images/exhaustMediumF.png')
]

LONG_IMAGES_LIST = [
    pygame.image.load('./resources/images/exhaustLongA.png'), 
    pygame.image.load('./resources/images/exhaustLongB.png'), 
    pygame.image.load('./resources/images/exhaustLongC.png'), 
    pygame.image.load('./resources/images/exhaustLongD.png'), 
    pygame.image.load('./resources/images/exhaustLongE.png'), 
    pygame.image.load('./resources/images/exhaustLongF.png')
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

