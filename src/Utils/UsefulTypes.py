import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.Utils.Point import Point
from src.Utils.Vector import Vector
from src.Utils.LinearEquation import LinearEquation
import math

"""
This module regroups a lot of class definition that are basic encapsulations
of other concepts. Found here so far : 

- Player (Abstract definition of Defender and Opponent) 
- Defender 
- Opponent 
- Shot 
- Goal
"""

class Player:
    
    """
    This class represents any player on the field. It is abstract (eventhough it doesn't 
    mean much in Python) and therefore has no reason to be instantiated.
    """

    def __init__(self, pos, radius):
        """
        Constructs a new 'Player' object. 

        :param pos: The initial position of the player. 

        :param radius: The radius of the player. 

        :return: returns nothing. 
        """
        self.pos = pos
        self.radius = radius

    def __str__(self):
        """
        Allows the use of print(p) where p is a 'Player' object. 

        :return: The corresponding string.
        """
        res = "Pos: " + str(self.pos) + " Radius: " + str(self.radius)
        return res

    def collision(self, player, distance=None):
        """
        Checks if this player and the given one collide. It can also be used
        to check if they are a certain distance apart with the optional parameter. 

        :param player: The other player to check collisions with.

        :param distance (opt): The distance to have between the two robots to not have \
        a collision. 

        :return: True if there is a collision, False otherwise.
        """
        if distance == None:
            distance = 2 * self.radius
        return self.pos.distance(player.pos) < distance

    def in_zone(self, bottom_left, top_right):
        """
        Checks if this player is in a rectangular zone defined by its bottom left point 
        and top right point. 

        :param bottom_left: The bottom left point of the zone. 

        :param top_right: The top right point of the zone. 

        :return: True if the player is in the zone, False otherwise.
        """
        return (bottom_left.x <= self.pos.x and self.pos.x <= bottom_left.x and
                top_right.y <= self.pos.y and self.pos.y <= top_right.y)


class Defender(Player):

    """
    This class represents a defender on the field. This is basically renaming what a player is
    which is about renaming what a point is. Although, in this case a radius needs to be specified.
    """
    
    def __init__(self, pos, radius):
        """
        Constructs a new 'Defender' object. 

        :param pos: The initial position of the defender. 

        :param radius: The radius of the defender. 

        :return: returns nothing.
        """
        super().__init__(pos, radius)

    def is_valid_pos(self, pos_step):
        """
        Check if the position of this player is valid regarding the given
        step between two positions. 

        :param pos_step: The distance between two positions next to each other \
        in all four cardinal directions. 

        :return: True if the position is valid, False otherwise.
        """
        return not (self.pos.x % pos_step or self.pos.y % pos_step)

class Opponent(Player):

    """
    This class represents an opponent on the field. This is basically renaming what a player is
    which is about renaming what a point is. Although, in this case a radius doesn't need to be specified.
    """
    
    def __init__(self, pos, radius=0):
        """
        Constructs a new 'Opponent' object. 

        :param pos: The initial position of the opponent. 

        :param radius (opt): The radius of the opponent. 

        :return: returns nothing.
        """
        super().__init__(pos, radius)

class Shot:

    """
    This class represents what a shot is, which is an opponent and an angle.
    """

    def __init__(self, opponent, angle):
        """
        Constructs a new 'Shot' object. 

        :param opponent: The opponent that is taking the shot. 

        :param angle: The angle at which the opponent is shooting, with regard to the
        origin of the field (in the center). 

        :return: returns nothing.
        """
        self.opponent = opponent
        self.angle = angle

    def __str__(self):
        """
        Allows the use of print(s) where s is a 'Shot' object. 

        :return: The corresponding string.
        """
        res = "Opponent: " + str(self.opponent) + " Angle: " + str(self.angle)
        return res

    def is_valid_angle(self, theta_step):
        """
        Check if the angle of this shot is valid regarding the given
        step between two angles. 

        :param theta_step: The angle between two consecutive angles. 

        :return: True if the angle is valid, False otherwise.
        """
        return not (self.angle % theta_step)

