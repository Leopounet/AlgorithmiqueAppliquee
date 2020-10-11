import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import math
from src.Utils.LinearEquation import LinearEquation
from src.Utils.Vector import Vector

class ConvexShape:

    def __init__(self, points):
        self.points = points

    # All methods created to create this method come from this answer on stackoverflow
    # # https://stackoverflow.com/questions/1119627/how-to-test-if-a-point-is-inside-of-a-convex-polygon-in-2d-integer-coordinates
    def point_in(self, point):
        prev_side = 0
        nb_vertices = len(self.points)

        for v in range(nb_vertices):
            # The mod is here because last and first vertices have to be checked (would be an overflow otherwise)
            a, b = self.points[v], self.points[(v+1) % nb_vertices]
            seg = a - b
            p = point - a
            current_side = self.side(seg, p)

            if not current_side:
                return False
            
            elif not prev_side:
                prev_side = current_side

            elif prev_side != current_side:
                return False

        return True
    
    @classmethod
    def side(self, p1, p2):
        cosine = p1.x * p2.y - p1.y * p2.x
        return 0 if not cosine else cosine / abs(cosine)

    @classmethod
    def compute_triangle(self, opponent, goal):
        points = []
        points.append(opponent.pos)
        points.append(goal.s_pos)
        points.append(goal.e_pos)
        return ConvexShape(points)

    @classmethod
    def compute_bigger_triangle(self, triangle, size):
        t_p1 = None
        t_p2 = None
        t_p3 = None

        v = Vector.v_from_pp(triangle.points[1], triangle.points[2]).normalize()
        t_p2 = triangle.points[2] + v * size
        t_p3 = triangle.points[1] - v * size

        v1 = Vector.v_from_pp(triangle.points[1], triangle.points[0])
        v2 = Vector.v_from_pp(triangle.points[2], triangle.points[0])
        v = v1 + v2
        v.normalize()

        t_p1 = triangle.points[0] + v * size

        return ConvexShape([t_p1, t_p2, t_p3])