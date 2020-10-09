"""
File used to do some testing for now. Might be better to have a test.py file though.
"""

# import Decoders.JSonDecoder as JSonDecoder
# from Problem import Problem
# from ProblemType import Problemtype
# import glob

# all_problems_path = glob.glob("../examples/problems/*.json")

# for problem_path in all_problems_path:
#     problem = Problem(JSonDecoder.decode)
#     problem.decode(problem_path)
#     print("File: ", problem_path)
#     print("Problem Type: ", Problemtype.identifyProblem(problem).value)
#     print("")

from Utils.UsefulTypes import Opponent, Goal, Shot
from Utils.Point import Point
from Utils.Vector import Vector

import math

goal = Goal(Point(3, 0), Point(4, 0), Vector(0, -1))
opponent = Opponent(Point(-2, -1))
shot = Shot(opponent, math.pi / 2)

print(goal.check_position(opponent))
print(goal.check_shot_direction(shot))
print(goal.check_shot_on_target(shot))