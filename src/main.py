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
import threading

# all_problems_path = glob.glob("../examples/problems/*.json")

# for problem_path in all_problems_path:
#     problem = Problem(JSonDecoder.decode)
#     problem.decode(problem_path)
#     print("File: ", problem_path)
#     print("Problem Type: ", Problemtype.identify_problem(problem).value)
#     print("")

path = glob.glob("../examples/problems/basic_problem_4.json")[0]
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

graph.compute_graph(goal, pos_step, theta_step, opponents, bottom_left, top_right, radius)
graph_sorted = graph.copy()

graph.construct_deg(False)
graph_sorted.construct_deg(True)

print("Graph has be constructed!")
res = None
step = 1

class myThread (threading.Thread):

    def __init__(self, threadID, name, graph, step, sorted_arr):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.step = step
        self.graph = graph
        self.sorted = sorted_arr

        self.res = None

    def run(self):
        self.res = graph.solve(step, self)

while res == None and step <= 10:
    thread1 = myThread(1, "Thread-1", graph, step, True)
    thread2 = myThread(2, "Thread-2", graph_sorted, step, False)

    thread1.graph.thread_end = False
    thread2.graph.thread_end = False
    res = None

    thread1.start()
    thread2.start()

    thread1.graph.thread_end = True
    thread2.graph.thread_end = True

    thread1.join()
    thread2.join()

    if thread1.res == None and thread2.res == None:
        res = None
    
    elif thread1.res != None:
        res = thread1.res
    
    elif thread2.res != None:
        res = thread2.res

    if res != None:
        for d in res:
            print(d.pos)
    else:
        print("None")
    step += 1
# # print(graph)
