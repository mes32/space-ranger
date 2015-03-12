"""Module corresponding to the levels of the game

"""

class Level:
    """A level of the game"""

    def __init__(self, name, duration):
        self.name = name
        self.duration = duration

    def getName(self):
        """Returns the name of the level"""
        return self.name

    def getDuration(self):
        """Returns the duration of the level in frames"""
        return self.duration

    def getWashout(self):
        """Returns the duration of the washout after the level in frames"""
        return 500

# List of each of the levels in the game
LEVELS = [
    Level('Wave 1', 2400), 
    Level('Wave 2', 2800), 
    Level('Wave 3', 3200), 
    Level('Wave 4', 3600), 
    Level('Wave 5', 4000),
    Level('Final Wave', 999999999999)
]

