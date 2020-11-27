import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.Solvers.Solver import Solver

"""
This module is used to simulate graphs.
Subject to a lot, lot of changes, yep.
"""

class BruteForceSolver(Solver):

    """
    Graph encapsulates a broad definition of what is a graph. It is optimized to be used on this specific problem.
    It has therefore a lot of flaws as an actual Graph class. 

    If for some reason an other problem (other than dominant set) must be solved, maybe another class Graph will be
    added.
    """

    def __init__(self, graph):
        super().__init__(graph)

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
        if index == len(self.graph.defenders) and size != 0:
            return None

        # If the team is full, check if this is a dominant set, if so
        # return the list, otherwise return None (not going further because
        # we need to remove the last added defender, to add the next one)
        if size == 0:
            if dominated_set == self.graph.dominant_value:
                return self.graph.index_list_to_defenders(defenders_list)
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
            while index < len(self.graph.defenders):

                if (dominated_set | self.graph.edges[index]) == dominated_set:
                    index += 1
                    continue
 
                # Collision detection
                if not self.graph.valid_defender(defenders_list, index):
                    index += 1
                    continue

                tmp_max_possible_deg = max_possible_deg + self.graph.deg[index]
                if tmp_max_possible_deg + (size-1) * self.graph.max_deg_after[index] < self.graph.nb_shots:
                    index += 1
                    continue

                tmp_dominant_set = dominated_set | self.graph.edges[index]

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

    def solve(self, params):
        if params.compare_func != None:
            self.sort(params.compare_func)
        self.construct_deg()

        res = None
        for i in range(1, len(self.graph.opponents) * 2):
            # check before hand
            if self.graph.max_deg * i < self.graph.nb_shots:
                continue

            res = self.solve_(i, [], 0, 0, 0)
            if res != None:
                break
        return res

    def construct_deg(self):
        # to do in a separate place pls
        max_found = self.graph.deg[len(self.graph.deg) - 1]
        for i in range(0, len(self.graph.deg)):
            max_found = max(self.graph.deg[len(self.graph.deg) - i - 1], max_found)
            self.graph.max_deg_after.append(max_found)
        self.graph.max_deg_after = self.graph.max_deg_after[::-1]

    def sort(self, compare_func):
        arrays = [self.graph.deg, self.graph.defenders, self.graph.edges]
        self.graph.bubble_sort(arrays, compare_func)