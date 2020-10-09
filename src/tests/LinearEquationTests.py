import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import src.Utils.Vector as Vector
import src.Utils.Point as Point
import src.Utils.LinearEquation as LinearEquation

le1 = LinearEquation.LinearEquation(1, 0)
le2 = LinearEquation.LinearEquation(-4, -1)

p3 = Point.Point(4, le2.apply(4))
p4 = Point.Point(4, 4)
p5 = le1.intersection(le2)
le6 = LinearEquation.LinearEquation.le_from_vp(Vector.Vector(4, 7), Point.Point(5, 4))

print("LE1 = ", le1)
print("LE2 = ", le2)
print("P3 = ", p3)
print("P4 = ", p4)
print("P3 on LE1 ->", le1.is_point_on(p3))
print("P4 on LE1 ->", le1.is_point_on(p4))
print("P3 on LE2 ->", le2.is_point_on(p3))
print("P4 on LE2 ->", le2.is_point_on(p4))
print("P5 = ", p5)
print("LE6 = ", le6)