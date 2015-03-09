import sys
sys.path.append('./lib')

import random
import pygame
import gametext
import playership
import astroid
import explosion
import playershot
import powerup

from pygame.locals import *
from gamewindow import *

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

def showStartScreen():
    # Show the "Start" screen
    gametext.drawCenter('Space Ranger', windowSurface, (WINDOW_HEIGHT / 3))
    gametext.drawCenter('Press a key to start.', windowSurface, (WINDOW_HEIGHT / 3) + 50)
    pygame.display.update()
    waitForPlayerToPressKey()

def showGameOverScreen():
    # Stop the game and show the "Game Over" screen.
    #pygame.mixer.music.stop()
    #gameOverSound.play()

    # Show "Game Over" screen
    gametext.drawCenter('GAME OVER', windowSurface, (WINDOW_HEIGHT / 3))
    gametext.drawCenter('Score: %s Top Score: %s' % (player.getScore(), topScore), windowSurface, (WINDOW_HEIGHT / 3) + 50)
    gametext.drawCenter('Press any key to play again', windowSurface, (WINDOW_HEIGHT / 3) + 100)
    pygame.display.update()
    waitForPlayerToPressKey()

    #gameOverSound.stop()


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
    # Set up the start of the game
    astroidList = []
    shotList = []
    powerupList = []
    explosionList = []

    moveLeft = moveRight = moveUp = moveDown = False
    player = playership.PlayerShip()

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
                player.mouseMove(event)

        # Add new astroids at the top of the screen as needed
        astroidList.extend(astroidSource.cycle())

        # Add new powerups at the top of the screen as needed
        powerupList.extend(powerupSource.cycle(player.getShields()))

        # Add new shots as needed
        shotList.extend(railgun.cycle(player.getHitbox()))

        # Move the player's ship around
        if moveLeft and player.notLeftEdge():
            player.moveLeft()
        if moveRight and player.notRightEdge():
            player.moveRight()
        if moveUp and player.notTopEdge():
            player.moveUp()
        if moveDown and player.notBottomEdge():
            player.moveDown()

        # Move the mouse cursor to match the player
        player.mouseCursorFollow()

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
            if p.getRect().colliderect(player.getHitbox()):
                powerupList.remove(p)
                if (p.getType() == 'shield'):
                    player.addShields(25)
                elif (p.getType() == 'plus'):
                    player.addScore(30)

        # Check if any shots have hit astroids
        for a in astroidList:
            for s in shotList:
                if s.getRect().colliderect(a.getRect()):
                    shotList.remove(s)
                    a.takeDamage(s.getDamage())
                    if a.isDestroyed():
                        astroidList.remove(a)
                        explosionList.append(explosion.Explosion(a))

        # Check if the player has hit an astroid
        damageTaken = playerHasHitAstroid(player.getHitbox(), astroidList)
        if damageTaken > 0:
            player.subShields(damageTaken)

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
            e.draw(windowSurface)

        # Draw each powerup
        for p in powerupList:
            p.draw(windowSurface)

        # Draw the player's spaceship
        player.draw(windowSurface)

        # Draw the score and top score.
        gametext.draw('Score: %s' % (player.getScore()), windowSurface, 10, 5)
        gametext.draw('Top Score: %s' % (topScore), windowSurface, 10, 30)
        gametext.draw('Shields: %s' % (player.getShields()), windowSurface, 10, 55)

        pygame.display.update()
        mainClock.tick(FRAMES_PER_SEC)

        if player.getShields() == 0:
            if player.getScore() > topScore:
                topScore = player.getScore() # set new top score
            break

    # Stop the game and show the "Game Over" screen.
    showGameOverScreen()

