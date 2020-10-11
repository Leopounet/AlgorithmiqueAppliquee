import math

"""
This module is used to emulate vectors in the 2D plane (could be extended to the 3D plane
but so far there is no use for that in this project).
"""

class Vector:

    """
    This class simulates a vector in the 2D plane.

    :member n_digits_round: The max number of digits after the decimal point (then
    rounded if exceeded). Useful because of approximation problems linked to Python and
    computers in general.
    """

    n_digits_round = 10

    def __init__(self, x=0, y=0):
        """
        Constructs a new 'Vector' object.

        :param x: The x coordinate of the vector.
        :param y: The y coordinate of the vector.
        """
        self.x = round(x, self.n_digits_round)
        self.y = round(y, self.n_digits_round)

    def __add__(self, other):
        """
        Overload of the + operator.

        :param other: The second vector to consider.
        :return: the sum of the two vectors.
        """
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        """
        Overload of the - operator.

        :param other: The second vector to consider.
        :return: the difference of the two vectors.
        """
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        """
        Overload of the * operator to represent the scalar product.

        :param other: The other vector to use for the scalar product.
        :return: the result of the scalar product.
        """
        if isinstance(other, (int, float)):
            return Vector(self.x * other, self.y * other)
        return round(self.x * other.x + self.y * other.y, self.n_digits_round)

    def __rmul__(self, other):
        """
        Overload of the * operator to represent the scalar product.

        :param other: The other vector to use for the scalar product.
        :return: the result of the scalar product.
        """
        if isinstance(other, (int, float)):
            return Vector(self.x * other, self.y * other)
        return round(self.x * other.x + self.y * other.y, self.n_digits_round)

    def __truediv__(self, const):
        """
        Overload of the / operator. Raises an error if const = 0.

        :param const: The constant to divide the vector by.
        :return: the result of the division of the vector by the constant.
        """
        if const == 0:
            raise ZeroDivisionError("const must not be 0")

        return Vector(self.x / const, self.y / const)

    def __rtruediv__(self, const):
        """
        Overload of the / operator. Raises an error if const = 0.

        :param const: The constant to divide the vector by.
        :return: the result of the division of the vector by the constant.
        """
        if const == 0:
            raise ZeroDivisionError("const must not be 0")

        return Vector(self.x / const, self.y / const)

    def norm(self):
        """
        Returns the norm of this vector.
        :return: The norm of the vector.
        """
        res = math.sqrt(pow(self.x, 2) + pow(self.y, 2))
        return round(res, self.n_digits_round)

    def __str__(self):
        """
        Used to use print(v) where v is a vector.

        :return: the corresponding string.
        """
        return "(" + str(self.x) + ", " + str(self.y) + ")"

    def normalize(self, in_place=True):
        """
        Normalizes this vector so that its norm is 1. If the norm of the vector is 0,
        raises an error.

        :param in_place (opt): If True, this vector is directly modified and no new vector is
        created, if False a new vector is created and returned (default: True).

        :return: The normalized vector (whether it is this vector or a new one).
        """

        # Get the norm
        norm = self.norm()

        # If the norm is zero, raise an error.
        if norm == 0:
            raise ZeroDivisionError("vector's norm can not be 0")

        # Normalization process.
        x = self.x / norm
        y = self.y / norm

        # If in place, modify this vector and return it (not necessary but it is cleaner because
        # it makes the behavior of this method consistent).
        if in_place:
            self.x = round(x, self.n_digits_round)
            self.y = round(y, self.n_digits_round)
            return self
        return Vector(x, y)           

    def angle(self, other):
        """
        Computes the angle formed between two vectors that have the same origin point.
        The formula is derived from the scalar product.
        Let u and v be two vectors, then u . v = norm(u) * norm(v) * cos(angle)
        After some transformation, angle = acos(u.v / ( norm(u) * norm(v) ))

        :param other: The second vector to use to compute the angle.
        :return: The angle between the two vectors.
        """
        return round(math.acos(self * other / (self.norm() * other.norm())), self.n_digits_round)

    @classmethod
    def v_from_pp(self, a, b):
        """
        Creates a vector from two points.

        :param a: The origin of the vector.
        :param b: The second point used to define the vector.
        :return: The created vector.
        """
        v = b - a
        return Vector(v.x, v.y)

    @classmethod 
    def v_from_a(self, theta):
        """
        Creates a vector from an angle.

        :param theta: The angle to consider.
        :return: The created vector.
        """

        # If theta = pi/2, then tan(theta) is undefined
        # In this case, the vector is vertical and going to positive y
        if theta == math.pi / 2:
            return Vector(0, 1)

        # If theta = -pi/2, then tan(theta) is undefined
        # In this case, the vector is vertical and going to negative y
        if theta == -math.pi / 2:
            return Vector(0, -1)

        if abs(theta) > math.pi / 2:
            return Vector(-1, -round(math.tan(theta), self.n_digits_round))
        return Vector(1, round(math.tan(theta), self.n_digits_round))