import requests
import json
import os
import config


def loadSettings():
    if "core" in os.listdir():
        os.chdir("core")
    with open("settings.json", "r", encoding="UTF-8") as f:
        settings = json.load(f)
        return settings


class APIMaster:
    def __init__(self):
        # settings = loadSettings()
        # self.x_api_key = settings["x-api-key"]
        # self.user = settings["user"]["id"]
        # self.teams = settings["teams"]
        # self.origin = settings["origin"]
        # self.uri = settings["uri"]
        # self.currentGame = settings["currentGame"]
        # self.boardSize = settings["boardSize"]
        # self.target = settings["target"]
        self.x_api_key = config.x_api_key
        self.user = config.user_id
        self.teamID = config.team_id
        self.origin = config.origin
        self.uri = config.uri
        self.currentGame = config.currentGame
        self.boardSize = config.boardSize
        self.target = config.target
        self.boardMap = [[None] * self.boardSize for _ in range(self.boardSize)]

    def commonRequest(self, requestType="POST", params=None, payload=None):
        url = self.origin + self.uri
        headers = {
            "userid": str(self.user),
            "x-api-key": self.x_api_key,
            "User-Agent": "PostmanRuntime/7.29.0"
        }
        response = requests.request(requestType, url=url, headers=headers, data=payload, params=params)
        return response

    def createGame(self, team2, team1=None, boardSize=None, target=None):
        if team1 is None:
            team1 = self.teamID
        payload = {
            "type": "game",
            "gameType": "TTT",
            "teamId1": str(team1),
            "teamId2": str(team2)
        }
        if boardSize is not None:
            self.boardSize = boardSize
            payload["boardSize"] = str(boardSize)
        if target is not None:
            self.target = target
            payload["target"] = str(target)
        response = self.commonRequest("POST", payload=payload)
        if response.ok:
            res = response.json()
            self.target = target
            self.boardSize = boardSize
            self.boardMap = [[None] * self.boardSize for _ in range(self.boardSize)]
            return res["gameId"]
        else:
            print(response.text)

    def makeMove(self, teamId: int, move: [int], gameId=None):
        if gameId is None:
            gameId = self.currentGame
        payload = {
            "teamId": teamId,
            "move": str(move[0]) + "," + str(move[1]),
            "type": "move",
            "gameId": gameId
        }
        response = self.commonRequest("POST", payload=payload)
        res = response.json()
        if res["code"] == "OK":
            return True
        else:
            print(res["message"])
            return False

    def getMoves(self):
        print(self.currentGame, "get moves")

    # not using this, since I already have getBoardMap
    def getBoardString(self):
        print(self.currentGame, "get board string")

    def getBoardMap(self, gameId=None):
        if gameId is None:
            gameId = self.currentGame
        params = {
            "type": "boardMap",
            "gameId": str(gameId)
        }
        res = self.commonRequest("GET", params=params)
        # print("game:", self.currentGame, "get board map:")
        if res.json()["output"] is not None:
            output = json.loads(res.json()["output"])
            for key in output:
                pos = key.split(",")
                pos[0] = int(pos[0])
                pos[1] = int(pos[1])
                (self.boardMap[pos[1]][pos[0]]) = True if output[key] == "O" else False
            return json.loads(res.json()["output"])
        return []


if __name__ == "__main__":
    if "core" not in os.listdir():
        os.chdir("../")
    testGame = APIMaster()
    # testGame.createGame()
    testGame.getBoardMap()
    # testGame.makeMove(teamId=1293, move=[1, 0])