class Goal:

    """
    This class represents a Goal. A goal is a defined by two points (to form a segment)
    and a vector that defines the orientation of the goal (where you can score from).
    """

    def __init__(self, start_pos, end_pos, direction):
        """
        Creates a new 'Goal' object. 

        :param start_pos: The starting point of the segment.

        :param end_pos: The ending point of the segment. 

        :param direction: The orientation of the goal. 

        :return: returns nothing.
        """
        self.s_pos = start_pos
        self.e_pos = end_pos
        self.dir = direction

    def __str__(self):
        """
        Allows the use of print(g) where g is a 'Goal' object. 

        :return: The corresponding string.
        """
        res = "Pos 1: " + str(self.s_pos) + " Pos 2: " + str(self.e_pos) + " Dir: " + str(self.dir)
        return res

    def is_in_interval(self, low, high, value):
        """
        Check if the given value in in the interval [low ; high]. 

        Useful method to make the code easier to read. It is not specific
        to this class and could be used in different classes but for now
        it will remain here. 

        :param low: Low bound of the interval. 

        :param high: High bound of the interval. 

        :param value: The value to check. 

        :return: True if value is in the interval, false otherwise.
        """
        return low <= value and value <= high

    def check_position(self, player):
        """
        Checks if the given player is correctly placed with regard to the orientation 
        of the goal. If the player is 'behind' the goal, then it is not correctly placed,
        if it is in front of the goal, then it is correctly placed.

        This is done by checking the angle formed between the direction vector of the goal and
        the vector going from the center of the goal to the player. This angle must be in
        [-pi/2 ; pi/2] if the player is correctly placed (draw it yourself or check out paper
        about this problem for more information). 

        :param player: The player to consider. 

        :return: True if the player is correctly placed, False otherwise.
        """

        # Mid point of the segment defining the goal
        mid = Point.mid_point(self.s_pos, self.e_pos)

        # Transposition of this point by the direction vector of the goal
        # to get the direction vector with its origin in the center of the goal
        mid_prime = self.dir + mid

        # Creating both needed vectors
        v1 = Vector.v_from_pp(mid, player.pos)
        v2 = Vector.v_from_pp(mid, mid_prime)

        # Getting the angle and checking if it is a valid one
        angle = v1.angle(v2)

        return self.is_in_interval(-math.pi / 2, math.pi / 2, angle)

    def check_shot_direction(self, shot):
        """
        Checks if the given shot goes towards this goal. To do so,
        simply consider that whether the shot is valid or not, for it to be
        going towards the goal, it needs to go towards the half-plane define by the goal's segment
        (well, goal's line in this case, it is considered infinite here). For more information,
        check our paper on this subject or try drawing it yourself. 

        To know if this is the case, the scalar product of the vector of the shot and the 
        direction of the goal is checked. There are supposed to be going in opposite direction,
        therefore the scalar product must be negative. 

        :param shot: The shot to consider. 

        :return: True if the shot goes towards the goal (if it was infinite), False otherwise.
        """
        return Vector.v_from_a(shot.angle) * self.dir < 0

    def check_shot_on_target(self, shot):
        """
        Checks if the shot (abstracted to an infinite line) intersects the goal's
        segment. 

        To do so,find the intersection point between the shot corresponding linear equation
        and the goal's segment corresponding linear equation. Then check if this point is
        in the goal's segment. 
        
        :param shot: The shot to consider. 

        :return: True if the shot intersects the goal's segment, False otherwise.
        """
        # Defining a few variables to ease the reading
        # Here we define the x and y interval of the goal's segment
        x_min = min(self.s_pos.x, self.e_pos.x)
        x_max = max(self.s_pos.x, self.e_pos.x)

        y_min = min(self.s_pos.y, self.e_pos.y)
        y_max = max(self.s_pos.y, self.e_pos.y)

        # Shortening variables names
        o_x = shot.opponent.pos.x
        o_y = shot.opponent.pos.y

        # If the angle = pi / 2 or - pi / 2, then tan(angle) is undefined
        # In these cases, the shot is vertical, therefore it is valid
        # iff the x coordinate of the opponent is in the goal's x interval
        if abs(shot.angle) == math.pi / 2:
            return self.is_in_interval(x_min, x_max, o_x)

        # If the angle = 0, pi or -pi, then tan(angle) is 0 which can lead to 
        # undefined intersection points (if the goal is vertical for example)
        # although there is an intersection point
        # 
        # In these cases, the shot is horizontal, therefore it is valid
        # iff the y coordinate of the opponent is in the goal's y interval
        if abs(shot.angle) == math.pi or shot.angle == 0:
            return self.is_in_interval(y_min, y_max, o_y)

        # Using tan the least amount of time possible, for this is a slow function
        tan_theta = math.tan(shot.angle)

        # Define the LE of the shot
        le1 = LinearEquation(tan_theta, o_y - tan_theta * o_x)
        le2 = None

        # If the goal is vertical, finding the intersection point
        # is not possible using the normal way
        #
        # That being said, unless the LE of the shot is vertical too (which it 
        # isn't as it is checked before hand) there has to be an intersection point
        # This intersection must happen when at the x coodinate of the goal's segment
        # therefore, it is possible to compute the y coordinate of the intersection by
        # computing the application of the shot's LE on this ex coordinate
        #
        # Then, the resulting y is valid iff it is in the goal's segment interval
        if self.e_pos.x - self.s_pos.x == 0:
            y = le1.apply(self.e_pos.x)
            return self.is_in_interval(y_min, y_max, y)

        # The normal way of solving the intersection of these two LEs
        else:

            # Shortening variables by computing the coefficient of the goal's LE
            ratio = (self.e_pos.y - self.s_pos.y) / (self.e_pos.x - self.s_pos.x)

            # If the lines are parallels (have the same coefficient) return False
            if math.tan(shot.angle) == ratio:
                return False

            # Defining the goal's LE
            le2 = LinearEquation(ratio, self.e_pos.y - self.e_pos.x * ratio)

        # Finding the intersection point of the two LEs
        # If there isn't one, return False (but there should be one
        # given all the asserts we do before hand, this is just for completion sake)
        p_intersect = le1.intersection(le2)
        if p_intersect == None:
            return False

        # If the intersection point's abscissa is in the goal's x interval, then it is
        # a valid abstracted shot going 
        return self.is_in_interval(x_min, x_max, p_intersect.x)

    def is_shot_valid(self, shot):
        """
        Checks if a shot is valid (going in the goal) or not. To do so, three
        things are checked : 

        1 -> Is the player ABLE to shoot in the goal, namely is it in front of the goal and not behind? 

        2 -> Is the shot going towards the half plane defined by the goal? 
        
        3 -> Is the linear equation defined by the shot intersecting the goal's segment? 

        (3) is obviously required. (2) is required because if it isn't checked, the player could shoot 
        away from the goal and it would be considered valid since in (3) we consider a linear equation 
        and not a half-line. (1) is required because otherwise it would be true even if the player 
        shoots from behind the goal. 

        :param shot: The shot to check. 

        :return: True if the shot is valid, False otherwise.
        """
        a = self.check_position(shot.opponent)
        b = self.check_shot_direction(shot)
        c = self.check_shot_on_target(shot)
        return a and b and c

    def shot_intercepted(self, defender, shot):
        """
        Checks if the given shot is intercepted by the given player with regard to this goal. 

        To do so, we check if the circle defined by the player and its radius intersects the
        shot. Then, it is checked if the intersection is between the opponent and the goal. 
        There are plenty of special cases, find more information below. 

        :param defender: The defender that should intercept the shot. 

        :param shot: The shot to intercept. 
            
        :return: True if the shot is intercepted, False otherwise.
        """

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

        # If the goal is vertical, solving the intersection won't work
        # it is then done "by hand"
        if self.e_pos.x - self.s_pos.x == 0:
            # If the goal and the shot are vertical, return False
            if abs(shot.angle) == math.pi / 2:
                return False
            
            # If the angle = 0, pi or -pi, then tan(angle) is 0 which can lead to
            # undefined behaviors (namely if the goal is vertical)
            # 
            # In these cases, the shot is horizontal, therefore it is valid
            # iff the x coordinate of the intersection point of the defender and the shot
            # is between the goal and the opponent x coordinates
            if abs(shot.angle) == math.pi or shot.angle == 0:
                q = Point(self.e_pos.x, o_y)
                return self.is_in_interval(min(q.x, o_x), max(q.x, o_x), p.x)

            le2 = LinearEquation(tan_theta, o_y - tan_theta * o_x)
            q = Point(self.e_pos.x, le2.apply(self.e_pos.x)) 
            return self.is_in_interval(min(q.x, o_x), max(q.x, o_x), p.x)     

        # If the goal is not vertical, it is now possible to define the coefficient
        # of the goal's LE
        ratio = (self.e_pos.y - self.s_pos.y) / (self.e_pos.x - self.s_pos.x)

        # If the shot is parallel to the goal (same coefficient) it doesn't
        # matter if it is intercepted (this method should only be used
        # with valid shot in the first place, this is just for completion sake)
        if math.tan(shot.angle) == ratio:
            return False

        # LE of the goal
        le1 = LinearEquation(ratio, self.e_pos.y - self.e_pos.x * ratio)

        # If the angle = pi / 2 or - pi / 2, then tan(angle) is undefined
        # In these cases, the shot is vertical, therefore it is valid
        # iff the y coordinate of the intersection point of the defender and the shot
        # is between the goal and the opponent
        if abs(shot.angle) == math.pi / 2:
            q = Point(o_x, le1.apply(o_x))
            return self.is_in_interval(min(q.y, o_y), max(q.y, o_y), p.y)
        
        # If the angle = 0, pi or -pi, then tan(angle) is 0 which can lead to
        # undefined behaviors (namely if the goal is vertical)
        # 
        # In these cases, the shot is horizontal, therefore it is valid
        # iff the x coordinate of the intersection point of the defender and the shot
        # is between the goal and the opponent y coordinates
        if abs(shot.angle) == math.pi or shot.angle == 0:
            q = Point(le1.reverse(o_y), o_y)
            return self.is_in_interval(min(q.x, o_x), max(q.x, o_x), p.x)
        
        # LE of the shot
        le2 = LinearEquation(tan_theta, o_y - tan_theta * o_x)

        # Find the intersection of the two lines and check if the defender
        # is between this point and the opponent
        q = le1.intersection(le2)

        return self.is_in_interval(min(q.x, o_x), max(q.x, o_x), p.x)

        

        