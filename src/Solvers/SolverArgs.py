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
        Creates a list of new arguments. 

        :param compare_func: t
        """
        self.compare_func = None
        self.random_tries = None
        self.random_pgr = None
        self.random_i_max = None
        self.random_i_best = None
        self.random_prob = None
        self.random_timeout = None
        self.random_perm = None