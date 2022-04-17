# about multiprocessing:
# https://blog.csdn.net/lomodays207/article/details/106384512
import multiprocessing
import threading
# import ctypes
import core.GUI


def gameOver(boardMap, target):
    pass


def main(mode="offline", guiOn=True, boardSize=12, target=6):
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
    # I am both black and white
    if mode == "offline":
        print("playing at offline mode")
    # playing as black or white
    elif mode == "online":
        print("playing game at online mode")


if __name__ == '__main__':
    main("offline", guiOn=True, boardSize=6, target=3)
