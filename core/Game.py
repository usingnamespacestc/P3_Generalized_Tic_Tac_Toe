# about multiprocessing:
# https://blog.csdn.net/lomodays207/article/details/106384512
# https://www.runoob.com/w3cnote/python-single-thread-multi-thread-and-multi-process.html
import multiprocessing
import threading
# import ctypes
import core.GUI
import time
from core.Player import Player
from core.StateMachine import StateMachine
from core.Utils import getAllDirections


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
            # the above two lines are to eliminate warnings
            if 0 not in boardMap:
                return "draw"
            for color in range(1, 3):
                # color 1 black, 2 white
                referee = StateMachine([color for _ in range(0, target)])
                # 4 directions
                allDirections = getAllDirections(boardSize=boardSize, boardMap=boardMap)
                for oneDirection in allDirections:
                    for oneLine in oneDirection:
                        if referee.perfectMatch(oneLine):
                            # someone wins
                            return "black" if color == 1 else "white"
            return "keep"


def singleStep(boardSize, boardMap, position: [int, int], color):
    x = position[0]
    y = position[1]
    boardMap[y * boardSize + x] = 1 if color == "black" else 2


# also works for multiprocessing.sharedctypes.c_long_Array
# the result is a normal list
def deepCopyArray(target):
    return [_ for _ in target]


def main(mode="offline", guiOn=True, boardSize=12, target=6, startState=None):
    multiprocessing.set_start_method("spawn")
    print("Starting Game...")
    print("Main process:", multiprocessing.current_process().name, multiprocessing.current_process().pid)
    print("Main thread:", threading.current_thread().name, threading.current_thread().native_id)

    # 0 in boardMap means none, 1 means black, 2 means white
    boardMap = multiprocessing.Array("i", [0 for _ in range(0, boardSize * boardSize)])
    if startState is not None:
        for i in range(0, len(startState)):
            boardMap[i] = startState[i]

    if guiOn:
        # initialize gui
        guiProcess = multiprocessing.Process(target=core.GUI.Board, args=(boardSize, boardMap))
        # guiProcess.daemon = True  # when the parent process is killed, kill it as well # doesn't work well
        guiProcess.start()
        # print("pause")
    # I am both black and white
    if mode == "offline":
        print("playing at offline mode")
        playerBlack = Player(boardMap=boardMap, boardSize=boardSize, color="black", target=target)
        playerWhite = Player(boardMap=boardMap, boardSize=boardSize, color="white", target=target)
        # loop between player black and player white, black first
        """
        loop:
            black decide
            check game over
            white decide
            check game over
        """
        # TODO: used for adding breakpoints, remember to delete this
        print("pause")
        while True:
            # black turn
            startTime = time.time()
            position = playerBlack.decide()
            print(int(time.time() - startTime), "seconds used")
            singleStep(boardSize, boardMap, position, "black")
            if gameStatus(boardSize, boardMap, target) != "keep":
                break

            # white turn
            startTime = time.time()
            position = playerWhite.decide()
            print(int(time.time() - startTime), "seconds used")
            singleStep(boardSize, boardMap, position, "white")
            if gameStatus(boardSize, boardMap, target) != "keep":
                break

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

    return gameStatus(boardSize, boardMap, target)


if __name__ == '__main__':
    main("offline", guiOn=True, boardSize=3, target=3)
