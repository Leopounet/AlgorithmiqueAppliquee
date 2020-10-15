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
import glob

import math
import time
import json
import random

# Either the path to the problem is specified or the default one is used
path = glob.glob("dumps/examples/problems/basic_problem_3.json")[0]
if len(sys.argv) >= 2:
    path = sys.argv[1]

# Create the problem
problem = Problem(JSonDecoder.decode)
problem.decode(path)

graph = Graph(problem)

graph.bubble_sort()

res = graph.find_minimum_dominating_set(10000, 100, 0.99, 10)

# Fetch the results
JSonDecoder.save_json(res)