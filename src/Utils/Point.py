import math

class Point:

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __add__(self, other):
        # Not super clean but technically 'other' can be a vector
        # (could use inspect just for completion sake but as long as Vector's members are
        # x and y it is fine, although just a tiny bit risky)
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        # Same remark as for the addition
        return Point(self.x - other.x, self.y - other.y)

    def __mul__(self, const):
        return Point(self.x * const, self.y * const)

    def __truediv__(self, const):
        if const == 0:
            raise ZeroDivisionError("const must not be 0")

        return Point(self.x / const, self.y / const)

    def __rmul__(self, const):
        return Point(self.x * const, self.y * const)

    def __rtruediv__(self, const):
        if const == 0:
            raise ZeroDivisionError("const must not be 0")

        return Point(self.x / const, self.y / const)

    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"

    def distance(self, other):
        return math.sqrt(pow(other.x - self.x, 2) + pow(other.y - self.y, 2))

    def mid_point(self, other):
        return Point((self.x + other.x) / 2, (self.y + other.y) / 2)