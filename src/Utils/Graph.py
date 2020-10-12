import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import math
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

        self.max_deg = 0
        self.deg = []
        self.max_deg_after = []

        self.triangles = []
        self.nb_shots = 0

        self.problem = problem

        self.compute_graph(problem)

    def compute_graph(self, problem):
        """
        Computes all the vertices and edges of the graph. The order of operation here is critical.
        For instance, dominant_values can only exist if the the set of shots is complete and 
        the computation of the positions is only possible with the set of shots and the 
        dominant value.

        Please improve the argument list, like ew. Create a class maybe?
        """
        self.opponents = problem["opponents"]
        self.compute_all_shots(problem["opponents"], problem["theta_step"], problem["goals"])
        self.interesting_points(problem["goals"], problem["radius"])
        self.dominant_value = pow(2, self.nb_shots + 1) - 1
        self.compute_all_positions(problem["bottom_left"], problem["top_right"], 
                                   problem["pos_step"], problem["radius"], problem["goals"])

    def compute_default_triangles(self, goal):
        triangles = []
        for opponent in self.opponents:
            triangles.append(ConvexShape.compute_triangle(opponent, goal))
        return triangles.copy()

    def compute_new_triangles(self, triangles, radius):
        new_triangles = []
        for triangle in triangles:
            new_triangles.append(ConvexShape.compute_bigger_triangle(triangle, radius))
        return new_triangles

    def point_in_triangles(self, point):
        tmp = []
        index = 0
        for triangle in self.triangles:
            if triangle.point_in(point):
                tmp.append(index)
            index += 1
        return tmp.copy()

    def interesting_points(self, goals, radius):
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
                    if self.exists_collision_opponents(defender, self.problem["radius"]):

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
                    self.max_deg = max(deg, self.max_deg)
                    self.deg.append(deg)
                
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

    def check_redundancy(self, def_list, new_def):
        index = 0
        to_delete = []
        for d in def_list:
            
            res = self.edges[new_def]

            index2 = 0
            for d2 in def_list:

                if d != d2 and index2 not in to_delete:
                    res = res | self.edges[d2]

                index2 += 1

            if (self.edges[d] | res) == res:
                to_delete.append(index)
            index += 1

        return to_delete.copy()


    def find_dominating_set(self, permutation, coloration=0):
        """
        This method should return a dominating set of G (not a minimum one though).
        """
        s = []
        p = []
        index = 0
        while coloration != self.dominant_value:

            if index == len(permutation):
                random.shuffle(permutation)
                index = 0
                s = []
                coloration = 0

            p_i = permutation[index]

            if not self.valid_defender(s, p_i):
                p.append(p_i)
                index += 1
                continue

            new_coloration = coloration | self.edges[p_i]
            if new_coloration != coloration:

                to_delete = self.check_redundancy(s, p_i)
                shift = 0
                for i in to_delete:
                    p.append(s[i - shift])
                    del s[i - shift]
                    shift += 1
                
                s.append(p_i)
                coloration = new_coloration
            else:
                p.append(p_i)
            index += 1

        p += permutation[index:]
        random.shuffle(p)
        return (s.copy(), (s + p).copy())

    def jump(self, n, p):
        tmp = p[n]
        for i in range(1, n):
            p[n - i - 1] = p[n - i - 2]
        p[0] = tmp

    def gen_perm(self, size):
        perm = []
        for i in range(size):
            perm.append(i)
        random.shuffle(perm)
        return perm.copy()

    def find_minimum_dominating_set(self, tries, i_m, prob, timeout, perm=None):
        init_tries = tries

        s = None
        p = perm

        ext = False

        i = 0
        i_max = i_m

        s_best = self.gen_perm(len(self.defenders))

        s_time = time.time()

        while tries > 0:
            if (ext == False and i > i_max) or ext or p == None:
                if random.uniform(0, 1) < prob and p != None:
                    s, p = self.find_dominating_set(p)
                    init_tries = tries
                else:
                    s, p = self.find_dominating_set(self.gen_perm(len(self.defenders)))

            self.jump(random.randint(1, len(self.defenders) - 1), p)
            s2, p2 = self.find_dominating_set(self.gen_perm(len(self.defenders)))

            i = i + 1 if len(s2) >= len(s) else 0
            if len(s2) <= len(s):
                p = p2.copy()
                s = s2.copy()
                if len(s_best) > len(s):
                    print(len(s))
                    i = 0
                    s_best = s.copy()
                    ext = True
                    tries = init_tries
                    prob = prob / 1.2
            
            if len(s2) >= len(s):
                i += 1

            tries -= 1

            if time.time() - s_time > timeout:
                break
   
        res = []
        for i in s_best:
            res.append(self.defenders[i])
        return res

