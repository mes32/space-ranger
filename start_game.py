import pygame, random, sys
from pygame.locals import *

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 700
TEXT_COLOR = (155, 155, 255)
BACKGROUND_COLOR = (0, 0, 0)
FRAMES_PER_SEC = 40

ASTROID_SIZE_MIN = 15
ASTROID_SIZE_MAX = 45
ASTROID_SPEED_MIN = 1
ASTROID_SPEED_MAX = 7
ASTROID_ADD_RATE = 6

PLAYER_SPEED = 5

SHOT_ADD_RATE = 6
SHOT_SPEED = 10
DAMAGE_PER_SHOT = 5  # originally 3 DAMAGE per shot

POWERUP_SPEED_MIN = 1
POWERUP_SPEED_MAX = 4
POWERUP_ADD_RATE = 300

def terminate():
    pygame.quit()
    sys.exit()

def waitForPlayerToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: # pressing escape quits
                    terminate()
                return

def playerHasHitAstroid(playerHitbox, astroidList):
    for a in astroidList:
        if playerHitbox.colliderect(a['rect']):
            astroidList.remove(a)
            return a['mass']
    return 0

def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, TEXT_COLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

# Set up pygame, the window, and the mouse cursor
pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Space Ranger')
pygame.mouse.set_visible(False)

# Set up fonts
font = pygame.font.SysFont(None, 32)

# Set up sounds
#gameOverSound = pygame.mixer.Sound('gameover.wav')
#pygame.mixer.music.load('background.mid')

# Set up player images
playerImageStandard = pygame.image.load('./resources/images/playerSpaceship.png')
playerImageHit = pygame.image.load('./resources/images/playerSpaceshipHit.png')
playerImageExplosion = pygame.image.load('./resources/images/playerSpaceshipExplosion.png')
playerImage = playerImageStandard
playerHitbox = playerImage.get_rect()
playerShotImage = pygame.image.load('./resources/images/shot.png')

# Set up astroid images
astroidImage = pygame.image.load('./resources/images/astroid.png')
astroidImageExplosion = pygame.image.load('./resources/images/astroidExplosion.png')

# Set up powerup images
shieldPowerupImage = pygame.image.load('./resources/images/powerupShield.png')
gemPowerupImage = pygame.image.load('./resources/images/powerupAstroidCore.png')


# Show the "Start" screen
shields = 100
drawText('Space Ranger', font, windowSurface, (WINDOW_WIDTH / 3), (WINDOW_HEIGHT / 3))
drawText('Press a key to start.', font, windowSurface, (WINDOW_WIDTH / 3) - 30, (WINDOW_HEIGHT / 3) + 50)
pygame.display.update()
waitForPlayerToPressKey()


