import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.Utils.Vector import Vector
from src.Utils.Point import Point
from src.Utils.LinearEquation import LinearEquation

le1 = LinearEquation(1, 0)
le2 = LinearEquation(-4, -1)

p3 = Point(4, le2.apply(4))
p4 = Point(4, 4)
p5 = le1.intersection(le2)

print("LE1 = ", le1)
print("LE2 = ", le2)
print("P3 = ", p3)
print("P4 = ", p4)
print("P3 on LE1 ->", le1.is_point_on(p3))
print("P4 on LE1 ->", le1.is_point_on(p4))
print("P3 on LE2 ->", le2.is_point_on(p3))
print("P4 on LE2 ->", le2.is_point_on(p4))
print("P5 = ", p5)