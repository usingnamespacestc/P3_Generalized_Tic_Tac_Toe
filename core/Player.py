import math
from core.StateMachine import StateMachine
from core.Utils import getAllDirections
# import copy
import time
import config


class Player:
    def __init__(self, color, boardSize, boardMap, target, testSteps=None):
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
        self.winScore = math.pow(10, self.target)
        self.generateScoreModels(player="self")
        self.generateScoreModels(player="rival")
        # after this step the patterns will be replaced by their StateMachines
        self.scoreModelsToStateMachines()
        self.offsetRange = [_ for _ in range(-self.target, self.target + 1)]
        # self.offsetRange = [_ for _ in range(1 - self.target, self.target)]
        # self.offsetRange = [-2, -1, 0, 1, 2]
        self.startTime = None  # time that starts one round of search
        self.searchCount = 0
        self.cutCount = 0
        self.bestPosition = [0, 0]

    def generateScoreModels(self, player="self"):
        """
        Generate a score model to evaluate patterns. Save the model to self scoreModels or rival scoreModels
        example score model(target is 5, I'm black, black is 1 white is 2 and blank is 0, 3 other obstacles(edges)):
        scoreModels = [
            # [score, [pattern], symmetry]
            # for not symmetry pattern, we have to use match
            # for symmetry pattern, we can use perfectMatch

            # level  0
                # dead   1
                [1, [2, 1, 0], False],
                [1, [3, 1, 0], False],
            # level  1
                # living 1
                [10, [0, 1, 0], True],
                # dead   2
                [10, [2, 1, 1, 0], False],
                [10, [3, 1, 1, 0], False],
            # level  2
                # living 2
                [100, [0, 1, 1, 0], True],
                [100, [0, 1, 0, 1, 0], True],  # mark
                # dead   3
                [100, [2, 1, 1, 1, 0], False],
                [100, [3, 1, 1, 1, 0], False],
            # level  3
                # living 3
                [1000, [0, 1, 1, 1, 0], True],
                [1000, [0, 1, 1, 0, 1, 0], False],  # mark
                # dead   4
                [1000, [2, 1, 1, 1, 1, 0], False],
                [1000, [3, 1, 1, 1, 1, 0], False],
                [1000, [2, 1, 1, 1, 0, 1], False],  # mark
            # level  5
                # living 4
                [10000, [0, 1, 1, 1, 1, 0], True],
            # level6
                # any    5
                [100000, [1, 1, 1, 1, 1], True]

            # I haven't put "mark" such as [0, 1, 1, 0, 1, 0] into consideration yet
            # adding them may cause some known problems due to the increasing complexity
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
        self.scoreModels[player].append([1, [3, selfNumber, 0], False])

        for level in range(1, self.target - 1):
            score = int(math.pow(config.scoreLevel, level))
            pattern1 = [0] + [selfNumber for _ in range(0, level)] + [0]  # like [0, 1, 1, 1, 1, 1, 0]
            self.scoreModels[player].append([score, pattern1, True])
            pattern2 = [rivalNumber] + [selfNumber for _ in range(0, level + 1)] + [0]  # like [2, 1, 1, 1, 1, 0]
            self.scoreModels[player].append([score, pattern2, False])
            pattern3 = [3] + [selfNumber for _ in range(0, level + 1)] + [0]  # like [3, 1, 1, 1, 1, 0]
            self.scoreModels[player].append([score, pattern3, False])

        self.scoreModels[player].append([int(math.pow(config.scoreLevel, self.target - 1)),
                                         [0] + [selfNumber for _ in range(0, self.target - 1)] + [0], True])
        self.scoreModels[player].append(
            [int(math.pow(config.scoreLevel, self.target + 1)), [selfNumber for _ in range(0, self.target)], True])

    def scoreModelsToStateMachines(self):
        for player in self.scoreModels:
            for onePattern in self.scoreModels[player]:
                onePattern[1] = StateMachine(onePattern[1])

    def calculateScore(self, boardMap=None, player="self"):
        """
        The total score of this status of boardMap
        :param boardMap: if it has a boardMap input, use that boardMap, or else use self.boardMap
        :param player: "self" or "rival", which one to evaluate
        :return: score: score evaluated for this map
        """
        if boardMap is None:
            boardMap = self.boardMap
        # need to take care of the edges, assume the edges are surrounded
        # if player == "self":
        #     surround = self.rivalNumber
        # else:
        #     surround = self.number
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
                        if oneRule[1].perfectMatch([3] + oneLine + [3]):
                            sumScore += oneRule[0]
                    else:
                        if oneRule[1].match([3] + oneLine + [3]):
                            sumScore += oneRule[0]
        return sumScore

    def placeOne(self, position: [int, int], player: str, boardMap=None):
        if boardMap is None:
            boardMap = self.boardMap
        if player == "self":
            boardMap[position[1] * self.boardSize + position[0]] = self.number
        else:
            boardMap[position[1] * self.boardSize + position[0]] = self.rivalNumber

    def removeOne(self, position: [int, int], boardMap=None):
        if boardMap is None:
            boardMap = self.boardMap
        boardMap[position[1] * self.boardSize + position[0]] = 0

    def evaluate(self, player=None, boardMap=None):
        if player is None:
            player = "self"
        if player == "self":
            active = "self"
            passive = "rival"
        else:
            passive = "self"
            active = "rival"
        activeScore = self.calculateScore(boardMap, player=active)
        passiveScore = self.calculateScore(boardMap, player=passive)
        # print("pause")
        return activeScore - passiveScore / config.aggressive

    def getAllPossiblePositions(self, boardMap=None):
        def indexExist(index):
            if index >= self.boardSize or index < 0:
                return False
            return True

        if boardMap is None:
            boardMap = self.boardMap
        allPossiblePositions = []
        for i in range(0, self.boardSize):
            for j in range(0, self.boardSize):
                isNearby = False
                if boardMap[i * self.boardSize + j] == 0:
                    for offsetX in self.offsetRange:
                        for offsetY in self.offsetRange:
                            # if not (offsetX == 0 and offsetY == 0):
                            x = j + offsetX
                            y = i + offsetY
                            if indexExist(x) and indexExist(y):
                                if boardMap[y * self.boardSize + x] != 0:
                                    isNearby = True
                                    break
                        if isNearby:
                            break
                if isNearby:
                    allPossiblePositions.append([[j, i], -0x3f3f3f3f])  # default score is -inf
        return allPossiblePositions

    def showMap(self, boardMap=None):
        if boardMap is None:
            boardMap = self.boardMap
        for i in range(0, self.boardSize):
            row = ""
            for j in range(0, self.boardSize):
                row += str(boardMap[i * self.boardSize + j])
            print(row)

    def sortedPossiblePositions(self, boardMap=None, player=None, reverse=True):
        if boardMap is None:
            boardMap = self.boardMap
        if player is None:
            player = "self"

        sortedPositions = self.getAllPossiblePositions(boardMap=boardMap)
        for i in range(0, len(sortedPositions)):
            self.placeOne(sortedPositions[i][0], player, boardMap)
            sortedPositions[i][1] = self.evaluate(player, boardMap)
            self.removeOne(sortedPositions[i][0], boardMap)
        return sorted(sortedPositions, key=lambda score: score[1], reverse=reverse)

    def negativeMaxRecursive(self, player="self", alpha=-0x3f3f3f3f, beta=0x3f3f3f3f, depth=0, boardMap=None):
        # the score is the last player's score after last action
        score = self.evaluate(player="self", boardMap=boardMap)
        # the score is this player's score after last players action
        # score = self.evaluate(player=player, boardMap=thisBoardMap)
        if config.debug:
            self.showMap(boardMap)
            if depth % 2 == 0:
                print("after rival")
            else:
                print("after self")
            print("count:", self.searchCount, "score:", score)
        if depth % 2 == 0:
            score *= -1

        # if depth > config.depthLimit or \
        #         score >= math.pow(10, self.target) * 0.9 or \
        #         time.time() - self.startTime > config.timeLimit:
        #     return score
        if depth > config.depthLimit:
            return score
        if time.time() - self.startTime > config.timeLimit:
            return score
        # preparation
        if boardMap is None:
            thisBoardMap = [_ for _ in self.boardMap]
        else:
            # already a new one, so the boardMap in the parameter don't need to be deepcopy
            thisBoardMap = [_ for _ in boardMap]
        if 0 not in thisBoardMap:
            return score
        if config.sorting:
            possiblePositions = self.sortedPossiblePositions(boardMap=thisBoardMap, reverse=depth % 2 == 0)
        else:
            possiblePositions = self.getAllPossiblePositions(boardMap=thisBoardMap)
        # it would be better if the positions are sorted
        for nextPosition in possiblePositions:
            self.searchCount += 1
            self.placeOne(nextPosition[0], player=player, boardMap=thisBoardMap)
            # self.showMap(thatBoardMap)
            # print("")
            value = self.negativeMaxRecursive(player="rival" if player == "self" else "self", alpha=-beta, beta=-alpha,
                                              depth=depth + 1, boardMap=thisBoardMap)
            self.removeOne(nextPosition[0], boardMap=thisBoardMap)

            # alpha-beta
            if value > alpha:
                if depth == 0:
                    self.bestPosition[0], self.bestPosition[1] = nextPosition[0][0], nextPosition[0][1]
                alpha = value
            # pruning
            if config.pruning:
                if alpha >= beta:
                    self.cutCount += 1
                    break
        return alpha

    # not used, using negativeMax instead
    def miniMax(self):
        def getMax(boardMap, depth, alpha=-float("inf"), beta=float("inf")):
            maxScore = None
            bestPosition = None
            thisBoardMap = [_ for _ in boardMap]
            if config.sorting:
                possiblePositions = self.sortedPossiblePositions(boardMap=boardMap, reverse=True)
            else:
                possiblePositions = self.getAllPossiblePositions(boardMap=boardMap)
            score = self.evaluate(player="self", boardMap=boardMap)
            if config.debug:
                self.showMap(boardMap=thisBoardMap)
                print("max layer, count:", self.searchCount, "score:", score)
            if depth > config.depthLimit:
                return score, None
            if time.time() - self.startTime > config.timeLimit:
                return score, None
            if len(possiblePositions) == 0:
                return score, None
            for nextPosition in possiblePositions:
                self.searchCount += 1
                self.placeOne(nextPosition[0], player="self", boardMap=thisBoardMap)
                score = getMin(thisBoardMap, depth + 1, alpha, beta)[0]
                self.removeOne(nextPosition[0], boardMap=thisBoardMap)
                if score is not None and (maxScore is None or score > maxScore):
                    maxScore = score
                    bestPosition = nextPosition[0]
                if config.pruning:
                    if score is not None and score > beta:
                        return score, nextPosition
                    if score is not None and score > alpha:
                        alpha = score
            return maxScore, bestPosition

        def getMin(boardMap, depth, alpha=-float("inf"), beta=float("inf")):
            minScore = None
            bestPosition = None
            thisBoardMap = [_ for _ in boardMap]
            if config.sorting:
                possiblePositions = self.sortedPossiblePositions(boardMap=boardMap, reverse=True)
            else:
                possiblePositions = self.getAllPossiblePositions(boardMap=boardMap)
            score = self.evaluate(player="self", boardMap=boardMap)
            if config.debug:
                self.showMap(boardMap=thisBoardMap)
                print("min layer, count:", self.searchCount, "score:", score)
            if depth > config.depthLimit:
                return score, None
            if time.time() - self.startTime > config.timeLimit:
                return score, None
            if len(possiblePositions) == 0:
                return score, None
            for nextPosition in possiblePositions:
                self.searchCount += 1
                self.placeOne(nextPosition[0], player="rival", boardMap=thisBoardMap)
                score = getMax(thisBoardMap, depth + 1, alpha, beta)[0]
                self.removeOne(nextPosition[0], boardMap=thisBoardMap)
                if score is not None and (minScore is None or score < minScore):
                    minScore = score
                    bestPosition = nextPosition[0]
                if config.pruning:
                    if score is not None and score < alpha:
                        return score, nextPosition
                    if score is not None and score < beta:
                        beta = score
            return minScore, bestPosition

        return getMax([_ for _ in self.boardMap], 0)[1]

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
            return math.ceil(self.boardSize / 2) - 1, math.ceil(self.boardSize / 2) - 1

        # game already get started
        else:
            # print("search starts here")
            self.startTime = time.time()
            if config.negativeMax:
                self.negativeMaxRecursive()
            if config.miniMax:
                self.bestPosition = self.miniMax()
            print("search count:", self.searchCount, "cut count:", self.cutCount)
            self.searchCount = 0
            self.cutCount = 0
            return self.bestPosition


if __name__ == '__main__':
    # testBoardSize = 5
    # initBoardMap = [0 for _ in range(0, testBoardSize * testBoardSize)]
    """
    0 2 1
    1 0 1
    2 2 0
    initBoardMap[1] = 2
    initBoardMap[2] = 1
    initBoardMap[3] = 1
    initBoardMap[5] = 1
    initBoardMap[6] = 2
    initBoardMap[7] = 2
    """
    # initBoardMap = [0, 0, 0, 0, 0, 0,
    #                 0, 0, 0, 0, 0, 0,
    #                 0, 0, 0, 2, 0, 0,
    #                 0, 1, 0, 2, 0, 0,
    #                 0, 0, 0, 0, 0, 0,
    #                 0, 0, 0, 0, 0, 0]
    # initBoardMap = [0, 0, 0, 0, 0,
    #                 0, 0, 0, 0, 0,
    #                 0, 0, 2, 2, 0,
    #                 0, 0, 0, 0, 0,
    #                 0, 0, 0, 0, 0]
    initBoardMap = [0, 1, 0, 0,
                    0, 2, 1, 0,
                    0, 0, 2, 0,
                    0, 0, 0, 0]
    # initBoardMap = [0, 0, 0, 0,
    #                 0, 0, 0, 0,
    #                 0, 0, 0, 0,
    #                 0, 0, 0, 2]
    # initBoardMap = [1, 1, 2, 2,
    #                 1, 2, 2, 3,
    #                 0, 0, 1, 2,
    #                 1, 1, 0, 1]
    # initBoardMap = [3, 2, 0,
    #                 0, 2, 3,
    #                 2, 3, 0]
    # initBoardMap = [3, 3, 0,
    #                 3, 2, 0,
    #                 0, 3, 3]
    # initBoardMap = [0, 0, 0,
    #                 0, 2, 0,
    #                 0, 0, 0]
    # initBoardMap = [1, 2, 0,
    #                 0, 1, 2,
    #                 0, 1, 2]
    # initBoardMap = [1, 2, 1,
    #                 0, 1, 2,
    #                 2, 1, 0]
    testPlayer = Player(color="white", boardSize=int(math.sqrt(len(initBoardMap))), target=3,
                        boardMap=initBoardMap)
    testPlayer.evaluate()
    print(testPlayer.decide())
    print("pause")
