import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import math
from src.Utils.Point import Point

class LinearEquation:

    n_digits_round = 15

    def __init__(self, a=0, b=0):
        self.a = round(a, self.n_digits_round)
        self.b = round(b, self.n_digits_round)

    def __str__(self):
        return "y = " + str(self.a) + " * x + " + str(self.b) 

    def apply(self, x):
        return round(self.a * x + self.b, self.n_digits_round)

    def is_point_on(self, point):
        if self.apply(point.x) == point.y:
            return True
        return False

    def intersection(self, other):
        if self.a == other.a:
            return None

        p_1 = (other.b - self.b) / (self.a - other.a)
        return Point(p_1, self.apply(p_1))

    @classmethod
    def intersection_circle(self, p, angle, origin, radius):
        if abs(angle) == math.pi / 2:
            if abs(p.x - origin.x) <= radius:
                return Point(p.x, origin.y)
            return None

        if angle == 0 or abs(angle) == math.pi:
            if abs(p.pos.y - origin.y) <= radius:
                return Point(origin.x, p.pos.y)
            return None
        
        tan_angle = math.tan(angle)
        cot_angle = 1 / tan_angle
        
        le1 = LinearEquation(-cot_angle, origin.y + cot_angle * origin.x)
        le2 = LinearEquation(tan_angle, p.pos.y - tan_angle * p.pos.x)

        p_intersect = le1.intersection(le2)
        if p_intersect.distance(origin) <= radius:
            return p_intersect
        return None

    @classmethod
    def le_from_vp(self, vector, point):
        a = vector.y / vector.x
        b = -a * point.x + point.y
        return LinearEquation(a, b)