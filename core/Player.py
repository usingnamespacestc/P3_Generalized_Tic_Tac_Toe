import math
from core.StateMachine import StateMachine
from core.Utils import getAllDirections


class Player:
    def __init__(self, color, boardSize, boardMap, target, testSteps=None, timeLimit=20):
        self.color = color
        self.started = True
        if self.color == "black":
            self.rivalColor = "white"
            self.number = 1  # symbol of black
            self.rivalNumber = 2  # symbol of white
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
        self.scoreModels = {"self": [], "rival": []}
        self.generateScoreModels(player="self")
        self.generateScoreModels(player="rival")
        # after this step the patterns will be replaced by their StateMachines
        self.scoreModelsToStateMachines()
        self.timeLimit = timeLimit

    def generateScoreModels(self, player="self"):
        """
        Generate a score model to evaluate patterns. Save the model to self scoreModels or rival scoreModels
        example score model(target is 5, I'm black, black is 1 white is 2 and blank is 0):
        scoreModels = [
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
        if player == "self":
            selfNumber = self.number
            rivalNumber = self.rivalNumber
        else:
            selfNumber = self.rivalNumber
            rivalNumber = self.number

        self.scoreModels[player].append([1, [rivalNumber, selfNumber, 0], False])

        for level in range(1, self.target - 1):
            score = int(math.pow(10, level))
            pattern1 = [0] + [selfNumber for _ in range(0, level)] + [0]  # like [0, 1, 1, 1, 1, 1, 0]
            self.scoreModels[player].append([score, pattern1, True])
            pattern2 = [rivalNumber] + [selfNumber for _ in range(0, level + 1)] + [0]  # like [2, 1, 1, 1, 1, 0]
            self.scoreModels[player].append([score, pattern2, False])

        self.scoreModels[player].append([int(math.pow(10, self.target - 1)),
                                        [0] + [selfNumber for _ in range(0, self.target - 1)] + [0], True])
        self.scoreModels[player].append(
            [int(math.pow(10, self.target)), [selfNumber for _ in range(0, self.target)], True])

    def scoreModelsToStateMachines(self):
        for player in self.scoreModels:
            for onePattern in self.scoreModels[player]:
                onePattern[1] = StateMachine(onePattern[1])

    def evaluate(self, boardMap=None, player="self"):
        """
        The total score of this status of boardMap
        :param boardMap: if it has a boardMap input, use that boardMap, or else use self.boardMap
        :param player: "self" or "rival", which one to evaluate
        :return: score: score evaluated for this map
        """
        if boardMap is None:
            boardMap = self.boardMap
        sumScore = 0
        # calculate score from every line and sum them up
        allDirections = getAllDirections(boardMap=boardMap, boardSize=self.boardSize)
        # because those patterns(with no # mark added) doesn't have any coverage between each other
        # so there's no need to worry about counting score of one position twice
        for oneDirection in allDirections:
            for oneLine in oneDirection:
                for oneRule in self.scoreModels[player]:
                    # assert isinstance(oneRule[1], StateMachine)
                    if oneRule[2]:
                        if oneRule[1].perfectMatch(oneLine):
                            sumScore += oneRule[0]
                    else:
                        if oneRule[1].match(oneLine):
                            sumScore += oneRule[0]
        return sumScore

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
    testBoardSize = 3
    testPlayer = Player(color="black", boardSize=testBoardSize, target=3,
                        boardMap=[0 for _ in range(0, testBoardSize * testBoardSize)])
    print("pause")
