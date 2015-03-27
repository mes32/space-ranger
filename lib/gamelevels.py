"""Module corresponding to the levels of the game

"""

import astroid
import powerup
from gamewindow import *

class Level:
    """A level of the game"""

    def __init__(self, name, duration, sizeRange, speedRange, sigmaDegrees, addRate):
        self.name = name
        self.duration = duration * FRAMES_PER_SEC
        self.astroidField = astroid.AstroidField(sizeRange, speedRange, sigmaDegrees, addRate)

    def getName(self):
        """Returns the name of the level"""
        return self.name

    def getDuration(self):
        """Returns the duration of the level in frames"""
        return self.duration

    def getWashout(self):
        """Returns the duration of the washout after the level in frames"""
        return 12 * FRAMES_PER_SEC

    def getAstroidField(self):
        """Returns the astroid source for the level"""
        return self.astroidField

    def getPowerupSource(self):
        """Returns the astroid source for the level"""
        return powerup.PowerupSource()

# List of each of the levels in the game
LEVELS = [
    Level('Wave 1', 60, (20, 30), (2, 4), 2, 10),
    Level('Wave 2', 80, (15, 35), (1, 6), 2, 9),
    Level('Wave 3', 100, (15, 45), (1, 7), 3, 8),
    Level('Wave 4', 120, (15, 45), (1, 7), 4, 7),
    Level('Wave 5', 140, (15, 45), (1, 7), 4, 6),
    Level('Final Wave', 999999999999, (15, 45), (1, 8), 5, 4)
]

