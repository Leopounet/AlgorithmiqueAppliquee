import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import src.Utils.Point as Point
import random

def random_point(domain):
    x = random.randint(domain[0], domain[1])
    y = random.randint(domain[0], domain[1])
    return Point.Point(x, y)

p1 = random_point((-10, 10))
p2 = random_point((-10, 10))

p3 = p1 + p2
p4 = p2 - (p3 * 0.5)
p5 = p2 / 4 + p3 - 3 * p4
p6 = p2.mid_point(p4)

print("P1 = ", p1)
print("P2 = ", p2)
print("P3 = ", p3)
print("P4 = ", p4)
print("P5 = ", p5)
print("P6 = ", p6)