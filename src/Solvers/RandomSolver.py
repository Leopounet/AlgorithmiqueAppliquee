import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.Solvers.Solver import Solver

import random
import time

"""
This modules is used to represent a graph for this specific problem, so 
it may be esoteric.
"""

class RandomSolver(Solver):

    """
    This class represents a graph.
    """

    def __init__(self, graph):
        super().__init__(graph)

    def solve(self, tries, i_m, prob, timeout, perm=None, compare_func=None):
        if compare_func != None:
            self.sort(compare_func)
        return self.find_minimum_dominating_set(tries, i_m, prob, timeout, perm)

    def check_redundancy(self, def_list, new_def):
        index = 0
        to_delete = []
        for d in def_list:
            
            res = self.graph.edges[new_def]

            index2 = 0
            for d2 in def_list:

                if d != d2 and index2 not in to_delete:
                    res = res | self.graph.edges[d2]

                index2 += 1

            if (self.graph.edges[d] | res) == res:
                to_delete.append(index)
            index += 1

        return to_delete.copy()


    def find_dominating_set(self, permutation, s_time, timeout, coloration=0):
        """
        This method should return a dominating set of G (not a minimum one though).
        """
        s = []
        p = []
        index = 0

        while coloration != self.graph.dominant_value:

            if time.time() - s_time > timeout:
                return (None, None)

            if index == len(permutation):
                random.shuffle(permutation)
                index = 0
                s = []
                coloration = 0

            p_i = permutation[index]

            if not self.graph.valid_defender(s, p_i):
                p.append(p_i)
                index += 1
                continue

            new_coloration = coloration | self.graph.edges[p_i]
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

        init = []
        for i in range(len(self.graph.defenders)):
            init.append(i)

        s_time = time.time()

        s_best, perm = self.find_dominating_set(init, s_time, timeout)

        while tries > 0:
            
            if (ext == False and i > i_max) or ext or p == None:
                if random.uniform(0, 1) < prob and p != None:
                    s, p = self.find_dominating_set(p, s_time, timeout)
                    init_tries = tries
                else:
                    s, p = self.find_dominating_set(self.gen_perm(len(self.graph.defenders)), s_time, timeout)

            if s == None:
                break

            self.jump(random.randint(1, len(self.graph.defenders) - 1), p)
            s2, p2 = self.find_dominating_set(p, s_time, timeout)

            if s2 == None:
                break

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
                    i_m = i_m * 1.2
            
            if len(s2) >= len(s):
                i += 1

            tries -= 1

            if time.time() - s_time > timeout:
                break
   
        res = []
        for i in s_best:
            res.append(self.graph.defenders[i])
        return res

    def connected(self, d, u):
        res = 0
        for i in d:
            if i != u:
                res = self.graph.edges[i] | res

        return res == self.graph.dominant_value

    def in_array(self, f, el):
        for i in f:
            if el == i:
                return True
        return False

    def all_in(self, d, f):
        for i in d:
            if not self.in_array(f, i):
                return False
        return True

    def sort(self, compare_func):
        arrays = [self.graph.deg, self.graph.defenders, self.graph.edges]
        self.graph.bubble_sort(arrays, compare_func)
