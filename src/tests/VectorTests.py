import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.Utils.Vector import Vector
from src.Utils.Point import Point
import random
import math

def random_vector(domain):
    x = random.randint(domain[0], domain[1])
    y = random.randint(domain[0], domain[1])
    return Vector(x, y)

v1 = random_vector((-10, 10))
v2 = random_vector((-10, 10))

v3 = v1 + v2
s4 = v1 * v2
v5 = v1 * s4
v6 = v1 / 2 + v3 * v1 * v5
v6.normalize()
l7 = v6.norm()
v8 = Vector(1, 0)
v9 = Vector(1 / math.sqrt(2), 1 / math.sqrt(2))
a10 = v8.angle(v9)
v11 = Vector.v_from_pp(Point(1, 2), Point(5, 7))
v12 = Vector.v_from_a(math.pi / 6)

print("V1 = ", v1)
print("V2 = ", v2)
print("V3 = ", v3)
print("S4 = ", s4)
print("V5 = ", v5)
print("V6 = ", v6)
print("L7 = ", l7)
print("V8 = ", v8)
print("V9 = ", v9)
print("A10 = ", a10)
print("V11 = ", v11)
print("V12 = ", v12)