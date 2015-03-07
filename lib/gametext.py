import pygame
#import sys
#from pygame.locals import *
#sys.path.append('./lib')
from gamewindow import *

TEXT_COLOR = (155, 155, 255)

def initFont():
    return pygame.font.SysFont(None, 32)

def draw(text, font, surface, x, y):
    textobj = font.render(text, 1, TEXT_COLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def drawCenter(text, font, surface, y):
    textobj = font.render(text, 1, TEXT_COLOR)
    textrect = textobj.get_rect()
    textrect.centery = y
    textrect.centerx = WINDOW_WIDTH/2
    surface.blit(textobj, textrect)
