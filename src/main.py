"""
File used to do some testing for now. Might be better to have a test.py file though.
"""

import Decoders.JSonDecoder as JSonDecoder
from Problem import Problem
from ProblemType import Problemtype
import glob

all_problems_path = glob.glob("../examples/problems/*.json")

for problem_path in all_problems_path:
    problem = Problem(JSonDecoder.decode)
    problem.decode(problem_path)
    print("File: ", problem_path)
    print("Problem Type: ", Problemtype.identifyProblem(problem).value)
    print("")