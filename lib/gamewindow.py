import pygame


WINDOW_WIDTH = 600
WINDOW_HEIGHT = 700

BACKGROUND_COLOR = (0, 0, 0)
FRAMES_PER_SEC = 40

def initWindowSurface():
    pygame.display.set_caption('Space Ranger')
    pygame.mouse.set_visible(False)
    return pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
