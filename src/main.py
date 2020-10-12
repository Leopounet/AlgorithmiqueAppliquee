"""
File used to do some testing for now. Might be better to have a test.py file though.
"""

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

import src.Decoders.JSonDecoder as JSonDecoder
from src.Problem import Problem
from src.ProblemType import ProblemType
import glob

import math
import time
import json

# Either the path to the problem is specified or the default one is used
path = glob.glob("dumps/examples/problems/basic_problem_3.json")[0]
if len(sys.argv) >= 2:
    path = sys.argv[1]

# Create the problem
problem = Problem(JSonDecoder.decode)
problem.decode(path)

print(problem)

# Fetch the results
res = []
JSonDecoder.save_json(res)