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

##################################################################################
################################# VARIABLES ######################################
##################################################################################

# do not touch
BRUTE = BruteForceSolver
RANDOM = RandomSolver
GREEDY = GreedySolver
UNKNOWN = None

# args for the graph generation
optimized = True # if true some problem with valid solution may become unsolvable

# args for the greedy algorithm
greedy_args = SolverArgs()
greedy_args.greedy_random = True

# args for the random solver (please do modify)
# see more info in SolverArgs.py
random_args = SolverArgs()
random_args.compare_func = lambda x, y : x < y
random_args.random_tries = 10000
random_args.random_i_max = 1000
random_args.random_prob = 0.2
random_args.random_timeout = 0.5
random_args.random_perm = None

# args for the brute solver
brute_args = SolverArgs()
brute_args.compare_func = lambda x, y: x < y

# path to the problem file
path = None

# the result of the solver
res = None 

# the solver to use
solver = None

# the arguments of the solver to use
args = None

##################################################################################
################################# UTILS ##########################################
##################################################################################

# decides which solver to use wrt the given arguments
def str_to_solver(string):
    if string == "greedy":
        return (GREEDY, greedy_args)
    if string == "random":
        return (RANDOM, random_args)
    if string == "brute":
        return (BRUTE, brute_args)
    return (UNKNOWN, None)

def usage():
    print("Usage: python3 main.py <file> <solveur>")
    print("file: chemin vers le probleme a resoudre")
    print("solveur: le solveur a utiliser greedy|random|brute")

##################################################################################
################################# MAIN ###########################################
##################################################################################

# reads the given arguments (no safety check)
if len(sys.argv) >= 3:
    path = sys.argv[1]
    solver, args = str_to_solver(sys.argv[2])

    if solver == UNKNOWN:
        usage()
        exit(1)
else:
    usage()
    exit(1)

# Creates the problem
problem = Problem(JSonDecoder.decode)
problem.decode(path)

# creates the graph
graph = Graph(problem)

# creates the solver
s = solver(graph)

# solves the graph
res = s.solve(args)

# if no results are found, stop here
if res == None:
    print("No solution found with this solver.")
    exit(2)

# Fetch the results
JSonDecoder.save_json(res, "data.json")