import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import math
from src.Utils.Vector import Vector
from src.Utils.Point import Point
from src.Utils.ConvexShape import ConvexShape
from src.Utils.UsefulTypes import Opponent, Shot, Defender
from src.ProblemType import ProblemType
import random
import time

"""
This modules is used to represent a graph for this specific problem, so 
it may be esoteric.
"""

class Graph:

    """
    This class represents a graph.
    """

    def __init__(self, problem):
        """
        Construct a new 'Graph' object.

        :param problem: The problem to use to construct the graph.

        :member defenders: This is a list of all the Defender objects that can be placed on the field (at first).
        These are one of the two parts of our vertices.

        :member opponents: A list of all the opponents on the field. This isn't used in the Graph per se, but it
        is important for efficiency reasons (see exists_collision).

        :member shots: This is a list of all the possible shots (whether are not they are aimed at a goal). This is the 
        second part of our vertices.

        :member edges: This a specific representation of edges. This a list of numbers where there binary representation
        represents the graph's matrix. 

        For example, if G has 3 vertices you can expect:
        101
        010
        100
        This is looking exactly like a normal matrix. Except that actually extracting an edge out of this representation
        is not efficient. That being said, it is an interesting representation because it allows us to quickly check
        if a set of vertices cover the whole graph.

        Back on the example, if I choose v1 and v3, and compute 101 | 100 (fast on computers), I get 101. Therefore those
        two vertices do NOT represent a dominant set. On the other hand, if I choose v1 and v2, I get 101 | 010, which 
        gives as a result 111, therefore v1 and v2 is a dominant set of G.

        :member dominant_value: This is the expected value if the disjunction of the binary representations of the selected
        vertices is a dominant set.

        :return: returns nothing.
        """
        self.defenders = []
        self.opponents = []
        self.shots = []
        self.edges = []
        self.dominant_value = 0

        self.min_deg_index = 0
        self.max_deg_index = 0
        self.min_deg = None
        self.max_deg = 0
        self.max_deg_after = []
        self.deg = []

        self.triangles = []
        self.total_distance_defender = []

        self.nb_shots = 0

        self.problem = problem

        self.compute_graph(problem)

    def compute_graph(self, problem):
        """
        Computes all the vertices and edges of the graph. The order of operation here is critical.
        For instance, dominant_values can only exist if the the set of shots is complete and 
        the computation of the positions is only possible with the set of shots and the 
        dominant value.
        """
        # Computes all valid shots
        self.opponents = problem["opponents"]
        self.compute_all_shots(problem["opponents"], problem["theta_step"], problem["goals"])
        self.dominant_value = pow(2, self.nb_shots + 1) - 1

        # Computes all interesting position (those that stop at least one shot)
        self.compute_triangles(problem["goals"], problem["radius"])
        self.compute_all_positions(problem["bottom_left"], problem["top_right"], 
                                   problem["pos_step"], problem["radius"], problem["goals"])

    def compute_default_triangles(self, goal):
        """
        Computes triangles from all opponents to a given goal.

        :param goal: The goal to consider.
        :return: The list of triangles.
        """
        triangles = []
        for opponent in self.opponents:
            triangles.append(ConvexShape.compute_triangle(opponent, goal))
        return triangles.copy()

    def compute_new_triangles(self, triangles, radius):
        """
        Computes a bigger triangle to account for the radius of the robots.

        :param triangles: The list of created triangles.
        :param radius: The radius of the robots.
        :return: A new list of triangles.
        """
        new_triangles = []
        for triangle in triangles:
            new_triangles.append(ConvexShape.compute_bigger_triangle(triangle, radius))
        return new_triangles.copy()

    def point_in_triangles(self, point):
        """
        Computes the list of all triangles the point is in.

        :param point: The point to check.
        :return: The list of triangles the point is in.
        """
        tmp = []
        index = 0
        for triangle in self.triangles:
            if triangle.point_in(point):
                tmp.append(index)
            index += 1
        return tmp.copy()

    def compute_triangles(self, goals, radius):
        """
        Computes the list of all the triangles to consider. 

        A triangle is a zone delimited by three points: an opponent and two goal posts. Here
        all the possible triangles are computed. All shots are guaranteed to be represented by those triangles.
        The triangles computes are a bit bigger to account for the size of the robots (a defender might 
        not be in the original triangle and still stop a shot).

        :param goals: The list of goals.
        :param radius: Teh radius of the robots.
        :return: returns nothing.
        """
        for goal in goals:
            self.triangles += self.compute_new_triangles(self.compute_default_triangles(goal), radius)

    def compute_all_shots(self, opponents, step, goals):
        """
        Computs all useful shots and adds them to the list of shots.

        - KEEPS shots aimed at at least one goal
        - Ideas?

        :param opponents: The list of opponents to consider the shots of.
        :param step: Used to compute a finite number of angles when considering an opponent.
        :param goal: The goal (or list later, I guess) to consider.
        :return: returns nothing.
        """
        
        # Parsing the list of goals
        for goal in goals:

            # Parsing the opponents list
            for opponent in opponents:

                # Low bound for an angle
                angle = -math.pi

                tmp = []

                # Parse all possible angle in [-pi ; pi[
                while angle < math.pi:

                    # If this shot is valid (i.e: goes in the goal), it is added to the list of shots
                    shot = Shot(opponent, angle)
                    if goal.is_shot_valid(shot):
                        self.nb_shots += 1
                        tmp.append(shot)
                    angle += step
                
                self.shots.append(tmp.copy())

    def perfect_distance_from_triangle(self, triangle, radius):
        """
        Computes the perfect distance for a defender to be, with regard
        to a triangle representing a set of valid shots. A perfect distance is
        the maximum distance from the opponent at which the defender can be and stop all the shots.

        :param triangle: The set of shots to consider.
        :param radius: The radius of the robots.
        :return: The perfect distance for this set of shots. 
        """
        v1 = Vector.v_from_pp(triangle.points[0], triangle.points[1])
        v2 = Vector.v_from_pp(triangle.points[0], triangle.points[2])

        angle = v2.angle(v1) / 2

        if abs(angle) == math.pi / 2 or angle == 0 or abs(angle) == math.pi:
            return 100

        opt = radius / math.tan(angle) + radius
        return opt

    def compute_distance_sum(self, defender, index_tr, index_def):
        """
        Computes a value to know how optimal a defender's position is.

        :param defender: The defender ton consider.
        :param index_tr: Index correspoding to the current triangle.
        :param index_def: The index correspoding to the current defender.
        :return: returns nothing.
        """
        opt = self.perfect_distance_from_triangle(self.triangles[index_tr], defender.radius)
        dst = defender.pos.distance(self.triangles[index_tr].points[0])

        if len(self.total_distance_defender) <= index_def:
            self.total_distance_defender.append(abs(opt - dst))
        else:
            self.total_distance_defender[index_def] = min(self.total_distance_defender[index_def], abs(opt - dst))

    def exists_collision_opponents(self, defender, radius):
        """
        Check if there exists a collision between at least one opponent and one defender.

        :param defender: The defender to check the collisions of.
        :return: True if at least one collision exists, False otherwise.
        """
        for opponent in self.opponents:
            if defender.collision(opponent, radius):
                return True
        return False

    def exist_goal(self, defender, shot, goals):
        """
        Checks if the current defender intercepts the shot, with regard to at least
        one goal.

        :param defender: The defender that should intercept a shot.
        :param shot: The shot to intercept.
        :param goals: The list of goals to check.
        :return: True if the defender intercepts at least one shot, False otherwise.
        """
        for goal in goals:
            if goal.shot_intercepted(defender, shot):
                return True
        return False

    def compute_all_positions(self, bottom_left, top_right, step, radius, goals):
        """
        Computes all useful positions for the defenders.

        - KEEPS positions where at least one valid shot (computed first) is intercepted
        - REMOVES positions where there is a collision with an opponent
        - Ideas?

        :param bottom_left: The bottom left point of the field.
        :param top_right: The top right point of the field.
        :param step: Used to compute a finite number of positions for the defensers.
        :param radius: Radius of a robot.
        :param goal: The goal (soon goals, I guess) to consider.
        :return: returns nothing.
        """
        index = 0
        # x coordinate being considered
        # goes from left to right
        x = bottom_left.x
        while x <= top_right.x:

            # y coordinate being considered
            # goes bottom to top
            y = bottom_left.y
            while y <= top_right.y:

                p = Point(x, y)

                in_triangle = self.point_in_triangles(p)
                if in_triangle == []:
                    y += step
                    continue

                # Current defender (if it were to be placed here)
                defender = Defender(p, radius)
                deg = 0

                # If there is a collision, go to the next position
                if self.problem.type == ProblemType.MIN_DIST:
                    if self.exists_collision_opponents(defender, self.problem["min_dist"]):

                        # Okay so, putting a break here works somehow much better
                        # but neglects a lot of solutions
                        y += step
                        continue

                else:
                    if self.exists_collision_opponents(defender, self.problem["radius"] * 2):

                        # Okay so, putting a break here works somehow much better
                        # but neglects a lot of solutions
                        y += step
                        continue

                # The numerical representation of the edge for now
                # it is 1 and not 0 because otherwise, as long as no shots is intercepted, the number would
                # remain 0, losing a lot of information
                edges = 1

                # Checking every valid shot, if at least one is intercepted, the defender gets added to
                # the list
                for i in range(len(self.triangles)):
                    if i in in_triangle:
                        self.compute_distance_sum(defender, i, index)
                        for shot in self.shots[i]:
                            if self.exist_goal(defender, shot, goals):
                                    
                                # Shifting to the left (*2) and adding one to signify that
                                # an edge exists
                                edges = (edges << 1) + 1
                                deg += 1
                            else:
                                edges = edges << 1
                    else:
                        edges = edges << len(self.shots[i])
                
                # If the result is not 1
                # The defender is added (because it isn't useless)
                if edges != (self.dominant_value + 1) / 2:
                    self.defenders.append(defender)
                    self.edges.append(edges)
                    if self.min_deg == None:
                        self.min_deg = deg
                    self.min_deg = min(self.min_deg, deg)
                    self.max_deg = max(self.max_deg, deg)
                    self.min_deg_index = index
                    self.max_deg_index = index
                    self.deg.append(deg)
                    index += 1
                else:
                    del self.total_distance_defender[-1]
                
                y += step
            x += step

    def valid_defender(self, def_list, new_def):
        """
        Check if there exists a collision between a new defender and a list of pre existing defender.
        It only checks if the new defender creates a collision, elements of the list could have collision
        between them.

        :param def_list: The list of defenders to compare the defender to.
        :param new_def: The defender that shall not have collisions with defenders in the list.
        :return: True if there exists a collision, False otherwise.
        """
        radius = self.problem["radius"] * 2
        if self.problem.type == ProblemType.MIN_DIST:
            radius = self.problem["min_dist"]

        for defender in def_list:
            if self.defenders[defender].collision(self.defenders[new_def], radius):
                return False
        return True

    def swap(self, arr, i, j):
        """
        Swaps two elements of an array.

        :param arr: The array to consider.
        :param i: The index of the first element.
        :param j: The index of the second element.
        :return: returns nothing.
        """
        tmp = arr[i]
        arr[i] = arr[j]
        arr[j] = tmp

    def bubble_sort(self, arrays, compare_func):
        """
        Sorts a set of arrays according to the first array given (it is useful to preserve 1-to-1
        relations in different arrays while sorting a specific one).

        :param arrays: A list of arrays, the first one should be the one to sort. Note that all arrays
        must have the same size.
        :param compare_func: The function to use to sort the arrays (e.g: fun x y -> x < y).
        :return: returns nothing.
        """
        to_sort = arrays[0]
        for i in range(0, len(to_sort)):
            for j in range(0, len(to_sort) - i - 1):

                # If the given comparing function is satisfied, sort all arrays
                if compare_func(to_sort[j], to_sort[j+1]):
                    for arr in arrays:
                        self.swap(arr, j, j+1)

    def index_list_to_defenders(self, indices):
        res = []
        for i in indices:
            res.append(self.defenders[i])
        return res.copy()

    def __str__(self):
        """
        Converts the graph to a string and allows us to type things like
        print(graph).

        :return: The string corresponding to the graph.
        """
        res = ""
        for x in self.edges:
            res += str(bin(x))[2:]
            res += "\n"
            
        return res
                

