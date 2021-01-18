"""
Lists all the possible arguments a solver could use. This is very useful
to make compact code while remaining clean.
"""

class SolverArgs:

    """
    Lists all the possible arguments a solver could use. This is very useful
    to make compact code while remaining clean.
    """

    def __init__(self):
        """
        Creates a list of new arguments. In parenthesis, which solver(s) this variable
        is applicable to.

        :ivar compare_func: (ALL) This function, if set, is used to sort the defenders
        in the graph according to their degrees with the specific function. Basically,
        this function is used to determine if there is no sorting, a increasing sorting
        or a decreasing sorting.

        :ivar random_tries: (RANDOM) The number of tries before stopping the algorithm. That is,
        the number of dominating set generated.

        :ivar random_i_max: (RANDOM) The maximum number of tries without finding any better set before
        shuffling the permutation entirely.

        :ivar random_prob: (RANDOM) This is the probability of shuffling the permutation entirely. Check
        the RandomSolver.py file for more information about this.

        :ivar random_timeout: (RANDOM) The maximum amount of time this solver can spend on finding a 
        minimum dominating set (in seconds).

        :ivar random_perm: (RANDOM) The initial permutation to use (can be lest to None).

        :ivar greedy_random: (GREEDY) If the greedy algorithm does not find a solution 
        eventhough there exists one, the random solver will be used to find one instead.
        """
        self.compare_func = None
        self.random_tries = None
        self.random_i_max = None
        self.random_prob = None
        self.random_timeout = None
        self.random_perm = None
        self.greedy_random = False