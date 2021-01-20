import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.Solvers.Solver import Solver

"""
BruteForce solver for a given problem.
"""

class BruteForceSolver(Solver):

    """
    BruteForce solver for a given problem.
    """

    def __init__(self, graph):
        """
        Creates a new BruteForceSolver object.

        :param graph: The graph the solver will have to find a minimum dominating set in.
        """
        super().__init__(graph)

    def solve_(self, size, defenders_list=[], index=0, dominant_value=0, max_possible_deg=0):
        """
        Solves the problem recursively. It is a brute force algorithm with slight improvements. 

        - If there is a collision with the current defender and a selected one, skip 
        - If a solution is found, stop looking for new solutions 

        It basically checks if every subset of the set of defender of size 'size' is a dominant 
        set of the shot set. 

        :param size: The size of the subset to find (faster, especially if you have an intuition or \
        are looking for a specific kind of solution). 

        :param defenders_list: The list of defenders that are selected at any given point. To be more \
        specific it a list of indexes in the defenders set (faster). This list is empty by default so that \
        the initial call to the function is easy. This list could already contain elements if a solution \
        with a (or multiple) specific defender is required. 

        :param index: The index of the current defender we are checking. 

        :param dominant_value: This value corresponds to the current domination value of the current defender \
        set. This value is equal to the dominant value of the given graph once a solution is found. Find more \
        information in Utils/Graph.py. 

        :param max_possible_deg: The maximum possible total degree of all the selected nodes w.r.t the maximum \
        size of the set. For example, if the set of defender is [10, 16, 25] and the maximum size of the set \
        is n, then this variable will be equal to: \
        deg(def10) + deg(def16) + def(def25) + (n - 3) * max_deg(graph) 

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
            if dominant_value == self.graph.dominant_value:
                return defenders_list.copy()
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

                if (dominant_value | self.graph.edges[index]) == dominant_value:
                    index += 1
                    continue
 
                # Collision detection (should be done an other way preferably
                # for this is not so efficient)
                if not self.graph.valid_defender(defenders_list, index):
                    index += 1
                    continue

                # this is a check about the possibility of finding a solution with the current
                # dominating set
                #
                # say you have a set of size a <= k where k is the maximum size allowed for the set
                # if the total degree of the set is smaller than (k - a) * DELTA(G) then
                # there are no possible solution (see solve method for more info)
                #
                # this could largely be enhanced by computing the new DELTA(G) after adding a defender
                # which can lower over time (since we don't choose twice the same defender)
                tmp_max_possible_deg = max_possible_deg + self.graph.deg[index]
                if (index < len(self.graph.defenders) - 1 and
                    tmp_max_possible_deg + (size-1) * self.graph.deg[index + 1] < self.graph.nb_shots):
                    index += 1
                    continue

                # compute the dominating value of the current set
                tmp_dominant_value = dominant_value | self.graph.edges[index]

                # New defender added and solution checking
                defenders_list.append(index)
                   
                res = self.solve_(size-1, defenders_list, index+1, tmp_dominant_value, tmp_max_possible_deg)

                # Remove current defender and go to the next one
                del defenders_list[-1]

                # End of recursion if there exists a solution
                if res != None:
                    return res

                index += 1

        # If the previous defender didn't yield any valid solution, return None
        return None

    def solve(self, params):
        """
        Tries to find a minimum dominating set for the given graph. If one is found,
        it has to be a minimum one. This algorithm has an exponential complexity. 

        :param params: A SolverArgs object storing different values to modify the behavior of \
        the solving algorithm. 

        :return: a list of defender that is a dominating set, None otherwise.
        """
        
        # sorts the list of defenders given a compare func
        self.sort(params.compare_func)

        res = None

        # iterative search for a minimum dominating set
        for i in range(1, len(self.graph.opponents) + 10):

            # if a solution of this size is impossible, go to the next step
            # here, if DELTA(G) * i < nb_shots then there are no solution
            # it is quite easy to see, blocking n shots <=> delta(v) = n
            # therefore blocking nb_shots shots requires to have a dominating set
            # that a total degree at least nb_shots
            if self.graph.max_deg * i < self.graph.nb_shots:
                continue
            
            # try to solve for this size of dominating set
            res = self.solve_(i, [], 0, 0, 0)

            # if a valid result has been found, return it
            if res != None:
                break
        return self.graph.index_list_to_defenders(res) if res != None else res

    def sort(self, compare_func):
        """
        Sorts the arrays defined below w.r.t the first array of the list.
        The sort is a bubble sort for now, but the time it takes is low compared
        to the time it takes the solver to solve the problem. 

        :param compare_func: The function used to sort the first array 
            
        :return: nothing
        """
        arrays = [self.graph.deg, self.graph.defenders, self.graph.edges]
        self.graph.bubble_sort(arrays, compare_func)