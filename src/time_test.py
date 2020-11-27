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
from src.Solvers.GreedySolver import GreedySolver
from src.Solvers.SolverArgs import SolverArgs
from src.ProblemGenerator import problem_generator
import glob

import math
import time
import json
import random

times = []

greedy_args = SolverArgs()
random_args = SolverArgs()
random_args.compare_func = lambda x, y : x > y
random_args.tries = 10000
random_args.i_m = 100
random_args.prob = 0.2
random_args.timeout = 0.5

def run(solver, graph, problem, args):
    start = time.time()

    res = solver.solve(args)

    if res == None:
        return None

    end = time.time()
    print("Solution of size " + str(len(res)) + " for " + str(len(problem["opponents"])) + " opponents found in " + str(end - start))
    return (end - start, len(res), len(problem["opponents"]))

random_def = []
greedy_def = []
ratio_def = []
random_time = []
greedy_time = []

for i in range(100) :
    problem_generator('B')

    # Create the problem
    problem = Problem(JSonDecoder.decode)
    problem.decode("dumps/B_problem.json")

    graph = Graph(problem)
    graph.compute_adjacency_matrix()

    r_solver = RandomSolver(graph)
    g_solver = GreedySolver(graph)

    print("RANDOM: ", end="")
    res1 = run(r_solver, graph, problem, random_args)
    print("GREEDY: ", end="")
    res2 = run(g_solver, graph, problem, greedy_args)

    if res1 == None or res2 == None:
        continue

    random_def.append(res1[1])
    greedy_def.append(res2[1])
    ratio_def.append(res1[1] / res2[1])
    random_time.append(res1[0])
    greedy_time.append(res2[0])
    print("----------------------------------------")

print(sum(ratio_def)/len(ratio_def))

# print("Average time measured over 300 random problems using random solver")
# print("number of opponent between 3 and 6")
# print(sum(times)/len(times))