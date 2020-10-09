import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.Utils.Point import Point
from src.Utils.Vector import Vector
from src.Utils.LinearEquation import LinearEquation
import math

class Player:

    def __init__(self, pos, radius):
        self.pos = pos
        self.radius = radius

    def collision(self, player, distance=None):
        if distance == None:
            distance = 2 * self.radius
        return self.pos.distance(player.pos) < distance

    def in_zone(self, top_left, bottom_right):
        return (top_left.x <= self.pos.x and self.pos.x <= bottom_right.x and
                bottom_right.y >= self.pos.y and self.pos.y >= bottom_right.y)


class Defender(Player):
    
    def __init__(self, pos, radius):
        super().__init__(pos, radius)

    def is_valid_pos(self, pos_step):
        return not (self.pos.x % pos_step and self.pos.y % pos_step)

class Opponent(Player):
    
    def __init__(self, pos, radius=0):
        super().__init__(pos, radius)

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
        x_min = min(self.s_pos.x, self.e_pos.x)
        x_max = max(self.s_pos.x, self.e_pos.x)

        y_min = min(self.s_pos.y, self.e_pos.y)
        y_max = max(self.s_pos.y, self.e_pos.y)

        tan_theta = math.tan(shot.angle)
        o_x = shot.opponent.pos.x
        o_y = shot.opponent.pos.y

        if abs(shot.angle) == math.pi / 2:
            if x_min < o_x and o_x < x_max:
                return True
            return False

        if abs(shot.angle) == math.pi or shot.angle == 0:
            if y_min < o_y and o_y < y_max:
                return True
            return False

        le1 = LinearEquation(tan_theta, o_y - tan_theta * o_x)
        le2 = None

        if self.e_pos.x - self.s_pos.x == 0:
            y = le1.apply(self.e_pos.x)
            return y_min < y and y < y_max
        else:
            ratio = (self.e_pos.y - self.s_pos.y) / (self.e_pos.x - self.s_pos.x)
            if math.tan(shot.angle) == ratio:
                return False
            le2 = LinearEquation(ratio, self.e_pos.y - self.e_pos.x * ratio)

        p_intersect = le1.intersection(le2)
        if p_intersect == None:
            return False

        return x_min < p_intersect.x and p_intersect.x < x_max

    def is_shot_valid(self, shot):
        return (self.check_position(shot.opponent) and
                self.check_shot_direction(shot) and
                self.check_shot_on_target(shot))

    def shot_intercepted(self, defender, shot):

        tan_theta = math.tan(shot.angle)
        o_x = shot.opponent.pos.x
        o_y = shot.opponent.pos.y

        le1 = None
        le2 = None

        p = None
        q = None

        p = LinearEquation.intersection_circle(shot.opponent, shot.angle, defender.pos, defender.radius)

        if p == None:
            return False

        if abs(shot.angle) == math.pi / 2:
            q = Point(o_x, self.e_pos.y)
        else:
            if abs(shot.angle) == math.pi or shot.angle == 0:
                q = Point(self.e_pos.x, o_y)
            else:
                le1 = LinearEquation(tan_theta, o_y - tan_theta * o_x)

                if self.e_pos.x - self.s_pos.x == 0:
                    y = le1.apply(self.e_pos.x)
                    q = Point(self.e_pos.x, y)                    
                else:
                    ratio = (self.e_pos.y - self.s_pos.y) / (self.e_pos.x - self.s_pos.x)

                    if math.tan(shot.angle) == ratio:
                        return False

                    le2 = LinearEquation(ratio, self.e_pos.y - self.e_pos.x * ratio)

                    q = le1.intersection(le2)

        if min(q.x, o_x) <= p.x and p.x <= max(q.x, o_x):
            return True
        return False

        

        