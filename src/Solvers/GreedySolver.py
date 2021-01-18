import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.Solvers.Solver import Solver
from src.Solvers.RandomSolver import RandomSolver
from src.Solvers.SolverArgs import SolverArgs


"""
Greedy solver for a given problem.
"""

class GreedySolver(Solver):

    """
    Greedy solver for a given problem.
    """


    def __init__(self, graph):
        """
        Creates a new GreedySolver object. Note that this solver never branches
        (it has a single recursive call, see method solve) therefore storing data
        globally for each individual object, instead of giving them as arguments of 
        the solve method when called recursively, is fine. 

        :param graph: The graph that is going to be used to solve the problem. 
        """
        super().__init__(graph)

        # the index of the node with the greatest degree that has not been selected yet
        self.max_uncovered = graph.max_deg_index

        # the index of the current maximum index
        self.max_current = 0

        # used to fix the dominant value when manipulated
        # since some value is xor-ed with another one
        # the first bit (which is always 1) will become a 0
        # changing the whole meaning of the bitwise representation
        # find more info in Graph.py
        self.compensation = int((self.graph.dominant_value + 1) // 2)

        # the maximum index possible
        self.max_index = len(self.graph.edges) - 1

    def remove_neighbors(self, index, edges):
        """
        Removes all the blocked shots from the graph.

        Let's say we have three defenders (one per line) and three shots 
        (columns), the first bits of each line is just a away to make sure
        the bitwise representation is the same length: 

        | 1 1 0 1 
        | 1 1 1 0 
        | 1 1 0 0 

        Here, the first defender for example blocks shots 1 and 3. The algorithm
        chooses the defender with the greatest degree, here the first or second.
        Say it chooses the first one, then shots 1 and 3 are blocked so the matrice
        must change accordingly:

        | 1 0 0 0
        | 1 0 1 0
        | 1 0 0 0

        This what this method does. This is achieved by xor-ing the ith line with
        the first one, adding a compensation (see above) and and-ing the result with the
        previous value of the ith line (this obviously will be more convincing with examples),
        here for example to obtain the result of the second line:

        | 1: xor-ing 1 1 0 1 ^ 1 1 1 0 -> 0 0 1 1
        | 2: compensate 1 0 0 0 + 0 0 1 1 -> 1 0 1 1
        | 3: and-ing 1 0 1 1 & 1 1 1 0 -> 1 0 1 0

        The idea is that in the first step, all the common blocked shot between the selected
        defender and the ith position are removed from the ith position. But this can add
        some shots to the ith position that were not blocked before. To prevent that from
        happening, the and-ing is used, so that only shots that were already blocked by the ith
        defender remain blocked.

        :param def_list: The list of defenders.

        :param edges: The matrix of defenders x shots.
        """

        # the value of the removed defender
        val1 = edges[index]

        # iterate through every defender that still block at least one shot
        i = 0
        while i <= self.max_index:

            # the computation described above
            edges[i] = ((val1 ^ edges[i]) + self.compensation) & edges[i]

            # getting the degree (the number of 1 in the bitwise representation)
            # of the current defender
            count = bin(edges[i]).count('1')

            # if the degree is greater then the max found so far, store it
            if count > self.max_current:
                self.max_uncovered = i
                self.max_current = count

            i += 1

    def solve_(self, dom_val, def_list, edges, depth=0):
        """
        This method implements a simple greedy solver, it just adds 
        the node with the greatest degree, then removes every blocked
        shots by this defender from the graph, therefore reducing the 
        degree of every defender blocking at least one of these shots.

        It stops once a dominating set is found, there is no guarantee
        about the size of this dominating set, but experimental results 
        showed that it is generally acceptable (w.r.t the size of the 
        minimum dominating set), on reasonable instances it generates
        a set at most two times bigger than the optimal one. Its time
        complexity is trivially O(n * m), n being the order of the graph
        and m the number of edges (removing a node requires to change
        every affected node's degree).

        This algorithm is not guaranteed to return a valid solution. If 
        there are no solution, obviously, but also if the selected nodes
        actually leads a configuration in which no solution exist anymore,
        this can happen because of the collision between defenders, for 
        example.

        :param dom_val: The dominant value of the current defender set. \
        this value represents how many different shots have been blocked. \
        If the set is [1001, 1101] then the dominant value is 1101. \
        The set dominates the graph when the dominant value has a bitwise \
        representation made of only 1s.

        :param def_list: The list of selected defenders.

        :param edges: The edges of the graph that are being modified when \
        shots are removed.

        :param depth: The current index in the list of defenders.

        :return: A set of defenders that dominate the graph, None if no \
        such set have been found.
        """

        # while there are still some defenders available
        # try to find a dominant set
        depth = 0
        while depth < len(self.graph.defenders):

            # if the current set is dominant, return it
            if dom_val == self.graph.dominant_value:
                return def_list

            # if the last selected defender leads to a configuration
            # where no solution can be found, abort
            if not self.has_solution(edges, dom_val):
                return None

            # if the current defender with maximum degree is not valid,
            # for example colliding with another defender, skip
            if not self.graph.valid_defender(def_list, self.max_uncovered):
                depth += 1
                continue

            # add the current defender with the greatest degree and modify the
            # dominant value accordingly
            def_list.append(self.max_uncovered)
            dom_val = dom_val | edges[self.max_uncovered]

            # remove all the blocked shots from the graph
            self.max_current = 0
            self.remove_neighbors(self.max_uncovered, edges)

            depth += 1

    def get_dominant_value_without(self, index, def_list, edges):
        """
        Returns the dominant value of the given set without one specified
        defender (used to check if this defender is useful, if the dominant 
        value does not change when this defender is removed, then the defender
        is useless).

        :param index: The index of the defender being tested for removal.

        :param def_list: The list of defenders.

        :param edges: The list of blocked shots per defenders.

        :return: The dominant value of the defender's set without the specified defender.
        """
        s = 0
        for j in range(len(def_list)):
            if j != index:
                s = s | edges[def_list[j]]
        return s

    def purge(self, def_list, edges):
        """
        Remove potential useless selected defenders from the defender list.
        A useless defender is a defender that does not block at least
        one shot that no other defender blocks.

        :param def_list: The list of defenders to purge.

        :param edges: The list of blocked shots per defenders.

        :return: A new array without useles defenders and a boolean \
        indicating if the list has been modified.
        """

        # the list to return
        new_list = []

        # true if at least one defender has been removed
        changed = False
        for i in range(len(def_list)):

            # if the list has already been changed do not try to
            # purge more (because the removed one is still considered
            # part of the array, can lead to incoherence)
            if changed:
                new_list.append(def_list[i])

            # get the dominating value of the set without the ith defender
            s = self.get_dominant_value_without(i, def_list, edges)

            # get the blocked shots by the ith defender
            d = edges[def_list[i]]

            # if the defender blocks at least one shot not blocked by any
            # other defender, add it to the new list, otherwise skip
            if s | d != s :
                new_list.append(def_list[i])
            else:
                changed = True
        return (new_list.copy(), changed)

    def has_solution(self, edges, dom_val):
        """
        Checks if given a edges, it is possible to block
        every single shot (no isolated node). This is done by
        checking that the dominating value of all defenders is equal
        to the expected dominating value of the graph.

        :param edges: The edges of the graph to consider.

        :param dom_val: The initial dominating value (1000...).

        :return: True if there exists at least one dominating set in the graph.
        """
        s = dom_val
        for e in edges:
            s = s | e
        return s == self.graph.dominant_value

    def solve(self, params):
        """
        Tries to find a minimum dominating set for the given graph using
        a greedy algorithm. The algorithm is described within the 
        :func:`~src.Solvers.GreedySolver.GreedySolver.solve_` method.

        :param params: A list of parameters to use for this algorithm. \
        More info in :class:`~src.Solvers.SolverArgs`.

        :return: A list of defenders dominating the graph, or None if none \
        exist/could be found.
        """

        # if there are no solution at all, we can stop here
        if not self.has_solution(self.graph.edges, 0):
            return None

        # creates a copy of the edges of the graph because they
        # are going to be modified
        edges = self.graph.edges.copy()

        # solve for the given graph
        res = self.solve_(0, [], edges)

        # it is possible that tis solver does not find a solution, eventhough
        # there is one (or multiple)
        # in this case, we can use the random solver to dramatically
        # increase the chances of finding a solution
        # this can be disabled
        if res == None:
            
            # if we definitely want a solution
            if params.greedy_random:
                # create a random solver with default arguments
                random_args = SolverArgs()
                random_args.compare_func = lambda x, y : x < y
                random_args.random_tries = 1000
                random_args.random_i_max = 78
                random_args.random_prob = 0.6
                random_args.random_timeout = 0.5

                # solve with random solver
                solver = RandomSolver(self.graph)
                return solver.solve(random_args)
            return None

        # if a solution has been found, it is possible that some node
        # are actually useless wrt the other nodes
        # in this case, we remove the useless nodes 
        changed = True
        while changed:
            res, changed = self.purge(res, self.graph.edges)

        # return the list of defenders
        return self.graph.index_list_to_defenders(res)

    def sort(self, compare_func):
        """
        Sorts the graph's defenders according to their degrees.

        :param compare_func: Used to know how to compare degrees.
        """
        arrays = [self.graph.deg, self.graph.defenders, self.graph.edges]
        self.graph.bubble_sort(arrays, compare_func)

    def print_b(self, val):
        """
        Prints the bitwise representation of a value.

        :param val: The value to represent.
        """
        print(str(bin(val))[2:])