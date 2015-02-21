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
DAMAGE_PER_SHOT = 6  # originally 3 DAMAGE per shot

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

def playerHasHitBaddie(playerRect, baddies):
    for b in baddies:
        if playerRect.colliderect(b['rect']):
            baddies.remove(b)
            return b['mass']
    return 0

def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, TEXT_COLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

# set up pygame, the window, and the mouse cursor
pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Space Ranger')
pygame.mouse.set_visible(False)

# set up fonts
font = pygame.font.SysFont(None, 32)

# set up sounds
#gameOverSound = pygame.mixer.Sound('gameover.wav')
#pygame.mixer.music.load('background.mid')

# set up images
playerImageStandard = pygame.image.load('./resources/images/playerSpaceship.png')
playerImageHit = pygame.image.load('./resources/images/playerSpaceshipHit.png')
playerImageExploded = pygame.image.load('./resources/images/playerSpaceshipExplosion.png')
playerImage = playerImageStandard
playerRect = playerImage.get_rect()
baddieImage = pygame.image.load('./resources/images/astroid.png')
baddieImage3 = pygame.image.load('./resources/images/astroidExplosion.png')
shotImage = pygame.image.load('./resources/images/shot.png')

powerUpShieldImage = pygame.image.load('./resources/images/powerupShield.png')
powerUpPlusImage = pygame.image.load('./resources/images/powerupAstroidCore.png')


# show the "Start" screen
shields = 100
drawText('Space Ranger', font, windowSurface, (WINDOW_WIDTH / 3), (WINDOW_HEIGHT / 3))
drawText('Press a key to start.', font, windowSurface, (WINDOW_WIDTH / 3) - 30, (WINDOW_HEIGHT / 3) + 50)
pygame.display.update()
waitForPlayerToPressKey()


