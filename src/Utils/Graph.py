import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import math
from src.Utils.Point import Point
from src.Utils.UsefulTypes import Opponent, Shot, Defender
import time
"""
This module is used to simulate graphs.
Subject to a lot, lot of changes, yep.
"""

class Graph:

    """
    Graph encapsulates a broad definition of what is a graph. It is optimized to be used on this specific problem.
    It has therefore a lot of flaws as an actual Graph class. 

    If for some reason an other problem (other than dominant set) must be solved, maybe another class Graph will be
    added.
    """

    recursive_calls = 0

    def __init__(self):
        """
        Construct a new 'Graph' object.

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

        self.thread_end = False

    def copy(self):
        graph = Graph()

        graph.defenders = self.defenders.copy()
        graph.opponents = self.opponents.copy()
        graph.shots = self.shots.copy()
        graph.edges = self.edges.copy()
        graph.dominant_value = self.dominant_value

        graph.max_deg = self.max_deg
        graph.deg = self.deg.copy()
        graph.max_deg_after = self.max_deg_after.copy()
        graph.thread_end = False
        return graph

    def compute_all_shots(self, opponents, step, goal):
        """
        Computs all useful shots and adds them to the list of shots.

        - KEEPS shots aimed at at least one goal
        - Ideas?

        :param opponents: The list of opponents to consider the shots of.
        :param step: Used to compute a finite number of angles when considering an opponent.
        :param goal: The goal (or list later, I guess) to consider.
        :return: returns nothing.
        """

        # Parsing the opponents list
        for opponent in opponents:

            # Low bound for an angle
            angle = -math.pi

            # Parse all possible angle in [-pi ; pi[
            while angle < math.pi:

                # If this shot is valid (i.e: goes in the goal), it is added to the list of shots
                shot = Shot(opponent, angle)
                if goal.is_shot_valid(shot):
                    self.shots.append(shot)
                angle += step

    def exists_collision_opponents(self, defender):
        """
        Check if there exists a collision between at least one opponent and one defender.

        :param defender: The defender to check the collisions of.
        :return: True if at least one collision exists, False otherwise.
        """
        for opponent in self.opponents:
            if defender.collision(opponent):
                return True
        return False

    def compute_all_positions(self, bottom_left, top_right, step, radius, goal):
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

                # Current defender (if it were to be placed here)
                defender = Defender(Point(x, y), radius)
                deg = 0

                # If there is a collision, go to the next position
                if self.exists_collision_opponents(defender):

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
                for shot in self.shots:
                    if goal.shot_intercepted(defender, shot):
                            
                        # Shifting to the left (*2) and adding one to signify that
                        # an edge exists
                        edges = (edges << 1) + 1
                        deg += 1
                    else:
                        edges = edges << 1
                
                # If the result is not 1
                # The defender is added (because it isn't useless)
                if edges != (self.dominant_value + 1) / 2:
                    self.defenders.append(defender)
                    self.edges.append(edges)
                    self.max_deg = max(deg, self.max_deg)
                    self.deg.append(deg)
                
                y += step
            x += step

    def is_dominant_set(self, set_to_test):
        """
        Check if a given set is dominant. A set can be dominant if and only if there exists
        an edge going to every shot. This means that the disjunction of the selected edges
        is 2^n - 1 where n is the number of valid shot. (see above for a clearer explanation).

        :param set_to_test: The set that has to be checked to be dominant (or not).
        :return: True if the given set is dominant, False otherwise.
        """
        res = self.edges[set_to_test[0]]
        for i in range(0, len(set_to_test)):
            res = res | self.edges[set_to_test[i]]
            if res == self.dominant_value:
                return True
        return False

    def valid_defender(self, def_list, new_def):
        """
        Check if there exists a collision between a new defender and a list of pre existing defender.
        It only checks if the new defender creates a collision, elements of the list could have collision
        between them.

        :param def_list: The list of defenders to compare the defender to.
        :param new_def: The defender that shall not have collisions with defenders in the list.
        :return: True if there exists a collision, False otherwise.
        """
        for defender in def_list:
            if self.defenders[defender].collision(self.defenders[new_def]):
                return True
        return False

    def index_list_to_defenders(self, defenders):
        """
        Converts a list of indexes of the defender's list to actual defenders.

        :param defenders: The list of indexes to convert.
        :return: The converted list.
        """
        lst = []
        for defender in defenders:
            lst.append(self.defenders[defender])
        return lst.copy()

    def solve_(self, size, defenders_list=[], index=0, dominated_set=0, max_possible_deg=0):
        """
        Solves the problem recursively. It is a brute force algorithm with slight improvements.
        
        - If there is a collision with the current defender and a selected one, skip
        - If a solution is found, stop looking for new solutions
        - Ideas?

        It basically checks if every subset of the set of defender of size 'size' is a dominant
        set of the shot set.

        :param size: The size of the subset to find (faster, especially if you have an intuition or
        are looking for a specific kind of solution).
        
        :param defenders_list: The list of defenders that are selected at any given point. To be more
        specific it a list of indexes in the defenders set (faster). This list is empty by default so that 
        the initial call to the function is easy. This list could already contain elements if a solution
        with a (or multiple) specific defender is required.

        :param index: The index of the current defender we are checking.

        :return: None if there isn't any solution, the list of indexes otherwise.
        """

        # If there isn't any more defender to add and the size of the team is still
        # not valid, return None (obviously we don't go further as
        # there aren't any defender to add next)
        if index == len(self.defenders) and size != 0:
            return None

        # If the team is full, check if this is a dominant set, if so
        # return the list, otherwise return None (not going further because
        # we need to remove the last added defender, to add the next one)
        if size == 0:
            if dominated_set == self.dominant_value:
                return self.index_list_to_defenders(defenders_list)
            return None

        # If the team isn't full and there are defenders to add
        else:

            # While there are defenders to check
            # 1 -> Check if the current one has any collisions with previously added ones
            # if so, go to the next defender
            # 2 -> Add the current defender
            # 3 -> Check if with this defender there exists a solution by going to
            # the next step (where either the team is full, there are no next defender or
            # another defender gets added) see above for more explanation and keep in mind
            # this is recursive
            # 4 -> If there exists a solution, stop the recursion and return it
            # 5 -> remove the current defender and go to the next one
            while index < len(self.defenders):

                if (dominated_set | self.edges[index]) == dominated_set:
                    index += 1
                    continue

                # Collision detection
                if self.valid_defender(defenders_list, index):
                    index += 1
                    continue

                tmp_max_possible_deg = max_possible_deg + self.deg[index]
                if tmp_max_possible_deg + (size-1) * self.max_deg_after[index] < len(self.shots):
                    index += 1
                    continue

                tmp_dominant_set = dominated_set | self.edges[index]

                # New defender added and solution checking
                defenders_list.append(index)
                   
                res = self.solve_(size-1, defenders_list, index+1, tmp_dominant_set, tmp_max_possible_deg)

                # Remove current defender and go to the next one
                del defenders_list[-1]

                # End of recursion if there exists a solution
                if res != None:
                    return res

                index += 1

        # If the previous defender didn't yield any valid solution, return None
        return None

    def solve(self, size):
        # check before hand
        if self.max_deg * size < len(self.shots):
            print("Impossible! ", self.max_deg * size, " < ", len(self.shots))
            return None

        defenders_list = []

        return self.solve_(size, defenders_list, 0, 0, 0)
     
    def swap(self, arr, i, j):
        tmp = arr[i]
        arr[i] = arr[j]
        arr[j] = tmp

    def bubble_sort(self):
        for i in range(0, len(self.deg)):
            for j in range(0, len(self.deg) - i - 1):
                if self.deg[j] < self.deg[j+1]:
                    self.swap(self.deg, j, j+1)
                    self.swap(self.defenders, j, j+1)
                    self.swap(self.edges, j, j+1)

    def construct_deg(self, sort):
        # print(self.deg)
        if sort:
            self.bubble_sort()
        # print(self.deg)

        # to do in a separate place pls
        max_found = self.deg[len(self.deg) - 1]
        for i in range(0, len(self.deg)):
            max_found = max(self.deg[len(self.deg) - i - 1], max_found)
            self.max_deg_after.append(max_found)
        self.max_deg_after = self.max_deg_after[::-1]

        # print(len(self.defenders))
        # print(len(self.edges))
        # print(len(self.max_deg_after))
        # print(self.max_deg_after)

    def compute_graph(self, goal, pos_step, theta_step, opponents, bottom_left, top_right, radius):
        """
        Computes all the vertices and edges of the graph. The order of operation here is critical.
        For instance, dominant_values can only exist if the the set of shots is complete and 
        the computation of the positions is only possible with the set of shots and the 
        dominant value.

        Please improve the argument list, like ew. Create a class maybe?
        """
        self.opponents = opponents
        self.compute_all_shots(opponents, theta_step, goal)
        self.dominant_value = pow(2, len(self.shots) + 1) - 1
        self.compute_all_positions(bottom_left, top_right, pos_step, radius, goal)

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
