import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.Solvers.Solver import Solver


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
        
        :param max_uncovered: The index of the node with the greatest degree that has not 
        yet been added to the list of defenders.

        :param 
        """
        super.__init__(graph)
        self.max_uncovered = graph.max_deg_index
        self.max_current = 0
        self.compensation = int((self.graph.dominant_value + 1) / 2)
        self.max_index = len(self.graph.edges) - 1

    def remove_uncovered(self, index, def_list, edges):
        tmp_max_uncovered = 0
        val1 = edges[index]
        i = 0
        while i <= self.max_index:

            edges[i] = ((val1 ^ edges[i]) + self.compensation) & edges[i]

            if edges[i] == self.graph.dominant_value:
                edges[i] = edges[self.max_index]
                edges[self.max_index] = self.graph.dominant_value
                self.max_index -= 1
                continue

            count = bin(edges[i]).count('1')

            if count > self.max_current:
                tmp_max_uncovered = i
                self.max_current = count

            i += 1

        self.max_uncovered = tmp_max_uncovered

    def _solve(self, dom_val, def_list, edges, depth=0):
        depth = 0
        while depth < len(self.graph.defenders):
            if dom_val == self.graph.dominant_value:
                return def_list

            if not self.has_solution(edges, dom_val):
                return None

            if not self.graph.valid_defender(def_list, self.max_uncovered):
                edges[self.max_uncovered] = edges[self.max_index]
                edges[self.max_index] = self.graph.dominant_value
                self.max_index -= 1
                depth += 1
                continue

            def_list.append(self.max_uncovered)
            dom_val = dom_val | edges[self.max_uncovered]
            self.max_current = 0
            self.remove_uncovered(self.max_uncovered, def_list, edges)

            depth += 1

    def sum_all(self, index, def_list, edges):
        s = 0
        for j in range(len(def_list)):
            if j != index:
                s = s | edges[def_list[j]]
        return s

    def purge(self, def_list, edges):
        new_list = []
        changed = False
        for i in range(len(def_list)):
            s = self.sum_all(i, def_list, edges)
            d = edges[def_list[i]]


            if s | d != s :
                new_list.append(def_list[i])
            else:
                changed = True
        return (new_list.copy(), changed)

    def has_solution(self, edges, dom_val):
        s = dom_val
        for e in edges:
            s = s | e
        return s == self.graph.dominant_value

    def solve(self, params):
        if not self.has_solution(self.graph.edges, 0):
            return None
        edges = self.graph.edges.copy()
        res = self._solve(0, [], edges)
        changed = True
        if res == None:
            return res
        while changed:
            res, changed = self.purge(res, self.graph.edges)
        return self.graph.index_list_to_defenders(res)

    def sort(self, compare_func):
        arrays = [self.graph.deg, self.graph.defenders, self.graph.edges]
        self.graph.bubble_sort(arrays, compare_func)

    def print_b(self, val):
        print(str(bin(val))[2:])