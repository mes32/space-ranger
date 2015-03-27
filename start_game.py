"""Main script to start space-ranger game

"""

import sys
import time
import pygame

import lib.gametext as gametext
import lib.playership as playership
import lib.astroid as astroid
import lib.explosion as explosion
import lib.playershot as playershot
import lib.powerup as powerup
import lib.gamelevels as gamelevels

from pygame.locals import *
from lib.gamewindow import *

def terminateGame():
    """Quits pygame and exits"""

    pygame.quit()
    sys.exit()

def waitForPlayerToPressKey():
    """Waits for the player to press a key on the keyboard"""

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminateGame()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: # pressing escape quits
                    terminateGame()
                return

def waitForPlayerYesNo():
    """Waits for the player to press a key on the keyboard"""

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminateGame()
            if event.type == KEYDOWN:
                if event.key == ord('n') or event.key == K_ESCAPE: # pressing escape quits
                    terminateGame()
                elif event.key == ord('y'):
                    return

def playerHasHitAstroid(playerHitbox, astroidList):
    """Returns the damage recieved if the player has colided with an astroid"""

    for a in astroidList:
        if playerHitbox.colliderect(a.getRect()):
            astroidList.remove(a)
            return a.getMass()
    return 0

def showStartScreen():
    """Show the Start screen before the first time playing"""

    windowSurface.fill(BACKGROUND_COLOR)
    gametext.drawCenter('Space Ranger', windowSurface, (WINDOW_HEIGHT / 3))
    gametext.drawCenter('Press a key to start.', windowSurface, (WINDOW_HEIGHT / 3) + 50)
    pygame.display.update()
    waitForPlayerToPressKey()

def showLevelScreen(levelName):
    """Show the level name before the level"""

    # Display a blank screen
    windowSurface.fill(BACKGROUND_COLOR)
    pygame.display.update()
    time.sleep(0.5)

    # Display the name of the level
    windowSurface.fill(BACKGROUND_COLOR)
    gametext.drawCenterWithBars(levelName, windowSurface, (WINDOW_HEIGHT / 3))
    pygame.display.update()
    time.sleep(0.5)

    # Count down the start of the level
    for i in [3, 2, 1]:
        windowSurface.fill(BACKGROUND_COLOR)
        gametext.drawCenterWithBars(levelName, windowSurface, (WINDOW_HEIGHT / 3))
        gametext.drawCenter('Ready...' + str(i), windowSurface, (WINDOW_HEIGHT / 3) + 100)
        pygame.display.update()
        time.sleep(0.8)

    # After last count display GO!
    windowSurface.fill(BACKGROUND_COLOR)
    gametext.drawCenterWithBars(levelName, windowSurface, (WINDOW_HEIGHT / 3))
    gametext.drawCenter('Ready...GO!', windowSurface, (WINDOW_HEIGHT / 3) + 100)
    pygame.display.update()
    time.sleep(1.2)


def showGameOverScreen():
    """Show the Game Over screen inbetween rounds"""

    #pygame.mixer.music.stop()
    #gameOverSound.play()

    # Show the "Game Over" screen
    gametext.drawCenterWithBars('GAME OVER', windowSurface, (WINDOW_HEIGHT / 3))
    gametext.drawCenter('Score: %s' % (player.getScore()), windowSurface, (WINDOW_HEIGHT / 3) + 50)
    gametext.drawCenter('Top Score: %s' % (topScore), windowSurface, (WINDOW_HEIGHT / 3) + 100)
    gametext.drawCenter('Play again?    [y]es or [n]o', windowSurface, (WINDOW_HEIGHT / 3) + 200)
    pygame.display.update()
    waitForPlayerYesNo()

    #gameOverSound.stop()

def drawFrame(windowSurface, player, topScore, astroidList, shotList, explosionList, powerupList):
    """Draw a single frame of world on the screen"""

    # Clear screen with background color
    windowSurface.fill(BACKGROUND_COLOR)

    # Draw each player shot
    for s in shotList:
        s.draw(windowSurface)

    # Draw each astroid
    for a in astroidList:
        a.draw(windowSurface)

    # Draw each explosion
    for e in explosionList:
        e.draw(windowSurface)

    # Draw each powerup
    for p in powerupList:
        p.draw(windowSurface)

    # Draw the player's spaceship
    player.draw(windowSurface)

    # Draw the score and top score.
    gametext.drawHUD('Score: %s' % (player.getScore()), windowSurface, 10, 5)
    gametext.drawHUD('Shields: %s' % (player.getShields()), windowSurface, 10, 30)

    # Update the game display
    pygame.display.update()

