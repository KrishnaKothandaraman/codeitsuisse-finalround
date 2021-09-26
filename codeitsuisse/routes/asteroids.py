import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/asteroid', methods=['POST'])
def evaluate_asteroid():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    inputValue = data.get("test_cases")
    result = []
    for inputs in inputValue:
      result.append(solve(inputs))
    logging.info("My result :{}".format(result))
    return json.dumps(result)


def solve(input_data):
  counts = {} 
  groupStarts = {}

  def getMultiplier(count): 
    if count <= 6: 
      return 1
    elif 10 > count >= 7: 
      return 1.5 
    else: 
      return 2

  groups = []

  currentCount = 1
  prevChar = input_data[0]
  currentGroupStart = 0 

  for i in range(1, len(input_data)): 
    if prevChar == input_data[i]: 
      currentCount+=1
    else: 
      counts[len(groups)] = currentCount
      groupStarts[len(groups)] = currentGroupStart
      groups.append(prevChar)
      prevChar = input_data[i]
      currentCount = 1
      currentGroupStart = i

  counts[len(groups)] = currentCount
  groupStarts[len(groups)] = currentGroupStart
  groups.append(prevChar)

  # print(groupStarts)

  ans = [1, 0]
  trav = 0
  groupStart = 0
  groupMiddle = 0

  while trav < len(groups): 

    groupStart = groupStarts[trav]
    groupMiddle = groupStart + counts[trav]//2

    # print(f'Current Group: {trav}')
    # print(f'Current Group Start: {groupStart}')
    # print(f'Current Group Middle: {groupMiddle}')


    hit = counts[trav] * getMultiplier(counts[trav])
    leftPointer = trav-1 
    rightPointer = trav+1

    while leftPointer >= 0 and rightPointer <= len(groups)-1 and groups[leftPointer] == groups[rightPointer]: 
      # print(f'   Left Pointer: {leftPointer}')
      # print(f'   Right Pointer: {rightPointer}')
      numberOfAsteroids = counts[leftPointer]+counts[rightPointer]
      hit += (numberOfAsteroids) * getMultiplier(numberOfAsteroids)
      leftPointer-=1 
      rightPointer+=1

    if hit > ans[0]:
      ans[0] = hit
      ans[1] = groupMiddle
      # print(f"Updated Answer to {ans}")

    # print("=================")
    trav+=1

  return {
    "input" : input_data,
    "score" : ans[0],
    "origin" : ans[1]
  }
  
