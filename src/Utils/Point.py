import math

"""
This module is used to emulate points in the 2D plane (could be extended to the 3D plane
but so far there is no use for that in this project).
"""

class Point:

    """
    This class simulates a point in the 2D plane. 
    """
    
    # The max number of digits after the decimal point (then
    # rounded if exceeded). Useful because of approximation problems linked to Python and
    # computers in general.
    n_digits_round = 10

    def __init__(self, x=0, y=0):
        """
        Constructs a new 'Point' object. 

        :param x: The x coordinate of the point. 

        :param y: The y coordinate of the point.
        """
        self.x = round(x, self.n_digits_round)
        self.y = round(y, self.n_digits_round)

    def __add__(self, other):
        """
        Overload of the + operator. 

        :param other: The second point to consider. 

        :return: the sum of the two points.
        """

        # Not super clean but technically 'other' can be a vector
        # (could use instanceof just for completion sake but as long as Vector's members are
        # x and y it is fine, although just a tiny bit risky)
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        """
        Overload of the - operator. 

        :param other: The second point to consider. 

        :return: the difference of the two points.
        """

        # Same remark as for the addition
        return Point(self.x - other.x, self.y - other.y)

    def __mul__(self, const):
        """
        Overload of the * operator. 

        :param const: The constant to multiply the point by. 

        :return: the product of the point by the constant.
        """
        return Point(self.x * const, self.y * const)

    def __truediv__(self, const):
        """
        Overload of the / operator. Raises an error if const = 0. 

        :param const: The constant to divide the point by. 

        :return: the result of the division of the point by the constant.
        """
        if const == 0:
            raise ZeroDivisionError("const must not be 0")

        return Point(self.x / const, self.y / const)

    def __rmul__(self, const):
        """
        Overload of the * operator. 

        :param const: The constant to multiply the point by. 

        :return: the product of the point by the constant.
        """
        return Point(self.x * const, self.y * const)

    def __rtruediv__(self, const):
        """
        Overload of the / operator. Raises an error if const = 0. 

        :param const: The constant to divide the point by. 

        :return: the result of the division of the point by the constant.
        """
        if const == 0:
            raise ZeroDivisionError("const must not be 0")

        return Point(self.x / const, self.y / const)

    def __str__(self):
        """
        Used to use print(p) where p is a point. 

        :return: the corresponding string.
        """
        return "(" + str(self.x) + ", " + str(self.y) + ")"

    def distance(self, other):
        """
        Computes the euclidian distance between this point and the given one. 

        :param other: The other point to consider. 

        :return: The distance between the two points.
        """
        return math.sqrt(pow(other.x - self.x, 2) + pow(other.y - self.y, 2))

    def mid_point(self, other):
        """
        Computes the mid point of the segment created by this point and the given one. 

        :param other: The other point to consider to create the segment. 
            
        :return: The mid point of the segment created by this point and the given one.
        """
        return Point((self.x + other.x) / 2, (self.y + other.y) / 2)