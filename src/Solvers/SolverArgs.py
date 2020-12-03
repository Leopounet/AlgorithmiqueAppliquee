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
        self.random_i_m = None
        self.prob = None
        self.timeout = None
        self.perm = None