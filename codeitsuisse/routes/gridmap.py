import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/stock-hunter', methods=['POST'])
def evaluate_grid():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    result = []
    for grid in data:
        result.append(solve(grid["entryPoint"], grid["targetPoint"],
                      grid["gridDepth"], grid["gridKey"],
                      grid["horizontalStepper"], grid["verticalStepper"]))
    logging.info("My result :{}".format(result))
    return json.dumps(result)

def minimumPathSum(grid):
    m = len(grid)
    n = len(grid[0])
    grid[0][0] = 0
    for i in range(m):
        for j in range(n):
            if i > 0 and j > 0:
                grid[i][j] += min(grid[i - 1][j], grid[i][j - 1])
            elif j != 0:
                grid[i][j] += grid[i][j - 1]
            elif i != 0:
                grid[i][j] += grid[i - 1][j]
    return grid[m - 1][n - 1]

 
def solve(entry, target, gridDepth, gridKey, horizontalStep, verticalStep):
    entryPoint = (entry["first"],entry["second"])
    targetPoint = (target["first"],target["second"])

    rows = targetPoint[0] - entryPoint[0] + 1
    cols = targetPoint[1] - entryPoint[1] + 1

    grid = [[0 for _ in range(cols)] for i in range(rows)]
    gridCpy = [[0 for _ in range(cols)] for i in range(rows)]
    for r in range(rows):
        for c in range(cols):
            if (r,c) == entryPoint or (r,c) == targetPoint:
                grid[r][c] = (0 + gridDepth) % gridKey
            elif c == 0:
                grid[r][c] = (r * verticalStep + gridDepth) % gridKey
            elif r == 0:
                grid[r][c] = (c * horizontalStep + gridDepth) % gridKey
            else:
                grid[r][c] = (grid[r][c-1] * grid[r-1][c] + gridDepth) % gridKey

    riskCost = ['L','M','S']
    riskCostRev = {
        'L' : 3,
        'M' : 2,
        'S' : 1
    }
    for r in range(rows):
        for c in range(cols):
            grid[r][c] = riskCost[grid[r][c] % 3]
            gridCpy[r][c] = riskCostRev[grid[r][c]]
            
    return {
        "gridMap" : grid,
        "minimumCost" : minimumPathSum(gridCpy)
    }



