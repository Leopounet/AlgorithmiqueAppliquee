import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.Utils.UsefulTypes import Opponent, Goal, Shot
from src.Utils.Point import Point
from src.Utils.Vector import Vector

import math

goal = Goal(Point(3, 0), Point(4, 0), Vector(0, -1))
opponent = Opponent(Point(-2, -1))
shot = Shot(opponent, math.pi / 2)

print(goal.check_position(opponent))
print(goal.check_shot_direction(shot))
print(goal.check_shot_on_target(shot))