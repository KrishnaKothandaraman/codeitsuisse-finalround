import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)


@app.route('/parasite', methods=['POST'])
def evaluate_parasite():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    result = []
    for room in data:
        result.append(solve(room["room"], room["grid"],
                      room["interestedIndividuals"]))
    logging.info("My result :{}".format(result))
    return json.dumps(result)


def isValid(i, j, grid):
    return 0 <= i < len(grid) and 0 <= j < len(grid[0])


def getAdjList(i, j, grid):

    steps = [
        (1, 0),
        (0, 1),
        (-1, 0),
        (0, -1)
    ]

    returnAns = []

    for step in steps:
        newX = i + step[0]
        newY = j + step[1]
        if isValid(newX, newY, grid) and grid[newX][newY] == 1:
            returnAns.append({(newX, newY): 1})
    return returnAns


def getAdjListB(i, j, grid):

    steps = [
        (1, 0),
        (0, 1),
        (-1, 0),
        (0, -1),
        (-1, -1),
        (1, -1),
        (-1, 1),
        (1, 1)
    ]

    returnAns = []

    for step in steps:
        newX = i + step[0]
        newY = j + step[1]
        if isValid(newX, newY, grid) and grid[newX][newY] == 1:
            returnAns.append({(newX, newY): 1})
    return returnAns


def getAdjListC(i, j, grid):

    steps = [
        (1, 0),
        (0, 1),
        (-1, 0),
        (0, -1),
    ]

    returnAns = []
    for step in steps:
        newX = i + step[0]
        newY = j + step[1]
        if isValid(newX, newY, grid):
            if grid[newX][newY] == 0 or grid[newX][newY] == 2:
                returnAns.append({(newX, newY): 1})
            else:
                returnAns.append({(newX, newY): 0})

    return returnAns


def helper(graph, parasiteLocation, interestedIndividuals, mapType):
    graphToIntMap = {}
    idx = 0
    for key in graph:
        graphToIntMap[key] = idx
        idx += 1

    dist = [float('inf') for key in graph]
    # for key in graph:
    #     print(f'{key}:{graph[key]}')

    dist[graphToIntMap[parasiteLocation]] = 0
    node_length = {parasiteLocation: 0}

    while node_length:
        source_node = min(node_length, key=lambda k: node_length[k])
        del node_length[source_node]

        for neighbours in graph[source_node]:
            for key, value in neighbours.items():
                if dist[graphToIntMap[key]] > dist[graphToIntMap[source_node]] + value:
                    dist[graphToIntMap[key]
                         ] = dist[graphToIntMap[source_node]] + value
                    if key in interestedIndividuals and mapType == 'A':
                        interestedIndividuals[key] = dist[graphToIntMap[key]]
                    node_length[key] = dist[graphToIntMap[key]]

    ans = max(dist)

    ans = ans if ans != float('inf') else -1

    return [ans, interestedIndividuals]


def helperB(graph, parasiteLocation, grid):
    graphToIntMap = {}
    idx = 0
    for key in graph:
        graphToIntMap[key] = idx
        idx += 1

    dist = [float('inf') for key in graph]
    # for key in graph:
    #     print(f'{key}:{graph[key]}')

    dist[graphToIntMap[parasiteLocation]] = 0
    node_length = {parasiteLocation: 0}
    maxEnergy = 0
    while node_length:
        source_node = min(node_length, key=lambda k: node_length[k])
        del node_length[source_node]

        for neighbours in graph[source_node]:
            for key, value in neighbours.items():
                if dist[graphToIntMap[key]] > dist[graphToIntMap[source_node]] + value:
                    dist[graphToIntMap[key]
                         ] = dist[graphToIntMap[source_node]] + value
                    if grid[key[0]][key[1]] == 1:
                        maxEnergy = max(maxEnergy, dist[graphToIntMap[key]])
                    # if key in interestedIndividuals:
                    #     interestedIndividuals[key] = dist[graphToIntMap[key]]
                    node_length[key] = dist[graphToIntMap[key]]

    return maxEnergy


def process(interestedIndividuals):
    returnAns = {}
    for location in interestedIndividuals:
        l1, l2 = location.split(',')
        returnAns[int(l1), int(l2)] = -1
    return returnAns


def convertToString(interestedIndividuals):

    p1 = {}
    for key in interestedIndividuals:
        strKey = f'{key[0]},{key[1]}'
        p1[strKey] = interestedIndividuals[key]

    return p1


def solve(roomNumber, grid, interestedIndividuals):
    rows = len(grid)
    cols = len(grid[0])
    graph = {}
    graphB = {}
    graphC = {}
    interestedIndividuals = process(interestedIndividuals)
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == 3 or grid[i][j] == 1:
                if grid[i][j] == 3:
                    parasiteLocation = (i, j)
                graph[(i, j)] = getAdjList(i, j, grid)
                graphB[(i, j)] = getAdjListB(i, j, grid)
            graphC[(i, j)] = getAdjListC(i, j, grid)

    p2 = helper(graph, parasiteLocation, interestedIndividuals, 'A')

    p3 = helper(graphB, parasiteLocation, interestedIndividuals, 'B')

    p4 = helperB(graphC, parasiteLocation, grid)

    p1 = convertToString(p2[1])

    # print(f'p1:{p1}')
    # print(f'p2:{p2[0]}')
    # print(f'p3:{p3[0]}')
    # print(f'p4:{p4}')

    return {
        "room": roomNumber,
        "p1": p1,
        "p2": p2[0],
        "p3": p3[0],
        "p4": p4
    }
