import pygame

SHOT_IMAGE = pygame.image.load('./resources/images/shot.png')

SHOT_ADD_RATE = 6
SHOT_SPEED = 10
DAMAGE_PER_SHOT = 5  # originally 3 DAMAGE per shot

shotAddCounter = 0

#def loadImage():
#    return pygame.image.load('./resources/images/shot.png')

def addNew(playerHitbox, counter):
    if counter % SHOT_ADD_RATE == 0:
        counter = 0
        newShot = {'rect': pygame.Rect(playerHitbox.centerx-3, playerHitbox.centery-12, 5, 16),}
        return [newShot]
    else:
        return []

def move(shot):
    shot['rect'].move_ip(0, -SHOT_SPEED)

def isOffScreen(shot):
    if shot['rect'].bottom < 0:
        return True
    else:
        return False

def draw(shot, windowSurface):
    windowSurface.blit(SHOT_IMAGE, shot['rect'])

def getDamage(shot):
    return DAMAGE_PER_SHOT
