import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.Utils.Point import Point
from src.Utils.Vector import Vector
from src.Utils.LinearEquation import LinearEquation
import math

class Defender:
    
    def __init__(self, pos):
        self.pos = pos

    def is_valid_pos(self, pos_step):
        return not (self.pos.x % pos_step and self.pos.y % pos_step)

class Opponent:
    
    def __init__(self, pos):
        self.pos = pos

class Shot:

    def __init__(self, opponent, angle):
        self.opponent = opponent
        self.angle = angle

    def is_valid_angle(self, theta_step):
        return not (self.angle % theta_step)

class Goal:

    def __init__(self, start_pos, end_pos, direction):
        self.s_pos = start_pos
        self.e_pos = end_pos
        self.dir = direction

    def check_position(self, player):
        mid = Point.mid_point(self.s_pos, self.e_pos)
        mid_prime = self.dir + mid

        v1 = Vector.v_from_pp(mid, player.pos)
        v2 = Vector.v_from_pp(mid, mid_prime)

        angle = v1.angle(v2)

        if -math.pi / 2 <= angle and angle <= math.pi / 2:
            return True

        return False

    def check_shot_direction(self, shot):
        return Vector.v_from_a(shot.angle) * self.dir < 0

    def check_shot_on_target(self, shot):
        i_min = min(self.s_pos.x, self.e_pos.x)
        i_max = max(self.s_pos.x, self.e_pos.x)

        tan_theta = math.tan(shot.angle)
        o_x = shot.opponent.pos.x
        o_y = shot.opponent.pos.y

        ratio = (self.e_pos.y - self.s_pos.y) / (self.e_pos.x - self.s_pos.x)

        if abs(shot.angle) == math.pi / 2:
            if i_min < o_x and o_x < i_max:
                return True
            return False

        if math.tan(shot.angle) == ratio:
            return False

        le1 = LinearEquation(tan_theta, o_y - tan_theta * o_x)
        le2 = LinearEquation(ratio, self.e_pos.y - self.e_pos.x * ratio)

        p_intersect = le1.intersection(le2)

        return i_min < p_intersect.x and p_intersect.x < i_max

        