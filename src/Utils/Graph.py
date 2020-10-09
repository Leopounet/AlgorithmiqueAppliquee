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
        self.dominant_value = 0

    def compute_all_shots(self, opponents, step, goal):
        for opponent in opponents:
            angle = -math.pi
            while angle < math.pi:
                shot = Shot(opponent, angle)
                if goal.is_shot_valid(shot):
                    self.shots.append(shot)
                angle += step

    def exists_collision(self, defender, shots):
        for shot in shots:
            if defender.collision(shot.opponent):
                return True
        return False

    def compute_all_positions(self, bottom_left, top_right, step, radius, goal):
        x = bottom_left.x
        while x <= top_right.x:
            y = bottom_left.y
            while y <= top_right.y:
                defender = Defender(Point(x, y), radius)
                edges = 1
                added = False

                if self.exists_collision(defender, self.shots):
                    break

                for shot in self.shots:
                    if goal.shot_intercepted(defender, shot):
                        if not added:
                            self.defenders.append(defender)
                            added = True
                        edges = (edges << 1) + 1
                    else:
                        edges = edges << 1

                if added:
                    self.edges.append(edges)
                
                y += step
            x += step

    def is_dominant_set(self, set_to_test):
        res = self.edges[set_to_test[0]]
        for i in range(0, len(set_to_test)):
            res = res | self.edges[set_to_test[i]]
            if res == self.dominant_value:
                return True
        return False

    def collision_rec(self, def_list, new_def):
        for defender in def_list:
            if self.defenders[defender].collision(self.defenders[new_def], self.defenders[0].radius):
                return True
        return False

    def solve_(self, size, defenders_list=[], index=0):
        res = None

        if index == len(self.defenders) and size != 0:
            return res

        if size == 0:
            if self.is_dominant_set(defenders_list):
                return defenders_list
            return res
        else:
            while index < len(self.defenders):
                if self.collision_rec(defenders_list, index):
                    return res
                defenders_list.append(index)
                res = self.solve_(size-1, defenders_list, index+1)
                if res != None:
                    return res
                del defenders_list[-1]
                index += 1
        return res

    def solve(self, size):
        res = self.solve_(size)
        if res != None:
            lst = []
            for defender in res:
                lst.append(self.defenders[defender])
            return lst.copy()
        return res

    def compute_graph(self, goal, pos_step, theta_step, opponents, bottom_left, top_right, radius):
        self.compute_all_shots(opponents, theta_step, goal)
        self.compute_all_positions(bottom_left, top_right, pos_step, radius, goal)
        self.dominant_value = pow(2, len(self.shots) + 1) - 1

    def __str__(self):
        res = ""
        for x in self.edges:
            res += str(bin(x))[2:]
            res += "\n"
            
        return res
