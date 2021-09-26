import requests
import logging
from flask import Flask, request
from sseclient import SSEClient
import json

from codeitsuisse import app

logger = logging.getLogger(__name__)

board = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0]
]


def resetBoard():
    global board
    board = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ]


moves = {
    "NW": (0, 0),
    "N": (0, 1),
    "NE": (0, 2),
    "W": (1, 0),
    "C": (1, 1),
    "E": (1, 2),
    "SW": (2, 0),
    "S": (2, 1),
    "SE": (2, 2)
}

# haveWePlayed = True


def with_requests(url, headers):
    return requests.get(url, stream=True, headers=headers)


def generateStream(battleId):
    global haveWePlayed, board
    url = f'https://cis2021-arena.herokuapp.com/tic-tac-toe/start/{battleId}'
    headers = {'Accept': 'text/event-stream'}
    response = with_requests(url, headers)
    client = SSEClient(response)

    for event in client.events():
        data = json.loads(event.data)
        print(data)
        # if not haveWePlayed:
        #     submit_move({
        #         "action": "(╯°□°)╯︵ ┻━┻"
        #     })
        #     resetBoard()
        #     return
        if "youAre" in data:
            player_choice = data["youAre"]
            if player_choice == 'O':
                haveWePlayed = False
                playTurn()
                Opponent_choice = 'X'
            else:
                Opponent_choice = 'O'
            continue

        if "action" in data and data["action"] == "putSymbol":
            if data["position"] not in moves:
                submit_move({
                    "action": "(╯°□°)╯︵ ┻━┻"
                })
                resetBoard()
                break

            if data["player"] == player_choice:
                moveRow, moveCol = moves[data["position"]]
                playMove(board, moveRow, moveCol, player_choice)
            else:
                isValid = OpponentTurn(Opponent_choice, data["position"])
                if isValid:
                    playTurn()
            continue

        if "action" in data and data["action"] == "(╯°□°)╯︵ ┻━┻" and data["player"] == Opponent_choice:
            submit_move({
                "action": "(╯°□°)╯︵ ┻━┻"
            })
            resetBoard()
            return

        if "winner" in data:
            resetBoard()
    return


@app.route('/tic-tac-toe', methods=['POST'])
def evaluate_tictactoe():
    global battleId
    data = request.get_json()
    battleId = data["battleId"]
    generateStream(battleId)
    return "working"


def submit_move(payload):
    url = f"https://cis2021-arena.herokuapp.com/tic-tac-toe/play/{battleId}"
    headers = {}
    headers["Content-Type"] = "application/x-www-form-urlencoded"
    requests.post(url, data=payload, headers=headers)


Opponent = -1
AI = 1


def evaluate(state):
    if wins(state, AI):
        score = 1
    elif wins(state, Opponent):
        score = -1
    else:
        score = 0
    return score


def wins(state, player):
    win_state = [
        [state[0][0], state[0][1], state[0][2]],
        [state[1][0], state[1][1], state[1][2]],
        [state[2][0], state[2][1], state[2][2]],
        [state[0][0], state[1][0], state[2][0]],
        [state[0][1], state[1][1], state[2][1]],
        [state[0][2], state[1][2], state[2][2]],
        [state[0][0], state[1][1], state[2][2]],
        [state[2][0], state[1][1], state[0][2]],
    ]

    if [player, player, player] in win_state:
        return True
    else:
        return False


def getEmptyCells(state):
    emptyCells = []
    for r in range(len(state)):
        for c in range(len(state)):
            if state[r][c] == 0:
                emptyCells.append([r, c])
    return emptyCells


def playMove(state, moveRow, moveCol, player):
    if state[moveRow][moveCol] == 0:
        state[moveRow][moveCol] = player
        return True
    else:
        return False


def minimax(state, depth, player):
    if player == AI:
        best = [-1, -1, float('-inf')]
    else:
        best = [-1, -1, float('inf')]

    if depth == 0 or wins(state, Opponent) or wins(state, AI):
        return [-1, -1, evaluate(state)]

    for row, col in getEmptyCells(state):
        state[row][col] = player
        score = minimax(state, depth-1, -player)
        state[row][col] = 0
        score[0], score[1] = row, col

        if player == AI:
            if score[2] > best[2]:
                best = score
        else:
            if score[2] < best[2]:
                best = score
    return best

    payload = {
        "action": "(╯°□°)╯︵ ┻━┻"
    }


def playTurn():
    depth = len(getEmptyCells(board))

    if depth == 0 or wins(board, Opponent) or wins(board, AI):
        return

    move = [0, 0]

    if depth < 9:
        move = minimax(board, depth, AI)

    position = None
    for m in moves:
        if moves[m][0] == move[0] and moves[m][1] == move[1]:
            position = m

    print(position)

    # Send post request
    payload = {
        "action": "putSymbol",
        "position": position
    }
    #haveWePlayed = True

    submit_move(payload)


def OpponentTurn(Opponent_choice, position):
    moveY, moveX = moves[position]
    if board[moveY][moveX] != 0:
        submit_move({
            "action": "(╯°□°)╯︵ ┻━┻"
        })
        resetBoard()
        return False
    else:
        playMove(board, moveY, moveX, Opponent_choice)
        return True


# currentTurn = -1

# while len(getEmptyCells(board)) > 0 and not (wins(board, Opponent) or wins(board, AI)):
#     if currentTurn == 1:
#         OpponentTurn()
#     else:
#         playTurn()
#     currentTurn *= -1
