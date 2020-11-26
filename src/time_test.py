"""
File used to do some testing for now. Might be better to have a test.py file though.
"""

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

import src.Decoders.JSonDecoder as JSonDecoder
from src.Problem import Problem
from src.ProblemType import ProblemType
from src.Utils.Graph import Graph
from src.Solvers.RandomSolver import RandomSolver
from src.Solvers.BruteForceSolver import BruteForceSolver
from src.ProblemGenerator import problem_generator
import glob

import math
import time
import json
import random

times = []

for i in range(300) :
    problem_generator('B')

    # Either the path to the problem is specified or the default one is used
    path = glob.glob("dumps/B_problem.json")[0]
    if len(sys.argv) >= 2:
        path = sys.argv[1]

    # Create the problem
    problem = Problem(JSonDecoder.decode)
    problem.decode(path)

    start = time.time()

    graph = Graph(problem)
    graph.compute_adjacency_matrix()

    r_solver = RandomSolver(graph)
    # bf_solver = BruteForceSolver(graph)

    res = r_solver.solve(10000, 100, 0.2, 0.5, compare_func=lambda x, y : x > y)
    # res = bf_solver.solve(compare_func=lambda x, y: x > y)

    # print("here ?")

    # # Fetch the results
    JSonDecoder.save_json(res)

    end = time.time()
    times.append(end-start)
    print(i+1)
    print(sum(times)/len(times))

print("Average time measured over 300 random problems")
print("number of opponent between 3 and 6")
print(sum(times)/len(times))