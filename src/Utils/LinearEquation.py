import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import math
import src.Utils.Point as Point

class LinearEquation:

    def __init__(self, a=0, b=0):
        self.a = a
        self.b = b

    def __str__(self):
        return "y = " + str(self.a) + " * x + " + str(self.b) 

    def apply(self, x):
        return self.a * x + self.b

    def is_point_on(self, point):
        if self.apply(point.x) == point.y:
            return True
        return False

    def intersection(self, other):
        if self.a == other.a:
            return None

        p_1 = (other.b - self.b) / (self.a - other.a)
        return Point.Point(p_1, self.apply(p_1))

    @classmethod
    def le_from_vp(self, vector, point):
        a = vector.y / vector.x
        b = -a * point.x + point.y
        return LinearEquation(a, b)