import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import math
from src.Utils.Point import Point
from src.Utils.UsefulTypes import Opponent, Shot, Defender

class Graph:

    def __init__(self):
        self.defenders = []
        self.shots = []
        self.edges = []

    def compute_all_shots(self, opponents, step, goal):
        for opponent in opponents:
            angle = -math.pi
            while angle < math.pi:
                shot = Shot(opponent, angle)
                if goal.is_shot_valid(shot):
                    self.shots.append(shot)
                angle += step

    def compute_all_positions(self, bottom_left, top_right, step, radius, goal):
        x = bottom_left.x
        while x <= top_right.x:
            y = bottom_left.y
            while y <= top_right.y:
                defender = Defender(Point(x, y), radius)
                lst = []
                added = False

                for shot in self.shots:
                    if goal.shot_intercepted(defender, shot):
                        if not added:
                            self.defenders.append(defender)
                            added = True
                        lst.append(1)
                    else:
                        lst.append(0)

                if added:
                    self.edges.append(lst.copy())
                
                y += step
            x += step

    def compute_graph(self, goal, pos_step, theta_step, opponents, bottom_left, top_right, radius):
        self.compute_all_shots(opponents, theta_step, goal)
        self.compute_all_positions(bottom_left, top_right, pos_step, radius, goal)

    def __str__(self):
        res = ""
        for x in self.edges:
            res += str(x)
            res += "\n"
            
        return res
