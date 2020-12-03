import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import math
from src.Utils.LinearEquation import LinearEquation
from src.Utils.Vector import Vector

"""
This modules is used to create polygons in 2D space. 
"""

class ConvexShape:

    """
    Simulates polygons in 2D space. The shape can be not convex but in this case all methods
    of this class are likely to not work properly.
    """

    def __init__(self, points):
        """
        Constructs a new 'ConvexShape'. It is considered that two consecutive points in the given
        set of points do form a side of the polygon. 

        :param points: The ste of points defining the polygon. 

        :return: returns nothing.        
        """
        self.points = points

    def __str__(self):
        """
        Allows the use of print(cs) where cs is a 'ConvexShape' object. 

        :return: The correspoding string.
        """
        res = ""
        for point in self.points:
            res += str(point) + " "
        return res

    # All methods created to create this method come from this answer on stackoverflow
    # # https://stackoverflow.com/questions/1119627/how-to-test-if-a-point-is-inside-of-a-convex-polygon-in-2d-integer-coordinates
    def point_in(self, point):
        """
        Detects if the given point is inside this polygon. 

        :param point: The point to check. 

        :return: True if the point is in the polygon, False otherwise.
        """
        prev_side = 0
        nb_vertices = len(self.points)

        for v in range(nb_vertices):
            # The mod is here because last and first vertices have to be checked (would be an overflow otherwise)
            a, b = self.points[v], self.points[(v+1) % nb_vertices]
            seg = a - b
            p = point - a
            current_side = self.side(seg, p)

            if not current_side:
                return False
            
            elif not prev_side:
                prev_side = current_side

            elif prev_side != current_side:
                return False

        return True
    
    @classmethod
    def side(self, p1, p2):
        cosine = p1.x * p2.y - p1.y * p2.x
        return 0 if not cosine else cosine / abs(cosine)

    @classmethod
    def compute_triangle(self, opponent, goal):
        """
        Computes a triangle representing a set of shots. It constructed using
        an opponent and a goal. It draws a triangle going from the center of the opponent
        to the edges of the goal. All valid shots going towards this goal are guaranteed to 
        be in this triangle. 

        :param opponent: The opponent to consider. 

        :param goal: The goal to consider. 

        :return: A new 'ConvexShape' that is a triangle with the opponent position first.
        """
        points = []
        points.append(opponent.pos)
        points.append(goal.s_pos)
        points.append(goal.e_pos)
        return ConvexShape(points)

    @classmethod
    def compute_bigger_triangle(self, triangle, size):
        """
        Computes a new (bigger in theory) triangle, given a first one. This method's name
        isn't great because it considers that the triangle represents a set of shots (cf above). 

        It is used to consider every point that are at most at distance 'size' from the given triangle.
        That being said, it doesn't extend the triangle behind the goal because no shot is going there
        so this would be pointless. 

        :param triangle: The triangle to biggen. 

        :param size: The distance between the two triangles (radius of a robot basically). 
            
        :return: The newly created triangle.
        """

        # The three new points of the triangle
        t_p1 = None
        t_p2 = None
        t_p3 = None

        # A vector to biggen the goal's segment size
        v = Vector.v_from_pp(triangle.points[1], triangle.points[2]).normalize()
        t_p2 = triangle.points[2] + v * size
        t_p3 = triangle.points[1] - v * size

        # Vectors from the goal to the opponent
        v1 = Vector.v_from_pp(t_p3, triangle.points[0])
        v2 = Vector.v_from_pp(t_p2, triangle.points[0])

        # The resulting vector defines where the last point is w.r.t the old triangle
        v = (v1 + v2).normalize()

        t_p1 = triangle.points[0] + 4 * v # * size

        return ConvexShape([t_p1, t_p2, t_p3])