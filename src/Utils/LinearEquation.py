import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import math
from src.Utils.Point import Point

"""
This module is used to simulate linear equation (ax + b).
"""

class LinearEquation:

    """
    This class simulates a linear a equation of the form ax + b. It then gives access
    to plenty of useful method on linear equations.

    :member n_digits_round: The max number of digits after the decimal point (then
    rounded if exceeded). Useful because of approximation problems linked to Python and
    computers in general.
    """

    n_digits_round = 15

    def __init__(self, a=0, b=0):
        """
        Constructs a new "LinearEquation" object.

        :param a: The coefficient of the LE.
        :param b: The added constant of the LE.
        :return: returns nothing.
        """
        self.a = round(a, self.n_digits_round)
        self.b = round(b, self.n_digits_round)

    def __str__(self):
        """
        Method to be able to use print(linear_eq).

        :return: Returns the corresponding string.
        """
        return "y = " + str(self.a) + " * x + " + str(self.b) 

    def apply(self, x):
        """
        Let f be this linear equation, return f(x).

        :param x: The abscissa of the point.
        :return: f(x) if defined, raises an exception otherwise.
        """
        try:
            return round(self.a * x + self.b, self.n_digits_round)
        except ArithmeticError as a:
            raise(a)
        return None

    def reverse(self, y):
        """
        lef f be this linear equation, return f-1(y).

        :param y: The ordinate of the point.
        :return: f-1(y) if defined, raises an exception otherwise.
        """
        try:
            return round((y - self.b) / self.a)
        except ArithmeticError as a:
            raise(a)
        return None

    def is_point_on(self, point):
        """
        Checks if a point is on this linear equation.

        :param point: The point to test.
        :return: True if the point is on the LE, False otherwise.
        """
        if self.apply(point.x) == point.y:
            return True
        return False

    def intersection(self, other):
        """
        Checks if there exists an intersection point between this LE and the given one.
        Formula: ax + b = a'x+ b' <=> x = (b' - b) / (a - a')

        :param other: The second LE to use.
        :return: return the intersection point if it exists, if it doesn't, returns None.
        """
        if self.a == other.a:
            return None

        p_1 = (other.b - self.b) / (self.a - other.a)
        return Point(p_1, self.apply(p_1))

    @classmethod
    def intersection_circle(self, p, angle, origin, radius):
        """
        Checks whether a LE, defined by a point and an angle intersect a circle of origin 
        'origin' and radius 'radius'.
        To do so it checks whether the projection of the origin on the LE is at a distance
        smaller than the radius of the origin.

        There are a lot of exceptions here to take into account, see specific comments for 
        detailed explanations.

        :param p: The point defining the LE.
        :param angle: The angle defining the LE.
        :param origin: The origin of the circle.
        :param radius: The radius of the circle.
        :return: the intersection point if it exists, None otherwise.
        """

        # If the angle is pi/2, then tan(angle) is undefined
        # If this case it means that the LE is a vertical line therefore the circle
        # intersects the LE iff its x coordinate is at most at a distance 'radius'
        # of the x coordinate of the given point 'p'.
        if abs(angle) == math.pi / 2:
            if abs(p.x - origin.x) <= radius:
                return Point(p.x, origin.y)
            return None

        # If the angle is 0, pi or -pi, then cot(angle) is undefined
        # If this case it means that the LE is a horizontal line therefore the circle
        # intersects the LE iff its y coordinate is at most at a distance 'radius'
        # of the y coordinate of the given point 'p'.
        if angle == 0 or abs(angle) == math.pi:
            if abs(p.pos.y - origin.y) <= radius:
                return Point(origin.x, p.pos.y)
            return None
        
        # LE(1) of the point 'p' and angle 'angle'
        tan_angle = math.tan(angle)

        # LE(2) used to find the projection of the origin of the circle on LE(1)
        # This basically the perpendicular linear equation to LE(1) that passes through 'origin'.
        cot_angle = 1 / tan_angle
        
        # Defining both LE (normally all undefined cases are handled)
        le1 = LinearEquation(-cot_angle, origin.y + cot_angle * origin.x)
        le2 = LinearEquation(tan_angle, p.pos.y - tan_angle * p.pos.x)

        # Get the intersection point, it obviously exists by the definition of LE(2)
        p_intersect = le1.intersection(le2)

        # Checking if the distance between the origin and the projection is less than radius
        # if it is, return this point, otherwise return None
        if p_intersect.distance(origin) <= radius:
            return p_intersect
        return None

    @classmethod
    def create_le_from_pa(self, point, angle):
        """
        Creates a new 'LinearEquation' object from a point and an angle.

        :param point: A point that the line goes through.
        :param angle: The angle of the line w.r.t the origin.
        :return: The newly created 'LinearEquation' object.
        """
        if abs(angle) == math.pi / 2:
            return None

        tan_angle = math.tan(angle)
        return LinearEquation(tan_angle, point.y - tan_angle * point.x)

    @classmethod
    def create_le_from_pp(self, p1, p2):
        """
        Creates a new 'LinearEquation' object from two points.

        :param point: A point that the line goes through.
        :param point: Another point that the line goes through.
        :return: The newly created 'LinearEquation' object.
        """
        if p1.x == p2.x:
            return None
        
        a = (p2.y - p1.y) / (p2.x - p1.x)
        b = p1.y - a * p1.x
        return LinearEquation(a, b)