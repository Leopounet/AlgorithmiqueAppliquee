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

from src.Utils.Graph import Graph
from src.Utils.Point import Point
from src.Utils.Vector import Vector
from src.Utils.UsefulTypes import Goal, Defender, Opponent, Shot

import math
import time

# all_problems_path = glob.glob("../examples/problems/*.json")

# for problem_path in all_problems_path:
#     problem = Problem(JSonDecoder.decode)
#     problem.decode(problem_path)
#     print("File: ", problem_path)
#     print("Problem Type: ", Problemtype.identify_problem(problem).value)
#     print("")

path = glob.glob("../examples/problems/basic_problem_2.json")[0]
problem = Problem(JSonDecoder.decode)
problem.decode(path)

graph = Graph()

field_limits = problem.get_input_from_key("field_limits")
bottom_left = Point(field_limits[0][0], field_limits[1][0])
top_right = Point(field_limits[0][1], field_limits[1][1])

goals = problem.get_input_from_key("goals")[0]
posts = goals["posts"]
direction = goals["direction"]

post1 = Point(posts[0][0], posts[0][1])
post2 = Point(posts[1][0], posts[1][1])
direction = Vector(direction[0], direction[1])
goal = Goal(post1, post2, direction)

o = Opponent(Point(0, 0))
angle = math.pi / 36
s = Shot(o, angle)

d = Defender(Point(1, 0), 0.5)

opponents = []
for opponent in problem.get_input_from_key("opponents"):
    opponents.append(Opponent(Point(opponent[0], opponent[1])))

radius = problem.get_input_from_key("robot_radius")
theta_step = problem.get_input_from_key("theta_step")
pos_step = problem.get_input_from_key("pos_step")

s = time.time()

graph.compute_graph(goal, pos_step, theta_step, opponents, bottom_left, top_right, radius)
graph_sorted = graph.copy()

graph.construct_deg(False)
graph_sorted.construct_deg(True)

print("Graph has been constructed!")

e = time.time() - s
print("Elapsed time (graph construction):", e, "seconds")

s = time.time()

for i in range(10):
    res = None
    if i <= len(opponents) - 2:
        res = graph_sorted.solve(i)
    else:
        res = graph.solve(i)
    if res != None:
        for d in res:
            print(d.pos)
        break
    if i == 9:
        print("No solution!")

e = time.time() - s
print("Elapsed time (solving):", e, "seconds")
