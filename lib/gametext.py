"""Module corresponding to text writen on screen during the game

"""

import pygame
from gamewindow import *

TEXT_COLOR = (155, 155, 255)

def initFont():
    """Initializes the game FONT for later use.
    
    Requires that pygame was previously initialized
    """
    global FONT
    FONT = pygame.font.SysFont(None, 32)

    return FONT

def draw(text, surface, x, y):
    """Draws text on the game window at the x-y coordinates"""
    textobj = FONT.render(text, 1, TEXT_COLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def drawCenter(text, surface, y):
    """Draws text on the game window with centered x-alignment and y height"""
    textobj = FONT.render(text, 1, TEXT_COLOR)
    textrect = textobj.get_rect()
    textrect.centery = y
    textrect.centerx = WINDOW_WIDTH/2
    surface.blit(textobj, textrect)
