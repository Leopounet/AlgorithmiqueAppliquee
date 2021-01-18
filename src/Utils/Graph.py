import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import math
from src.Utils.Vector import Vector
from src.Utils.Point import Point
from src.Utils.ConvexShape import ConvexShape
from src.Utils.UsefulTypes import Opponent, Shot, Defender, Goal
from src.Utils.LinearEquation import LinearEquation
from src.ProblemUtils.ProblemType import ProblemType

"""
This modules is used to represent a graph for this specific problem, so 
it may be esoteric.
"""

class Graph:

    """
    This class represents a graph.

    :ivar defenders: This is a list of all the Defender objects that can be placed on \
    the field (at first). These are one of the two parts of our vertices. 

    :ivar opponents: A list of all the opponents on the field. This isn't used in the \
    Graph per se, but it is important for efficiency reasons (see exists_collision). 

    :ivar shots: This is a list of all the possible shots. This is the second part of our vertices.

    :ivar edges: This is a specific representation of edges. This is a list of numbers where their \
    binary representation represents the graph's matrix. 

    For example, if G has 3 vertices you can expect:

    | 1101
    | 1010
    | 1100

    This is looking exactly like a normal matrix. Except that actually extracting an edge out of \
    this representation is not efficient. That being said, it is an interesting representation \
    because it allows us to quickly check if a set of vertices cover the whole graph. 

    Back on the example, choose v1 and v3, and compute 1101 | 1100 (fast on computers), \
    it returns 1101. Therefore those two vertices do NOT represent a dominant set. On the other \
    hand, choose v1 and v2, 1101 | 1010 gives as a result 1111, therefore v1 \
    and v2 is a dominant set of G. 

    :ivar dominant_value: This is the expected value if the disjunction of the binary representations \
    of the selected vertices is a dominant set. 
    """

    def __init__(self, problem, optimized=True):
        """
        Construct a new 'Graph' object. 

        :param problem: The problem to use to construct the graph.

        :param optimized (opt): If set to true, a defender will be considered interesting iff \
        it is on at least one edge of the triangles (see below for explanations on those). True \
        by default. Note that this optimization can lead to losing some valid solution and in the \
        worst cases can lead to not find solutions when some exist.

        :return: returns nothing.
        """

        # the list of defenders in the final graph
        # that is those that block at least one shot
        self.defenders = []

        # the list of opponents in the graph
        self.opponents = []

        # the list of all shots in the graph
        # this list is actually a list of list
        # each sub list corresponds to all the valid shots
        # between a given opponent and a given goal
        # therefore if there 3 opponents and 2 goals for example
        # there will be 6 sub lists
        self.shots = []

        # the list of edges in the graph, an edge exists
        # between a defender and a shot if the shot is intercepted
        # by this defender
        #
        # note that this is used as a adjacency matrix
        # we also actually take advantage of Python's huge number
        # limit
        #
        # the list is actually a list of integers with their
        # binary representation being the adjacency matrix
        # each number corresponds to the 'list' of shots blocked by 
        # the nth defender
        #
        # for example 10111010
        # means that the nth defenders blocks shots 2, 3, 4, 6
        # (the first one is a place holder so that every integer has
        # the exact same binary length)
        self.edges = []

        # as explained above, in a to become dominanting set we basically "or" all the 
        # corresponding edges together, the resulting value of an actual dominanting set
        # is this value 
        self.dominant_value = 0

        # the index of the defender blocking the greatest amount of shots
        self.max_deg_index = 0

        # the maximum number of blocked shots by a defender
        self.max_deg = 0

        # the list of degrees (= number of blocked shots) associated to each defender
        self.deg = []

        # this is a list of triangles drawn between each pair of goal and opponent
        self.triangles = []

        # each opponent has an 'optimal' distance from it at which if a defender is placed
        # it will block all their shots wrt a goal (note that this distance could be less than  
        # the radius of the robots if the opponent is very close to the goal)
        # when a defender is placed, we can compute how good his placement is wrt all the optimal
        # placements
        #
        # this clearly could be improved, to give a 'higher weight' to defenders that are very close
        # to the optimal distance of one opponent (here all opponents have the same importance
        # if the opponents are all far away from each other, this value is almost useless)
        self.total_distance_defender = []

        # the total number of shots
        self.nb_shots = 0

        # the problem to solve
        self.problem = problem

        # if True the graph generated will lose some valid solutions but will also
        # make it much much easier for solvers to find an optimal solution
        self.optimized = optimized

        # compute everything needed for the graph
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
        # (impossible for now in the case of ball speed, although it should be possible
        # also, some defenders should be easy to exclude in this extension...)
        self.compute_triangles(problem["goals"])
        self.compute_all_positions(problem["bottom_left"], problem["top_right"], 
                                   problem["pos_step"], problem["radius"], problem["goals"])

    def compute_triangles(self, goals):
        """
        Computes triangles from all opponents to a given goal. 

        :param goal: The goal to consider. 

        :return: The list of triangles.
        """
        for goal in goals:
            for opponent in self.opponents:
                self.triangles.append(ConvexShape.compute_triangle(opponent, goal))

    def point_in_triangles(self, point):
        """
        Computes the list of all triangles the point is in. 

        :param point: The point to check. 

        :return: The list of triangles the point is in.
        """

        # the list of triangles (by index) the points is in
        tmp = []

        # the current index of the triangle considered
        index = 0
        
        # get the radius of the robots
        radius = self.problem["radius"]

        # creating a new defender object to call the following methods
        # we could use some overload but that implies duplicating some code
        # which is not something we want for this specific project
        # for it is already pretty difficult to navigate
        defender = Defender(point, radius)

        # loop through all the triangles
        for triangle in self.triangles:
            
            # get the angles of the two sides of the triangle going towards the goal
            angle1 = math.atan(LinearEquation.create_le_from_pp(triangle.points[0], triangle.points[1]).a)
            angle2 = math.atan(LinearEquation.create_le_from_pp(triangle.points[0], triangle.points[2]).a)

            # if the defender does not intersect either of those lines, then it is not interesting
            # the idea behind this choice is that, except in specific cases, a defender in the middle
            # of a triangle is not useful, because then you obviously need two more defenders to complete
            # the triangle (if not more)
            #
            # although this is true in most cases, it's important to note that this does
            # remove some possible solutions, and in the worst cases, it removes all the 
            # possible solutions, this why there is an option to deactivate this optimization
            if (LinearEquation.intersection_circle(defender, angle1, triangle.points[0], radius) != None or
                LinearEquation.intersection_circle(defender, angle2, triangle.points[0], radius) != None or
                (not self.optimized and triangle.point_in(point))):
                tmp.append(index)
            index += 1
        return tmp.copy()

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

        opt = (radius / 2) / math.tan(angle)
        return opt

    def compute_distance_sum(self, defender, index_tr, index_def):
        """
        Computes a value to know how optimal a defender's position is. 

        :param defender: The defender ton consider. 

        :param index_tr: Index correspoding to the current triangle. 

        :param index_def: The index correspoding to the current defender. 

        :return: returns nothing.
        """

        # get the optimal distance from the opponent
        opt = self.perfect_distance_from_triangle(self.triangles[index_tr], defender.radius)

        # get the distance of the current defender
        dst = defender.pos.distance(self.triangles[index_tr].points[0])

        # if this is the first time we consider this defender, create a new 
        # cell for it
        if len(self.total_distance_defender) <= index_def:
            self.total_distance_defender.append(abs(opt - dst) * 10)

        # otherwise sum the difference of this placement with all the previously computed distances
        else:
            self.total_distance_defender[index_def] = min(self.total_distance_defender[index_def], abs(opt - dst) * 10)

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

        # in all the cases, but max_speed, we can use shot_intercepted because we
        # consider the defender as it is
        if self.problem.type != ProblemType.MAX_SPEED:
            for goal in goals:
                if goal.shot_intercepted(defender, shot):
                    return True

        # but in the case of max_speed, we need to use a different method
        # that computes distance and speed instead of checking if the shot is blocked
        # by the defender (more info in UsefulTypes/Goal)
        else:
            ball_speed = self.problem["ball_max_speed"]
            player_speed = self.problem["robot_max_speed"]
            for goal in goals:
                if goal.shot_intercepted_with_speed(defender, shot, ball_speed, player_speed):
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

                in_triangle = None
                if not self.problem.type == ProblemType.MAX_SPEED:
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
                    if in_triangle == None or i in in_triangle:
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
                if edges != (self.dominant_value + 1) // 2:

                    # add the defender to the list of possible defenders
                    self.defenders.append(defender)

                    # add the corresponding edge (= blocked shots)
                    self.edges.append(edges)

                    # update the maximum degree found (and its index)
                    if self.max_deg != max(self.max_deg, deg):
                        self.max_deg = deg
                        self.max_deg_index = index

                    # add the degree of this node to the list of degrees
                    self.deg.append(deg)
                    index += 1

                # we created a cell in case, but we can remove it if the defender is useless
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

        :param arrays: A list of arrays, the first one should be the one to sort. Note that all arrays \
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
        """
        Transforms a list of defenders indices into a list of defenders.

        :param indices: The indices representing defenders.

        :return: The corresponding list of defenders.
        """

        # security check
        if indices == None:
            return None

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
                

