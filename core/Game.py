# about multiprocessing:
# https://blog.csdn.net/lomodays207/article/details/106384512
# https://www.runoob.com/w3cnote/python-single-thread-multi-thread-and-multi-process.html
import multiprocessing
import threading
# import ctypes
import core.GUI
from core.Player import Player
from core.StateMachine import StateMachine


def generateScoreModel(target):
    pass


def gameStatus(boardSize=12, boardMap=None, target=6):
    """
    Get to know if the game is draw, black or white wins, or still keep going on
    :param boardSize:
    :param boardMap:
    :param target:
    :return: the winner ("black" or "white") or "draw" or "keep" means the game keeps going
    """
    if hasattr(multiprocessing, "sharedctypes"):
        if isinstance(boardMap, multiprocessing.sharedctypes.SynchronizedArray):  # multiprocessing.Array
            if 0 not in boardMap:
                return "draw"
            for color in range(1, 3):
                # color 1 black, 2 white
                referee = StateMachine([color for _ in range(0, target)])
                win = False
                # 4 directions
                # 1
                for i in range(0, boardSize):
                    if referee.perfectMatch(boardMap[i * boardSize:(i + 1) * boardSize]):
                        win = True
                # 2
                for j in range(0, boardSize):
                    if referee.perfectMatch([boardMap[i * boardSize + j] for i in range(0, boardSize)]):
                        win = True
                # 3
                res = [[boardMap[i * boardSize + i + boardSize - j] for i in range(0, j)] for j in
                       range(1, boardSize + 1)] + \
                      [[boardMap[j * boardSize + i * boardSize + i] for i in range(0, boardSize - j)] for j in
                       range(1, boardSize)]
                for one in res:
                    if referee.perfectMatch(one):
                        win = True
                # 4
                res = [[boardMap[i * boardSize + j - i - 1] for i in range(0, j)] for j in range(1, boardSize + 1)] + \
                      [[boardMap[i * boardSize + j * boardSize + boardSize - i - 1] for i in range(0, boardSize - j)]
                       for j in range(1, boardSize)]
                for one in res:
                    if referee.perfectMatch(one):
                        win = True

                if win:
                    return "black" if color == 1 else "white"
            return "keep"


def singleStep(boardSize, boardMap, position: [int, int], color):
    x = position[0]
    y = position[1]
    boardMap[y * boardSize + x] = 1 if color == "black" else 2
    print(color, "placed at", position)


def main(mode="offline", guiOn=True, boardSize=12, target=6):
    multiprocessing.set_start_method("spawn")
    print("Starting Game...")
    print("Main process:", multiprocessing.current_process().name, multiprocessing.current_process().pid)
    print("Main thread:", threading.current_thread().name, threading.current_thread().native_id)

    # 0 in boardMap means none, 1 means black, 2 means white
    boardMap = multiprocessing.Array("i", [0 for _ in range(0, boardSize * boardSize)])
    if guiOn:
        # initialize gui
        guiProcess = multiprocessing.Process(target=core.GUI.Board, args=(boardSize, boardMap))
        # guiProcess.daemon = True  # when the parent process is killed, kill it as well # doesn't work well
        guiProcess.start()
        # print("pause")
    # I am both black and white
    if mode == "offline":
        print("playing at offline mode")
        playerBlack = Player(boardMap=boardMap, boardSize=boardSize, color="black")
        playerWhite = Player(boardMap=boardMap, boardSize=boardSize, color="white")
        # loop between player black and player white, black first
        """
            loop:
                black decide
                check game over
                white decide
                check game over
        """
        while gameStatus(boardSize, boardMap, target) == "keep":
            position = playerBlack.decide()
            singleStep(boardSize, boardMap, position, "black")

    # playing as black or white
    elif mode == "online":
        print("playing game at online mode")
        """
            if I am black:
                loop:
                    I decide
                    check game over
                    wait for opponent decide
                    check game over
        """


if __name__ == '__main__':
    main("offline", guiOn=True, boardSize=2, target=3)
