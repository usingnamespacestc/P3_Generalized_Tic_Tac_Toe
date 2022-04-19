"""
name: Utils.py
author: usingnamespacestc@gmail.com
version: 1.0
create: forgotten
description:
    Some tool functions that don't know where to put.
"""


def getAllDirections(boardSize, boardMap):
    """
    eg:
    boardSize = 3
    boardMap = [1, 2, 3,
                4, 5, 6,
                7, 8, 9]
    return [[[1, 2, 3], [4, 5, 6], [7, 8, 9]],
            [[1, 4, 7], [2, 5, 8], [3, 6, 9]],
            [[3], [2, 6], [1, 5, 9], [4, 8], [7]],
            [[1], [2, 4], [3, 5, 7], [6, 8], [9]]]
    :param boardSize:
    :param boardMap:
    :return:
    """
    # 4 directions
    return [
        # direction 0 -
        [boardMap[i * boardSize:(i + 1) * boardSize] for i in range(0, boardSize)],
        # direction 1 |
        [[boardMap[i * boardSize + j] for i in range(0, boardSize)] for j in range(0, boardSize)],
        # direction 2 \
        [[boardMap[i * boardSize + i + boardSize - j]
          for i in range(0, j)] for j in range(1, boardSize + 1)] +
        [[boardMap[j * boardSize + i * boardSize + i]
          for i in range(0, boardSize - j)] for j in range(1, boardSize)],
        # direction 3 /
        [[boardMap[i * boardSize + j - i - 1] for i in range(0, j)]
         for j in range(1, boardSize + 1)] +
        [[boardMap[i * boardSize + j * boardSize + boardSize - i - 1] for i in range(0, boardSize - j)]
         for j in range(1, boardSize)]
    ]