topScore = 0
while True:
    # set up the start of the game
    baddies = []
    shots = []
    powerUps = []
    explosions = []
    score = 0
    hitBlink = 0
    playerImage = playerImageStandard
    playerRect.topleft = (WINDOW_WIDTH / 2, WINDOW_HEIGHT - 50)
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
                # If the mouse moves, move the player where the cursor is.
                playerRect.move_ip(event.pos[0] - playerRect.centerx, event.pos[1] - playerRect.centery)

        # Add new baddies at the top of the screen, if needed.
        if not reverseCheat and not slowCheat:
            baddieAddCounter += 1
        if baddieAddCounter == ASTROID_ADD_RATE:
            baddieAddCounter = 0
            baddieSize = random.randint(ASTROID_SIZE_MIN, ASTROID_SIZE_MAX)
            newBaddie = {'rect': pygame.Rect(random.randint(0, WINDOW_WIDTH-baddieSize), 0 - baddieSize, baddieSize, baddieSize),
                        'speed': random.randint(ASTROID_SPEED_MIN, ASTROID_SPEED_MAX),
                        'size': baddieSize,
                        'surface': pygame.transform.scale(baddieImage, (baddieSize, baddieSize)),
                        'mass': int(baddieSize^3),
                        'health': int(baddieSize^3),
                        }

            baddies.append(newBaddie)

        # Add new powerUp at the top of the screen, if needed.
        powerUpAddCounter += 1
        if powerUpAddCounter == POWERUP_ADD_RATE:
            powerUpAddCounter = 0
            powerUpType = random.randint(0,4)
            if powerUpType == 1 or (shields < 30 and (powerUpType == 2 or powerUpType == 3)):
                powerUpSize = powerUpShieldImage.get_width()
                newPowerUp = {'rect': pygame.Rect(random.randint(0, WINDOW_WIDTH-powerUpSize), 0 - powerUpSize, powerUpSize, powerUpSize),
                              'speed': random.randint(POWERUP_SPEED_MIN, POWERUP_SPEED_MAX),
                              'surface': pygame.transform.scale(powerUpShieldImage, (powerUpSize, powerUpSize)),
                              'type': 'shield',
                              }
            else:
                powerUpWidth = powerUpPlusImage.get_width()
                powerUpHeight = powerUpPlusImage.get_height()
                newPowerUp = {'rect': pygame.Rect(random.randint(0, WINDOW_WIDTH-powerUpWidth), 0 - powerUpHeight, powerUpHeight, powerUpWidth),
                              'speed': random.randint(POWERUP_SPEED_MIN, POWERUP_SPEED_MAX),
                              'surface': pygame.transform.scale(powerUpPlusImage, (powerUpWidth, powerUpHeight)),
                              'type': 'plus',
                              }
            powerUps.append(newPowerUp)

        # Move the player around.
        if moveLeft and playerRect.left > 0:
            playerRect.move_ip(-1 * PLAYER_SPEED, 0)
        if moveRight and playerRect.right < WINDOW_WIDTH:
            playerRect.move_ip(PLAYER_SPEED, 0)
        if moveUp and playerRect.top > 0:
            playerRect.move_ip(0, -1 * PLAYER_SPEED)
        if moveDown and playerRect.bottom < WINDOW_HEIGHT:
            playerRect.move_ip(0, PLAYER_SPEED)

        # Move the mouse cursor to match the player.
        pygame.mouse.set_pos(playerRect.centerx, playerRect.centery)

        # Add new shots as needed
        shotAddCounter += 1
        if shotAddCounter == SHOT_ADD_RATE:
            shotAddCounter = 0
            newShot = {'rect': pygame.Rect(playerRect.centerx-3, playerRect.centery-12, 5, 1),}
            shots.append(newShot)

        # Move the baddies down.
        for b in baddies:
            if not reverseCheat and not slowCheat:
                b['rect'].move_ip(0, b['speed'])
            elif reverseCheat:
                b['rect'].move_ip(0, -5)
            elif slowCheat:
                b['rect'].move_ip(0, 1)

         # Delete baddies that have fallen past the bottom.
        for b in baddies[:]:
            if b['rect'].top > WINDOW_HEIGHT:
                baddies.remove(b)

        # Move the explosions down and update animation.
        for e in explosions:
            e['rect'].move_ip(0, e['speed'])
            e['stage'] += 1
            explosionSize = e['size']
            if e['stage'] == 1:
                e['surface'] = pygame.transform.scale(baddieImage3, (int(explosionSize*0.75), int(explosionSize*0.75)))
                e['size'] = int(explosionSize*0.8)
                e['rect'].move_ip(int((explosionSize - e['size'])/2), int((explosionSize - e['size'])/2))
            elif e['stage'] < 6:
                e['surface'] = pygame.transform.scale(baddieImage3, (int(explosionSize*1.2), int(explosionSize*1.2)))
                e['size'] = int(explosionSize*1.25)
                e['rect'].move_ip(int((explosionSize - e['size'])/2), int((explosionSize - e['size'])/2))
            elif e['stage'] == 6:
                explosions.remove(e)

         # Delete explosions that have fallen past the bottom or burned out.
        for e in explosions[:]:
            if e['rect'].top > WINDOW_HEIGHT:
                explosions.remove(e)

        # Move the shots up.
        for s in shots:
            s['rect'].move_ip(0, -SHOT_SPEED)

         # Delete shots that have moved past the top.
        for s in shots[:]:
            if s['rect'].top < 0:
                shots.remove(s)

        # Move the powerups down.
        for p in powerUps:
            p['rect'].move_ip(0, p['speed'])

        # Check if any powerups have hit the player.
        for p in powerUps[:]:
            if p['rect'].colliderect(playerRect):
                powerUps.remove(p)
                if (p['type'] == 'shield'):
                    shields += 25
                    if shields > 100:
                        shields = 100
                        score += 10
                elif (p['type'] == 'plus'):
                    score += 30

        # Check if any shots have hit baddies.
        for b in baddies[:]:
            for s in shots[:]:
                if s['rect'].colliderect(b['rect']):
                    shots.remove(s)
                    b['health'] -= DAMAGE_PER_SHOT
                    if b['health'] <= 0:
                        baddies.remove(b)
                        explosionSize = b['size']
                        newExplosion = {'rect': b['rect'],
                        'speed': b['speed'],
                        'size': explosionSize,
                        'surface': pygame.transform.scale(baddieImage3, (explosionSize, explosionSize)),
                        'stage': 2,
                        }
                        explosions.append(newExplosion)
                    break

        # Check if any of the baddies have hit the player.
        damageTaken = playerHasHitBaddie(playerRect, baddies)
        if damageTaken > 0:
            playerImage = playerImageHit
            hitBlink = 8
            shields -= damageTaken
            if shields < 0:
                shields = 0
                playerDestroyed = True
                playerImage = playerImageExploded
                hitBlink = 8
                pygame.display.update()
                if score > topScore:
                    topScore = score # set new top score

        # Draw the game world on the window.
        windowSurface.fill(BACKGROUND_COLOR)

        # Draw each shot
        for s in shots:
            windowSurface.blit(shotImage, s['rect'])

        # Draw each baddie
        for b in baddies:
            windowSurface.blit(b['surface'], b['rect'])

        # Draw each explosion
        for e in explosions:
            windowSurface.blit(e['surface'], e['rect'])

        # Draw each powerup
        for p in powerUps:
            windowSurface.blit(p['surface'], p['rect'])

        # Draw the player's rectangle
        windowSurface.blit(playerImage, playerRect)

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
