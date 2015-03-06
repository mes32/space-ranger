import sys
import random
import pygame
from pygame.locals import *

sys.path.append('./lib')

import gametext
import playershot
import astroid
import powerup
from gamewindow import *
from powerup import *

BACKGROUND_COLOR = (0, 0, 0)
FRAMES_PER_SEC = 40

PLAYER_SPEED = 5

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
        if playerHitbox.colliderect(a.getRect()):
            astroidList.remove(a)
            return a.getMass()
    return 0

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

# Set up explosion images
astroidImageExplosion = pygame.image.load('./resources/images/astroidExplosion.png')

# Show the "Start" screen
shields = 100
gametext.drawCenter('Space Ranger', font, windowSurface, (WINDOW_HEIGHT / 3))
gametext.drawCenter('Press a key to start.', font, windowSurface, (WINDOW_HEIGHT / 3) + 50)
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

    scoreAddCounter = 0
    powerUpAddCounter = 0

    shields = 100
    playerDestroyed = False
    railgun = playershot.Railgun()
    astroidSource = astroid.AstroidField()
    powerupSource = powerup.PowerupSource()
    #pygame.mixer.music.play(-1, 0.0)

    while True: # main game loop runs continuously while the game is playing

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            if event.type == KEYDOWN:
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
        astroidList.extend(astroidSource.cycle())

        # Add new powerups at the top of the screen as needed
        powerupList.extend(powerupSource.cycle(shields))

        # Add new shots as needed
        shotList.extend(railgun.cycle(playerHitbox))

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

        # Move astroids down the screen
        for a in astroidList:
            a.move()
            if a.isOffScreen():
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
            # Delete explosions that have fallen past the bottom
            if e['rect'].top > WINDOW_HEIGHT:
                explosionList.remove(e)

        # Move player shots up and delete those that have moved past the top
        for shot in shotList:
            shot.move()
            if shot.isOffScreen():
                shotList.remove(shot)

        # Move the powerups down and delete ones that have moved past the bottom
        for p in powerupList:
            p.move()
            if p.isOffScreen():
                powerupList.remove(p)

        # Check if any powerups have hit the player
        for p in powerupList:
            if p.getRect().colliderect(playerHitbox):
                powerupList.remove(p)
                if (p.getType() == 'shield'):
                    shields += 25
                    if shields > 100:
                        shields = 100
                        score += 10
                elif (p.getType() == 'plus'):
                    score += 30

        # Check if any shots have hit astroids
        for a in astroidList:
            for s in shotList:
                shotRect = s.getRect()
                astroidRect = a.getRect()
                if shotRect.colliderect(astroidRect):
                    shotList.remove(s)
                    a.takeDamage(s.getDamage())
                    if a.isDestroyed():
                        astroidList.remove(a)
                        explosionSize = a.getSize()
                        newExplosion = {'rect': a.getRect(),
                        'speed': a.getSpeed(),
                        'size': explosionSize,
                        'surface': pygame.transform.scale(astroidImageExplosion, (explosionSize, explosionSize)),
                        'stage': 2,
                        }
                        explosionList.append(newExplosion)

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
        for shot in shotList:
            shot.draw(windowSurface)

        # Draw each astroid
        for a in astroidList:
            a.draw(windowSurface)

        # Draw each explosion
        for e in explosionList:
            windowSurface.blit(e['surface'], e['rect'])

        # Draw each powerup
        for p in powerupList:
            p.draw(windowSurface)

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
        gametext.draw('Score: %s' % (score), font, windowSurface, 10, 5)
        gametext.draw('Top Score: %s' % (topScore), font, windowSurface, 10, 30)
        gametext.draw('Shields: %s' % (shields), font, windowSurface, 10, 55)

        pygame.display.update()
        mainClock.tick(FRAMES_PER_SEC)

    # Stop the game and show the "Game Over" screen.
    #pygame.mixer.music.stop()
    #gameOverSound.play()

    # Show "Game Over" screen
    gametext.drawCenter('GAME OVER', font, windowSurface, (WINDOW_HEIGHT / 3))
    gametext.drawCenter('Score: %s Top Score: %s' % (score, topScore), font, windowSurface, (WINDOW_HEIGHT / 3) + 50)
    gametext.drawCenter('Press any key to play again', font, windowSurface, (WINDOW_HEIGHT / 3) + 100)
    pygame.display.update()
    waitForPlayerToPressKey()

    #gameOverSound.stop()
