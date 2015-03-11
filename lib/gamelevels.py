
class Level:

    def __init__(self, name, duration):
        self.name = name
        self.duration = duration

    def getName(self):
        return self.name

    def getDuration(self):
        return self.duration

LEVELS = [Level('Wave 1', 1200), Level('Wave 2', 1400), Level('Wave 3', 1600), Level('Wave 4', 1800), Level('Wave 5', 2000)]