def moveAll(player, astroidList, shotList, explosionList, powerupList):
    """Move all the game elements for a single frame"""

    # Move the player's ship around
    player.move()

    # Move astroids down the screen
    for a in astroidList:
        a.move()
        if a.isOffScreen():
            astroidList.remove(a)

    # Move the explosions down and update their animation
    for e in explosionList:
        e.move()
        if e.isOffScreen():
            explosionList.remove(e)

    # Move player shots up and delete those that have moved past the top
    for s in shotList:
        s.move()
        if s.isOffScreen():
            shotList.remove(s)

    # Move the powerups down and delete ones that have moved past the bottom
    for p in powerupList:
        p.move()
        if p.isOffScreen():
            powerupList.remove(p)

def checkCollisions(player, astroidList, shotList, powerupList):
    """Check for all relavant collisions between game elements"""

    # Check if any powerups have hit the player
    for p in powerupList:
        if p.getRect().colliderect(player.getHitbox()):
            powerupList.remove(p)
            if (p.getType() == 'shield'):
                player.addShields(25)
            elif (p.getType() == 'plus'):
                player.addScore(30)

    # Check if any shots have hit astroids
    for s in shotList:
        for a in astroidList:
            if s.getRect().colliderect(a.getRect()):
                shotList.remove(s)
                if a.isDestroyed():
                    astroidList.remove(a)
                    explosionList.append(explosion.Explosion(a))
                else:
                    a.takeDamage(s.getDamage())
                break

    # Check if the player has hit an astroid
    damageTaken = playerHasHitAstroid(player.getHitbox(), astroidList)
    if damageTaken > 0:
        player.subShields(damageTaken)

def initGame():
    """Initialize pygame, main clock, game window, and font"""
    pygame.init()
    gametext.initFont()
    global mainClock
    mainClock = pygame.time.Clock()
    global windowSurface
    windowSurface = initWindowSurface()
    global topScore
    topScore = 0

    # Set up sounds
    #gameOverSound = pygame.mixer.Sound('gameover.wav')
    #pygame.mixer.music.load('background.mid')


initGame()
showStartScreen()

while True:

    #pygame.mixer.music.play(-1, 0.0)

    gameOver = False
    player = playership.PlayerShip()

    for level in gamelevels.LEVELS:

        if gameOver == True:
            break

        showLevelScreen(level.getName())

        frameCounter = 0

        # Initialize lists of non-player sprites
        astroidList = []
        shotList = []
        powerupList = []
        explosionList = []

        player.reset()
        astroidSource = level.getAstroidField()
        powerupSource = level.getPowerupSource()

        while frameCounter < level.getDuration() and gameOver == False:
        # main game loop runs continuously while the game is playing

            # Add new astroids, player shots, and powerups as needed
            shotList.extend(player.cycleWeapon())
            if frameCounter < level.getDuration() - level.getWashout():
                astroidList.extend(astroidSource.cycle())
                powerupList.extend(powerupSource.cycle(player.getShields()))

            # Listen for keyboard and mouse inputs
            for event in pygame.event.get():
                if event.type == QUIT:
                    terminateGame()
                if event.type == KEYDOWN:
                    player.keydownMove(event.key)
                if event.type == KEYUP:
                    if event.key == K_ESCAPE:
                        terminateGame()
                    else:
                        player.keyupMove(event.key)
                if event.type == MOUSEMOTION:
                    player.mouseMove(event)

            # Move and update all game elements/sprites
            moveAll(player, astroidList, shotList, explosionList, powerupList)

            # Check for collisions between game elements/sprites
            checkCollisions(player, astroidList, shotList, powerupList)

            # Draw a single frame of the game world on the windowSurface
            drawFrame(windowSurface, player, topScore, astroidList, shotList, explosionList, powerupList)

            # Check if player was destroyed and break main game loop
            if player.isDestroyed():
                if player.getScore() > topScore:
                    topScore = player.getScore() # set new top score
                gameOver = True
                drawFrame(windowSurface, player, topScore, astroidList, shotList, explosionList, powerupList)
                break

            mainClock.tick(FRAMES_PER_SEC)
            frameCounter += 1

    # Stop the game and show the "Game Over" screen.
    showGameOverScreen()

