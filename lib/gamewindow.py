"""Module corresponding to the main game window

"""

import pygame

WINDOW_WIDTH = 600   # Height of the game window in pixels
WINDOW_HEIGHT = 700  # Width of the game window in pixels

BACKGROUND_COLOR = (0, 0, 0)  # Black background color for game window
FRAMES_PER_SEC = 40           # Rate at which game window is repainted (40x per second)

def initWindowSurface():
    """Initializes the game window.

    Sets the window title bar caption, turns off the mouse cursor, and sets 
    dimensions.
    """
    pygame.display.set_caption('space-ranger')
    pygame.mouse.set_visible(False)
    return pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
