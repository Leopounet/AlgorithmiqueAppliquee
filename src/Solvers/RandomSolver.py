import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.Solvers.Solver import Solver

import random
import time

class RandomSolver(Solver):

    """
    This class represents a random solver (order-based solver
    as describe in "An Order-based Algorithm for Minimum Dominating 
    Set with Application in Graph Mining" by David Chalupa).
    """

    def __init__(self, graph):
        """
        Creates a new RandomSolver object.

        :param graph: The graph to find a dominating set in.
        """
        super().__init__(graph)

        # used to fix the dominant value when manipulated
        # since some value is xor-ed with another one
        # the first bit (which is always 1) will become a 0
        # changing the whole meaning of the bitwise representation
        # find more info in Graph.py
        self.compensation = int((self.graph.dominant_value + 1) // 2)

    def solve(self, params):
        """
        Tries to find a minimum dominating set in the graph within a specified 
        delay. The algorithm is described in :func:`~src.Solvers.RandomSolver.RandomSolver.solve_`. 

        :param params: A SolverArgs object storing different values to modify the behavior of \
        the solving algorithm.

        :return: A list of defenders dominating the set, if there exists one has been \
        found, None otherwise.
        """

        # if the compare_function is defined, sort the graph with it
        if params.compare_func != None:
            self.sort(params.compare_func)

        res = self.solve_(params.random_tries,
                          params.random_i_max,
                          params.random_prob,
                          params.random_timeout, 
                          params.random_perm)

        return self.graph.index_list_to_defenders(res)

    def solve_(self, tries, i_m, prob, timeout, perm=None):
        """
        Taken from `Chalupa, D. (2018). An order-based algorithm for minimum dominating set with 
        application in graph mining. Information Sciences, 426, 101-116. <https://arxiv.org/pdf/1705.00318.pdf>`_

        Tries to find a minimum dominating thanks to the algorithm developped by
        David Chalupa. The idea of the algorithm is as follows: first, check every
        nodes sequentially until a dominant set is formed. Remove one of
        these nodes and mix all the not selected nodes with the ejected one.
        Then repeat the algorithm. There are two part of the algorithm in which
        randomness is involved, first when the nodes are mixed, second, randomly
        every nodes will be mixed up (normally the nodes of the previous dominating 
        set, except one, are not mixed up).

        :param tries: The maximum number of tries without finding a better solution. \
        Once this value is exceed, the algorithm terminates, this is used to stop if \
        a potential optimal solution has been found.

        :param i_max: The maximum number of allowed iteration without finding a better \
        solution.

        :param prob: Probability to randomize the first permutation right of the bat.

        :param timeout: The maximum delay allowed without finding a better solution \
        than the previous best dominant set.

        :param opt perm: The initial permutation to use.

        :return: The minimum dominating set of defenders found before exiting.
        """

        # set the number of tries
        init_tries = tries

        # these two variables are the partition described above 
        # defenders = s@p
        s = None
        p = perm

        # true whenever a new best dominating set is found
        ext = False

        # current iteration
        i = 0

        # the maximum number of iteration without a new best set
        # before shuffling all the defenders
        i_max = i_m

        # default permutation (not random)
        init = []
        for i in range(len(self.graph.defenders)):
            init.append(i)

        # start the time to know when to end
        s_time = time.time()

        # use the greedy algorithm to find a first valid solution
        s_best, perm = self.greedy_algorithm(init, s_time, timeout)

        # as long as we allow more tries
        while tries > 0:
            
            # there is always a random chance to shuffle all the defenders entirely
            # here if the first if condition is satisfied, then there is a probability
            # 1 - prob that the whole thing is shuffled
            if (ext == False and i > i_max) or ext or p == None:
                if random.uniform(0, 1) < prob and p != None:
                    s, p = self.greedy_algorithm(p, s_time, timeout)
                    init_tries = tries
                else:
                    s, p = self.greedy_algorithm(self.gen_perm(len(self.graph.defenders)), s_time, timeout)

            # s can equal none here iff the time allocated has been exceeded
            if s == None:
                break
            
            # perform a jump as described above
            self.jump(random.randint(1, len(self.graph.defenders) - 1), p)

            # find a new solution after the jump
            s2, p2 = self.greedy_algorithm(p, s_time, timeout)
            
            # s can equal none here iff the time allocated has been exceeded
            if s2 == None:
                break
            
            # increase i if not better solution has been found
            i = i + 1 if len(s2) >= len(s) else 0

            # if a better solution has been found, update the best solution since last
            # reset
            if len(s2) <= len(s):
                p = p2.copy()
                s = s2.copy()

                # if this is the best solution ever, update everything
                # (these values below were chosen after experimenting a bit)
                if len(s_best) > len(s):
                    i = 0
                    s_best = s.copy()
                    ext = True
                    tries = init_tries
                    prob = prob / 1.2
                    i_m = i_m * 1.2

            # whatever happened, there is now one try less
            tries -= 1

            # break if the time has been exceeded
            if time.time() - s_time > timeout:
                break
   
        return s_best

    def greedy_algorithm(self, permutation, s_time, timeout, coloration=0):
        """
        This method should return a dominating set of G (not a minimum one though). It finds
        it by sequentially reading the list of defenders in the given permutation, it adds
        any new defender that is not 100% useless (blocks no new shots) and that does not 
        colide with a previously chosen defender.

        :param permutation: The current permutation to consider.
        
        :param s_time: When did the whole algorithm start.

        :param timeout: The time limit to not exceed.
        
        :param coloration: The dominant value of the current chosen set.
        """

        # those variables represent the partition of the defenders
        # s@p = defenders (but shuffled)
        s = []
        p = []

        # current iteration
        index = 0

        # while the current set is not dominant
        while coloration != self.graph.dominant_value:
            
            # if no time is left, leave
            if time.time() - s_time > timeout:
                return (None, None)

            # if no more defender exists, then the current permutation has no
            # valid solution, so shuffle everything and start again
            if index == len(permutation):
                random.shuffle(permutation)
                index = 0
                s = []
                coloration = 0

            # get the current defender
            p_i = permutation[index]

            # if it collides with a previous defender, go to the next one
            if not self.graph.valid_defender(s, p_i):
                p.append(p_i)
                index += 1
                continue
            
            # compute the new dominant value of this set with the new node
            new_coloration = coloration | self.graph.edges[p_i]

            # if the new value is better, add this defender, and check if any other
            # previously added defender becomes obsolete
            if new_coloration != coloration:
                
                # computes all the redundant defenders, wrt the new one
                to_delete = self.check_redundancy(s, p_i)

                # delete every redundant defender
                shift = 0
                for i in to_delete:
                    p.append(s[i - shift])
                    del s[i - shift]
                    shift += 1
                
                # add the defender to the dominating set and update the dominant value
                s.append(p_i)
                coloration = new_coloration

            # otherwise, do not add it
            else:
                p.append(p_i)
            index += 1

        # shuffle the defenders not chose
        p += permutation[index:]
        random.shuffle(p)
        return (s.copy(), (s + p).copy())

    def check_redundancy(self, def_list, new_def):
        """
        Creates a list of all the redundant vertices, that is the vertices
        that do not block an element not blocked by any other vertex.

        :param def_list: The list of the current dominating set.

        :param new_def: The element to add to this list.
        """

        index = 0
        to_delete = []

        # go through the current dominating set (may be partial)
        # d will be considered removed from the set, the idea is to check
        # if removing d leads to finding a better set
        for d in def_list:
            
            # get the dominating value of the new element
            res = self.graph.edges[new_def]

            index2 = 0

            # get the dominating value of the set without d of the set
            for d2 in def_list:
                if d != d2 and index2 not in to_delete:
                    res = res | self.graph.edges[d2]
                index2 += 1

            # here res is the dominating value of the set of defender minus d but
            # with the new element
            # if adding d doesn't change anything, d is useless
            if (self.graph.edges[d] | res) == res:
                to_delete.append(index)
            index += 1

        return to_delete.copy()

    def jump(self, n, p):
        """
        Moves an element from the permutation to the front of it.

        :param n: The index of the element to move to the front.

        :param p: The permutation to modify.
        """
        tmp = p[n]
        for i in range(1, n):
            p[n - i - 1] = p[n - i - 2]
        p[0] = tmp

    def gen_perm(self, size):
        """
        Generates a permutation of the numbers 1 to size.

        :param size: The greatest integer of the permutation.

        :return: A permutation of the numbers 1 to size.
        """
        perm = list(range(0, size))
        random.shuffle(perm)
        return perm.copy()

    def in_array(self, f, el):
        """
        Checks if a given element is in an array.

        :param f: The array.

        :param el: The element.

        :return: True if the element is in the array, False otherwise.
        """
        return el in f

    def all_in(self, d, f):
        """
        Checks if all the elements of the first array are in the second array.

        :param d: The first array.

        :param f: The second array.

        :return: True if all the elements of d are in f, False otherwise.
        """
        for i in d:
            if not self.in_array(f, i):
                return False
        return True

    def sort(self, compare_func):
        """
        Sorts the graph's defenders according to their degrees.

        :param compare_func: Used to know how to compare degrees.
        """
        arrays = [self.graph.deg, self.graph.defenders, self.graph.edges]
        self.graph.bubble_sort(arrays, compare_func)