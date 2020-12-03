"""
File used to do some testing for now. Might be better to have a test.py file though.
"""

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

import src.Decoders.JSonDecoder as JSonDecoder
from src.ProblemUtils.Problem import Problem
from src.ProblemUtils.ProblemType import ProblemType
from src.Utils.Graph import Graph
from src.Solvers.RandomSolver import RandomSolver
from src.Solvers.BruteForceSolver import BruteForceSolver
from src.Solvers.GreedySolver import GreedySolver
from src.Solvers.SolverArgs import SolverArgs
import glob

import math
import time
import json
import random

##################################################################################
################################# VARIABLES ######################################
##################################################################################

# do not touch
BRUTE = BruteForceSolver
RANDOM = RandomSolver
GREEDY = GreedySolver
UNKNOWN = 3

# args for the greedy algorithm (none)
greedy_args = SolverArgs()

# args for the random solver (please do modify)
random_args = SolverArgs()
random_args.compare_func = lambda x, y : x < y
random_args.random_tries = 10000
random_args.random_pgr = 0.4
random_args.random_i_max = 1000
random_args.random_i_best = 4000
random_args.random_prob = 0.2
random_args.random_timeout = 0.5

# args for the brute solver
brute_args = SolverArgs()
brute_args.compare_func = lambda x, y: x < y

path = None
res = None 
solver = None
args = None

##################################################################################
################################# UTILS ##########################################
##################################################################################

def str_to_solver(string):
    if string == "greedy":
        return (GREEDY, greedy_args)
    if string == "random":
        return (RANDOM, random_args)
    if string == "brute":
        return (BRUTE, brute_args)
    return (UNKNOWN, None)

def usage():
    print("Usage: python3 test.py <file> <solveur>")
    print("file: chemin vers le probleme a resoudre")
    print("solveur: le solveur a utiliser greedy|random|brute")

##################################################################################
################################# MAIN ###########################################
##################################################################################

if len(sys.argv) >= 3:
    path = sys.argv[1]
    solver, args = str_to_solver(sys.argv[2])

    if solver == UNKNOWN:
        usage()
        exit(1)
else:
    usage()
    exit(1)

# Create the problem
problem = Problem(JSonDecoder.decode)
problem.decode(path)

graph = Graph(problem)

s = solver(graph)
res = s.solve(args)

if res == None:
    print("No solution found with this solver.")
    exit(2)

# Fetch the results
JSonDecoder.save_json(res, "data.json")