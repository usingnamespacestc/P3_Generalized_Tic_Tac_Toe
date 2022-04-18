import math


class Player:
    def __init__(self, color, boardSize, boardMap, testSteps=None):
        self.color = color
        self.started = True
        if self.color == "black":
            self.started = False  # then should place first
        self.boardSize = boardSize
        self.boardMap = boardMap
        self.testSteps = testSteps
        self.testCount = 0

    def decide(self):
        if self.testSteps is not None and self.testCount < len(self.testSteps):
            self.testCount += 1
            return self.testSteps[self.testCount - 1]
        # the whole board is empty and this player is the first one
        if not self.started:
            self.started = True
            # just place in the center
            return math.ceil(self.boardSize / 2), math.ceil(self.boardSize / 2)
        # game already get started
        else:
            print("search starts here")
            return [0, 0]
