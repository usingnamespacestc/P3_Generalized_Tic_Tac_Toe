import math
from core.StateMachine import StateMachine


class Player:
    def __init__(self, color, boardSize, boardMap, target, testSteps=None):
        self.color = color
        self.started = True
        if self.color == "black":
            self.rivalColor = "white"
            self.number = 1
            self.rivalNumber = 2
            # if continuing an existing game, set the boardMap before initializing players
            if 1 not in boardMap and 2 not in boardMap:
                self.started = False  # then should place first
        else:
            self.rivalColor = "black"
            self.number = 2
            self.rivalNumber = 1
        self.boardSize = boardSize
        self.boardMap = boardMap
        self.target = target
        self.testSteps = testSteps
        self.testCount = 0
        self.scoreModel = []
        self.generateScoreModel()

    def generateScoreModel(self):
        """
        Generate a score model to evaluate patterns.
        example score model(target is 5, I'm black, black is 1 white is 2 and blank is 0):
        scoreModel = [
            # [score, [pattern], symmetry]
            # for not symmetry pattern, we have to use match
            # for symmetry pattern, we can use perfectMatch

            # level  0
            # dead   1
            [1, [2, 1, 0], False],
            # level  1
            # living 1
            [10, [0, 1, 0], True],
            # dead   2
            [10, [2, 1, 1, 0], False],
            # level  2
            # living 2
            [100, [0, 1, 1, 0], True],
            [100, [0, 1, 0, 1, 0], True],  # mark
            # dead   3
            [100, [2, 1, 1, 1, 0], False],
            # level  3
            # living 3
            [1000, [0, 1, 1, 1, 0], True],
            [1000, [0, 1, 1, 0, 1, 0], False],  # mark
            # dead   4
            [1000, [2, 1, 1, 1, 1, 0], False],
            [1000, [2, 1, 1, 1, 0, 1], False],  # mark
            # level  5
            # living 4
            [10000, [0, 1, 1, 1, 1, 0], True],
            # level6
            # any    5
            [100000, [1, 1, 1, 1, 1], True]

            # I haven't put "mark" such as [0, 1, 1, 0, 1, 0] into consideration yet
            # adding them may cause some unknown problems due to the increasing complexity
            # the value of this type is that its potential of becoming a living 4
            # maybe put them into consideration can help reduce the layer of searching
        ]
        """
        self.scoreModel.append([1, [self.rivalNumber, self.number, 0], False])
        for level in range(1, self.target - 1):
            score = int(math.pow(10, level))
            pattern1 = [0] + [self.number for _ in range(0, level)] + [0]  # like [0, 1, 1, 1, 1, 1, 0]
            pattern2 = [self.rivalNumber] + [self.number for _ in range(0, level + 1)] + [0]  # like [2, 1, 1, 1, 1, 0]
            self.scoreModel.append([score, pattern1, True])
            self.scoreModel.append([score, pattern2, False])
        self.scoreModel.append([int(math.pow(10, self.target - 1)),
                                [0] + [self.number for _ in range(0, self.target - 1)] + [0], True])
        self.scoreModel.append([int(math.pow(10, self.target)), [self.number for _ in range(0, self.target)], True])

    def evaluate(self, position):
        """
        The total score after setting in this position
        :param position
        :return: a score
        """

        pass

    def decide(self):
        # do the test steps first if needed
        if self.testSteps is not None:
            if self.testCount < len(self.testSteps):
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


if __name__ == '__main__':
    testPlayer = Player(color="black", boardSize=3, target=10, boardMap=[0 for _ in range(0, 9)])
    print("pause")