topScore = 0
while True:
    # Set up the start of the game
    astroidList = []
    shotList = []
    powerupList = []
    explosionList = []

    score = 0
    hitBlink = 0
    playerImage = playerImageStandard
    playerHitbox.topleft = (WINDOW_WIDTH / 2, WINDOW_HEIGHT - 50)
    moveLeft = moveRight = moveUp = moveDown = False
    reverseCheat = slowCheat = False

    scoreAddCounter = 0
    baddieAddCounter = 0
    shotAddCounter = 0
    powerUpAddCounter = 0

    shields = 100
    playerDestroyed = False
    #pygame.mixer.music.play(-1, 0.0)

    while True: # the game loop runs while the game part is playing
        if playerDestroyed == False:
            scoreAddCounter += 1
            if scoreAddCounter == 50:
                scoreAddCounter = 0
                score += 1 # increase score

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            if event.type == KEYDOWN:
                if event.key == ord('z'):
                    reverseCheat = True
                if event.key == ord('x'):
                    slowCheat = True
                if event.key == K_LEFT or event.key == ord('a'):
                    moveRight = False
                    moveLeft = True
                if event.key == K_RIGHT or event.key == ord('d'):
                    moveLeft = False
                    moveRight = True
                if event.key == K_UP or event.key == ord('w'):
                    moveDown = False
                    moveUp = True
                if event.key == K_DOWN or event.key == ord('s'):
                    moveUp = False
                    moveDown = True

            if event.type == KEYUP:
                if event.key == ord('z'):
                    reverseCheat = False
                    score = 0
                if event.key == ord('x'):
                    slowCheat = False
                    score = 0
                if event.key == K_ESCAPE:
                        terminate()

                if event.key == K_LEFT or event.key == ord('a'):
                    moveLeft = False
                if event.key == K_RIGHT or event.key == ord('d'):
                    moveRight = False
                if event.key == K_UP or event.key == ord('w'):
                    moveUp = False
                if event.key == K_DOWN or event.key == ord('s'):
                    moveDown = False

            if event.type == MOUSEMOTION:
                # Move the player avatar with mouse cursor if needed
                playerHitbox.move_ip(event.pos[0] - playerHitbox.centerx, event.pos[1] - playerHitbox.centery)

        # Add new astroids at the top of the screen as needed
        if not reverseCheat and not slowCheat:
            baddieAddCounter += 1
        if baddieAddCounter == ASTROID_ADD_RATE:
            baddieAddCounter = 0
            baddieSize = random.randint(ASTROID_SIZE_MIN, ASTROID_SIZE_MAX)
            newBaddie = {'rect': pygame.Rect(random.randint(0, WINDOW_WIDTH-baddieSize), 0 - baddieSize, baddieSize, baddieSize),
                        'speed': random.randint(ASTROID_SPEED_MIN, ASTROID_SPEED_MAX),
                        'size': baddieSize,
                        'surface': pygame.transform.scale(astroidImage, (baddieSize, baddieSize)),
                        'mass': int(baddieSize^3),
                        'health': int(baddieSize^3),
                        }

            astroidList.append(newBaddie)

        # Add new powerUp at the top of the screen, if needed
        powerUpAddCounter += 1
        if powerUpAddCounter == POWERUP_ADD_RATE:
            powerUpAddCounter = 0
            powerUpType = random.randint(0,4)
            if powerUpType == 1 or (shields < 30 and (powerUpType == 2 or powerUpType == 3)):
                powerUpSize = shieldPowerupImage.get_width()
                newPowerUp = {'rect': pygame.Rect(random.randint(0, WINDOW_WIDTH-powerUpSize), 0 - powerUpSize, powerUpSize, powerUpSize),
                              'speed': random.randint(POWERUP_SPEED_MIN, POWERUP_SPEED_MAX),
                              'surface': pygame.transform.scale(shieldPowerupImage, (powerUpSize, powerUpSize)),
                              'type': 'shield',
                              }
            else:
                powerUpWidth = gemPowerupImage.get_width()
                powerUpHeight = gemPowerupImage.get_height()
                newPowerUp = {'rect': pygame.Rect(random.randint(0, WINDOW_WIDTH-powerUpWidth), 0 - powerUpHeight, powerUpHeight, powerUpWidth),
                              'speed': random.randint(POWERUP_SPEED_MIN, POWERUP_SPEED_MAX),
                              'surface': pygame.transform.scale(gemPowerupImage, (powerUpWidth, powerUpHeight)),
                              'type': 'plus',
                              }
            powerupList.append(newPowerUp)

        # Move the player around
        if moveLeft and playerHitbox.left > 0:
            playerHitbox.move_ip(-1 * PLAYER_SPEED, 0)
        if moveRight and playerHitbox.right < WINDOW_WIDTH:
            playerHitbox.move_ip(PLAYER_SPEED, 0)
        if moveUp and playerHitbox.top > 0:
            playerHitbox.move_ip(0, -1 * PLAYER_SPEED)
        if moveDown and playerHitbox.bottom < WINDOW_HEIGHT:
            playerHitbox.move_ip(0, PLAYER_SPEED)

        # Move the mouse cursor to match the player
        pygame.mouse.set_pos(playerHitbox.centerx, playerHitbox.centery)

        # Add new shots as needed
        shotAddCounter += 1
        if shotAddCounter == SHOT_ADD_RATE:
            shotAddCounter = 0
            newShot = {'rect': pygame.Rect(playerHitbox.centerx-3, playerHitbox.centery-12, 5, 1),}
            shotList.append(newShot)

        # Move astroids down the screen
        for a in astroidList:
            if not reverseCheat and not slowCheat:
                a['rect'].move_ip(0, a['speed'])
            elif reverseCheat:
                a['rect'].move_ip(0, -5)
            elif slowCheat:
                a['rect'].move_ip(0, 1)

        # Delete astroids that have passed the bottom of the screen
        for a in astroidList[:]:
            if a['rect'].top > WINDOW_HEIGHT:
                astroidList.remove(a)

        # Move the explosions down and update their animation
        for e in explosionList:
            e['rect'].move_ip(0, e['speed'])
            e['stage'] += 1
            explosionSize = e['size']
            if e['stage'] == 1:
                e['surface'] = pygame.transform.scale(astroidImageExplosion, (int(explosionSize*0.75), int(explosionSize*0.75)))
                e['size'] = int(explosionSize*0.8)
                e['rect'].move_ip(int((explosionSize - e['size'])/2), int((explosionSize - e['size'])/2))
            elif e['stage'] < 6:
                e['surface'] = pygame.transform.scale(astroidImageExplosion, (int(explosionSize*1.2), int(explosionSize*1.2)))
                e['size'] = int(explosionSize*1.25)
                e['rect'].move_ip(int((explosionSize - e['size'])/2), int((explosionSize - e['size'])/2))
            elif e['stage'] == 6:
                explosionList.remove(e)

        # Delete explosions that have fallen past the bottom or burned out
        for e in explosionList[:]:
            if e['rect'].top > WINDOW_HEIGHT:
                explosionList.remove(e)

        # Move player shots up.
        for s in shotList:
            s['rect'].move_ip(0, -SHOT_SPEED)

        # Delete player shots that have moved past the top
        for s in shotList[:]:
            if s['rect'].top < 0:
                shotList.remove(s)

        # Move the powerups down
        for p in powerupList:
            p['rect'].move_ip(0, p['speed'])

        # Check if any powerups have hit the player
        for p in powerupList[:]:
            if p['rect'].colliderect(playerHitbox):
                powerupList.remove(p)
                if (p['type'] == 'shield'):
                    shields += 25
                    if shields > 100:
                        shields = 100
                        score += 10
                elif (p['type'] == 'plus'):
                    score += 30

        # Check if any shots have hit an astroid
        for a in astroidList[:]:
            for s in shotList[:]:
                if s['rect'].colliderect(a['rect']):
                    shotList.remove(s)
                    a['health'] -= DAMAGE_PER_SHOT
                    if a['health'] <= 0:
                        astroidList.remove(a)
                        explosionSize = a['size']
                        newExplosion = {'rect': a['rect'],
                        'speed': a['speed'],
                        'size': explosionSize,
                        'surface': pygame.transform.scale(astroidImageExplosion, (explosionSize, explosionSize)),
                        'stage': 2,
                        }
                        explosionList.append(newExplosion)
                    break

        # Check if the player has hit an astroid
        damageTaken = playerHasHitAstroid(playerHitbox, astroidList)
        if damageTaken > 0:
            playerImage = playerImageHit
            hitBlink = 8
            shields -= damageTaken
            if shields < 0:
                shields = 0
                playerDestroyed = True
                playerImage = playerImageExplosion
                hitBlink = 8
                pygame.display.update()
                if score > topScore:
                    topScore = score # set new top score

        # Draw the game world on the window.
        windowSurface.fill(BACKGROUND_COLOR)

        # Draw each shot
        for s in shotList:
            windowSurface.blit(playerShotImage, s['rect'])

        # Draw each baddie
        for a in astroidList:
            windowSurface.blit(a['surface'], a['rect'])

        # Draw each explosion
        for e in explosionList:
            windowSurface.blit(e['surface'], e['rect'])

        # Draw each powerup
        for p in powerupList:
            windowSurface.blit(p['surface'], p['rect'])

        # Draw the player's rectangle
        windowSurface.blit(playerImage, playerHitbox)

        # Animate spaceship shields responding to damage.
        # Or animate spaceship exploding upon destruction.
        if hitBlink != 0:
            hitBlink -= 1
            if hitBlink == 0:
                if playerDestroyed == True:
                    break
                else:
                    playerImage = playerImageStandard

        # Draw the score and top score.
        drawText('Score: %s' % (score), font, windowSurface, 10, 0)
        drawText('Top Score: %s' % (topScore), font, windowSurface, 10, 25)
        drawText('Shields: %s' % (shields), font, windowSurface, 10, 50)

        pygame.display.update()
        mainClock.tick(FRAMES_PER_SEC)

    # Stop the game and show the "Game Over" screen.
    #pygame.mixer.music.stop()
    #gameOverSound.play()

    drawText('GAME OVER', font, windowSurface, (WINDOW_WIDTH / 3), (WINDOW_HEIGHT / 3))
    drawText('Score: %s Top Score: %s' % (score, topScore), font, windowSurface, (WINDOW_WIDTH / 3), (WINDOW_HEIGHT / 3) + 50)
    drawText('Press a key to play again...', font, windowSurface, (WINDOW_WIDTH / 3), (WINDOW_HEIGHT / 3) + 100)
    pygame.display.update()
    waitForPlayerToPressKey()

    #gameOverSound.stop()
