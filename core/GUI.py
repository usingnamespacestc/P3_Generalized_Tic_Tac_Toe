"""
name: GUI.py
author: usingnamespacestc@gmail.com
version: 1.0
create: forgotten
description:
    Show the board and game status.
history:
    2022-xx-xx: I hate writing GUI using python.
"""
import tkinter
from tkinter import *
from tkinter import messagebox
import random
import multiprocessing
import threading


# import asyncio
# import time


class Board:
    def __init__(self, boardSize=12, boardMap=None):
        self.FULL_SIZE_RATIO = 0.95
        self.PIECE_SIZE_RATIO = 0.618
        self.tk = None  # Tk()
        self.canvas = None  # Canvas()
        self.boardSize = 0
        self.refreshDelay = 300
        if boardMap is not None:
            self.boardMap = boardMap
        else:
            self.boardMap = []
        print("GUI initializing...")
        print("GUI process:", multiprocessing.current_process().name, multiprocessing.current_process().pid)
        print("GUI thread:", threading.current_thread().name, threading.current_thread().native_id)
        self.createBoard(boardSize=boardSize)

    def noClosing(self):
        realQuit = messagebox.askokcancel("Warning:", "Don't close the window without eliminating the process.\n"
                                          "Are you sure you want to close this window?")
        if realQuit:
            self.tk.destroy()

    def createBoard(self, boardSize=12):
        self.boardSize = boardSize
        self.tk = Tk()
        self.tk.title("P3_Generalized_Tic_Tac_Toe")
        self.tk.protocol("WM_DELETE_WINDOW", self.noClosing)
        self.canvas = Canvas(self.tk, width=600, height=600)
        self.canvas.pack()
        # canvas.create_rectangle(0, 0, 50, 50)  # （10,10）为正方形右上角坐标，（50,50）为正方形右下角坐标
        # canvas.create_oval(0, 0, 50, 50, fill="white")
        self.tk.after(1, self.update)
        self.tk.mainloop()

    def update(self):
        if isinstance(self.canvas, Canvas):
            self.updateAll()
        if isinstance(self.tk, Tk):
            self.tk.after(self.refreshDelay, self.update)

    def updateAll(self):
        # calculate size
        canvasHeight = self.canvas.winfo_height()
        canvasWidth = self.canvas.winfo_width()
        # print("h:", canvasHeight, "w:", canvasWidth)
        singleBlankSize, singlePieceSize = self.calculateSingleSize(
            min(canvasWidth, canvasHeight), self.boardSize)
        # calculate positions
        allPositions = self.calculateAllPositions(canvasWidth, canvasHeight, singleBlankSize)
        # clear current map
        self.canvas.delete(tkinter.ALL)

        for i in range(0, self.boardSize):
            for j in range(0, self.boardSize):
                # the position is actually (j, i), for i is row and j is col
                # which means (x, y) is map[j][i]
                # draw board
                self.drawSingleBlank(allPositions[i * self.boardSize + j][0],
                                     allPositions[i * self.boardSize + j][1],
                                     singleSize=singleBlankSize)
                # draw pieces
                if self.boardMap[i * self.boardSize + j] == 1:
                    color = "black"
                elif self.boardMap[i * self.boardSize + j] == 2:
                    color = "white"
                else:
                    color = None
                if color is not None:
                    self.drawSinglePiece(allPositions[i * self.boardSize + j][0],
                                         allPositions[i * self.boardSize + j][1],
                                         singleSize=singlePieceSize, color=color)

    # totalSize is min(height, width)
    def calculateSingleSize(self, totalSize, boardSize):
        # print(totalHeight)
        singleBlankSize = totalSize * self.FULL_SIZE_RATIO / boardSize
        # print(singleBlankSize)
        singlePieceSize = singleBlankSize * self.PIECE_SIZE_RATIO
        return singleBlankSize, singlePieceSize

    def calculateAllPositions(self, canvasWidth, canvasHeight, singleBlankSize) -> [[float, float]]:
        totalNumbers = self.boardSize * self.boardSize
        allPositions = [[0, 0] for _ in range(0, totalNumbers)]
        for i in range(0, self.boardSize):
            for j in range(0, self.boardSize):
                allPositions[i * self.boardSize + j] = [0, 0]
        base = (min(canvasWidth, canvasHeight) * ((1 - self.FULL_SIZE_RATIO) / 2))
        # print(base)
        basePosition = [base, base]
        halfBlankSize = singleBlankSize / 2
        if canvasHeight > canvasWidth:
            verticalOffset = (canvasHeight - canvasWidth) / 2
            basePosition[0] += halfBlankSize
            basePosition[1] += halfBlankSize + verticalOffset
        else:
            basePosition[0] += halfBlankSize
            basePosition[1] += halfBlankSize
        for i in range(0, self.boardSize):
            for j in range(0, self.boardSize):
                allPositions[i * self.boardSize + j][0] = basePosition[0] + j * singleBlankSize
                allPositions[i * self.boardSize + j][1] = basePosition[1] + i * singleBlankSize

        return allPositions

    def drawSingleBlank(self, centerX, centerY, singleSize):
        self.canvas.create_rectangle(centerX - singleSize / 2, centerY - singleSize / 2,
                                     centerX + singleSize / 2, centerY + singleSize / 2)

    def drawSinglePiece(self, centerX, centerY, singleSize, color):
        self.canvas.create_oval(centerX - singleSize / 2, centerY - singleSize / 2,
                                centerX + singleSize / 2, centerY + singleSize / 2, fill=color)


if __name__ == "__main__":
    testSize = 16
    gui = Board(boardSize=testSize, boardMap=[random.randint(0, 2) for _ in range(0, testSize * testSize)])
