import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

import collections
from functools import cmp_to_key
matches = ["Annalee Angert, Boris Batts, Ernesto Eno, Kasandra Kroll, Tyree Takahashi, Jannet Jacquemin, Annamarie Ahern, Alayna Alberson, Nakita Newport, Elbert Ehrman", "Candice Cahill, Astrid Acheson, Rebekah Regnier, Robert Richeson, Alayna Alberson, Gaston Glotfelty, Donald Drennen, Cortez Carranco, Cora Carruth, Jesse Julio", "Shona Stanek, Donald Drennen, Orval Olsson, Chester Caldwell, Olympia Oliphant, Tyree Takahashi, Ernesto Eno, Candice Cahill, Judi Jacquez, Amos Alward", "Cortez Carranco, Sacha Stanforth, Tyree Takahashi, Fabian Fogel, Astrid Acheson, Dominic Dolce, Donald Drennen, Ernesto Eno, Josiah Jarnagin, Adina Able", "Damien Degraff, Boris Batts, Frances Fava, Alysia Alejandro, Sacha Stanforth, Ernesto Eno, Gaston Glotfelty, Alysia Auslander, Robert Richeson, Ozell Ostrem", "Donald Drennen, Irvin Insley, Lavonna Latson, Orval Olsson, Alfonso Allred, Judith Juntunen, Judi Jacquez, Douglas Delima, Ernesto Eno, Damien Degraff", "Amos Alward, Sacha Stanforth, Irvin Insley, Dominic Dolce, Alysia Auslander, Jesse Julio, Johanne Jeffress, Evelyn Eckstein, Eva Epping, Roland Room", "Fabian Fogel, Mariana Mcgruder, Sang Sirois, Dominic Dolce, Jesse Julio, Eva Epping, Nelson Noss, Ernesto Eno, Cortez Carranco, Karin Kurth", "Wilfred Weinberger, Ernesto Eno, Frances Fava, Boris Batts, Fletcher Felty, Isadora Ing, Regenia Rathburn, Alayna Alberson, Judi Jacquez, Donald Drennen", "Alysia Auslander, Chester Caldwell, Erwin Ewen, Cortez Carranco, Damien Degraff, Leslie Lubinsky, Johanne Jeffress, Denver Delaughter, Chantel Corn, Adaline Anwar", "Lorita Loeffler, Leslie Lubinsky, Boris Batts, Mariana Mcgruder, Eva Epping, Hilario Heatherly, Adina Able, Sacha Stanforth, Deidre Draves, Donald Drennen", "Jesse Julio, Felice Forte, Nelson Noss, Dorathy Detweiler, Cleveland Crofts, Pei Patague, Wilfred Weinberger, Eva Epping, Hilario Heatherly, Gaston Glotfelty", "Alanna Ayoub, Ozell Ostrem, Candice Cahill, Leslie Lubinsky, Adaline Anwar, Donald Drennen, Caitlyn Croskey, Marco Mena, Ernesto Eno, Judi Jacquez", "Felice Forte, Darren Dudley, Zada Zynda, Cora Carruth, Corine Cottrill, Amos Alward, Adina Able, Synthia Sylvestre, Boris Batts, Annette Augustine"] 

winners = ["Ernesto Eno", "Donald Drennen", "Ernesto Eno", "Ernesto Eno", "Ernesto Eno", "Ernesto Eno", "Jesse Julio", "Ernesto Eno", "Ernesto Eno", "Cortez Carranco", "Donald Drennen", "Jesse Julio", "Ernesto Eno", "Boris Batts"] 

edges = {}
freqMap = {}

for idx, match in enumerate(matches): 
  matchWinner = winners[idx]
  if matchWinner not in edges: 
    edges[matchWinner] = []
  for participant in match.split(","):
    if participant not in edges[matchWinner]:
      edges[matchWinner].append(participant) 
    
    if participant not in freqMap: 
      freqMap[participant] = 0 
    freqMap[participant]+=1

def checkPath(source, dest):
  queue = collections.deque([source])
  visited = { v: False for v in freqMap }
  visited[source] = True

  while queue: 
    node = queue.popleft()
    if node == dest: 
      return True
    
    if node in edges: 
      for neighbour in edges[node]: 
        if visited[neighbour] is False: 
          visited[neighbour] = True
          queue.appendleft(neighbour)
    
  return False

def custom_sort(item1, item2): 
  if checkPath(item1, item2): 
    return -1
  elif checkPath(item2, item1): 
    return 1 
  else: 
    if item1 in freqMap and item2 in freqMap: 
      if freqMap[item1] > freqMap[item2]: 
        return -1
      else: 
        return 1
    else: 
      return 0

@app.route('/fixedrace', methods=['POST'])
def evaluate_race():
    data = str(request.get_data())
    logging.info("data sent for evaluation {}".format(data))
    match_arr = data.split(",")
    sorted_arr = sorted(match_arr, key=cmp_to_key(custom_sort))
    return ",".join(sorted_arr) 



