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
import asyncio
import time

FULL_SIZE_RATIO = 0.95
PIECE_SIZE_RATIO = 0.618
globalTk = None  # Tk()
globalCanvas = None  # Canvas()
globalBoardSize = 0
globalBoardStatus = []


async def asyncTest():
    time.sleep(5)


def drawBoard(boardSize=9):
    global globalTk
    global globalCanvas
    global globalBoardSize
    globalBoardSize = boardSize
    globalTk = Tk()
    globalCanvas = Canvas(globalTk, width=600, height=600)
    globalCanvas.pack()
    # globalCanvas.create_rectangle(0, 0, 50, 50)  # （10,10）为正方形右上角坐标，（50,50）为正方形右下角坐标
    # globalCanvas.create_oval(0, 0, 50, 50, fill="white")
    globalTk.after(0, update)
    globalTk.mainloop()


def update():
    if isinstance(globalCanvas, Canvas):
        updateAll(globalCanvas)
    if isinstance(globalTk, Tk):
        globalTk.after(10, update)


def updateAll(canvas: Canvas):
    canvasHeight = canvas.winfo_height()
    canvasWidth = canvas.winfo_width()
    # print("h:", canvasHeight, "w:", canvasWidth)
    singleBlankSize, singlePieceSize = calculateSingleSize(min(canvasWidth, canvasHeight), globalBoardSize)
    allPositions = calculateAllPositions(canvasWidth, canvasHeight, singleBlankSize)
    canvas.delete(tkinter.ALL)
    for position in allPositions:
        drawSingleBlank(canvas, position[0], position[1], singleBlankSize)


# totalSize is min(height, width)
def calculateSingleSize(totalSize, boardSize):
    # print(totalHeight)
    singleBlankSize = totalSize * FULL_SIZE_RATIO / boardSize
    # print(singleBlankSize)
    singlePieceSize = singleBlankSize * PIECE_SIZE_RATIO
    return singleBlankSize, singlePieceSize


def calculateAllPositions(canvasWidth, canvasHeight, singleBlankSize) -> [[float, float]]:
    totalNumbers = globalBoardSize * globalBoardSize
    allPositions = [[0, 0] for _ in range(0, totalNumbers)]
    for i in range(0, globalBoardSize):
        for j in range(0, globalBoardSize):
            allPositions[i * globalBoardSize + j] = [0, 0]
    base = (min(canvasWidth, canvasHeight) * ((1 - FULL_SIZE_RATIO) / 2))
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
    for i in range(0, globalBoardSize):
        for j in range(0, globalBoardSize):
            allPositions[i * globalBoardSize + j][0] = basePosition[0] + j * singleBlankSize
            allPositions[i * globalBoardSize + j][1] = basePosition[1] + i * singleBlankSize
    # global debugCounter
    # debugCounter += 1
    # print("debugCounter:", debugCounter)
    # if debugCounter == 100:
    #     print(allPositions)

    return allPositions


def drawSingleBlank(canvas: Canvas, centerX, centerY, singleSize):
    canvas.create_rectangle(centerX - singleSize / 2, centerY - singleSize / 2,
                            centerX + singleSize / 2, centerY + singleSize / 2)


def drawSinglePiece(canvas: Canvas, centerX, centerY, singleSize, color):
    canvas.create_oval(centerX - singleSize / 2, centerY - singleSize / 2,
                       centerX + singleSize / 2, centerY + singleSize / 2, fill=color)


if __name__ == "__main__":
    drawBoard()
