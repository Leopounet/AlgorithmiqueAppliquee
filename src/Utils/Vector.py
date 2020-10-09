import math

class Vector:

    n_digits_round = 15

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Vector(self.x * other, self.y * other)
        return self.x * other.x + self.y * other.y

    def __rmul__(self, other):
        if isinstance(other, (int, float)):
            return Vector(self.x * other, self.y * other)
        return self.x * other.x + self.y * other.y

    def __truediv__(self, const):
        if const == 0:
            raise ZeroDivisionError("const must not be 0")

        return Vector(self.x / const, self.y / const)

    def __rtruediv__(self, const):
        if const == 0:
            raise ZeroDivisionError("const must not be 0")

        return Vector(self.x / const, self.y / const)

    def norm(self):
        res = math.sqrt(pow(self.x, 2) + pow(self.y, 2))
        return round(res, self.n_digits_round)

    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"

    def normalize(self, in_place=True):
        norm = self.norm()
        x = self.x / norm
        y = self.y / norm

        if in_place:
            self.x = x
            self.y = y
            return self
        return Vector(x, y)           

    def angle(self, other):
        return round(math.acos(self * other / self.norm() * other.norm()), self.n_digits_round)

    @classmethod
    def v_from_pp(self, a, b):
        v = b - a
        return Vector(v.x, v.y)

    @classmethod 
    def v_from_pa(self, a, theta):

        # Unlikely to happen? Should we add an epsilon margin?
        if theta == math.pi / 2:
            return Vector(0, 1)

        # Same remark
        if theta == -math.pi / 2:
            return Vector(0, -1)

        return Vector(1, round(math.tan(theta), self.n_digits_round))