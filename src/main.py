"""
File used to do some testing for now. Might be better to have a test.py file though.
"""

import Decoders.JSonDecoder as JSonDecoder
from Problem import Problem

problem = Problem(JSonDecoder.decode)
problem.decode("../examples/problems/basic_problem_1.json")
keys = problem.get_key_list()

for key in keys:
    print(key, ": ", problem.get_input_from_key(key))
