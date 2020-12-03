"""
This class is just the generic representation of a Solver. It clearly has
no use as such but allows for a simple documentation.
"""

class Solver:

    """
    This class is a solver. Given a graph, it will try to find a minimum
    dominating set. It might not succeed in doing so. Some solver might
    return an approximated solution, while others will try to find
    an optimal solution even if the search lasts for hours, days, years... 

    The given graph must be a graph from the class Graph.py, which is a special
    representation of graphs (more info in Graph.py). 

    There are two main methods, solve and sort. The first one is self explanatory, the 
    second one is used to sort the nodes of the graph given one characteristic, the
    degree for example. All of this is specific to each solver, but most solvers will
    sort multiple arrays at once given a compare function and a reference array. This
    is done because different arrays of the graph are linked (for example the index i of 
    array A, specifically corresponds to the index i of array B). This could be solved by
    adding some classes, for now this isn not solved. 
    """

    def __init__(self, graph):
        """
        Creates a new Solver object. 

        :param graph: The graph to find the minimum dominating set in.
        """
        self.graph = graph

    def solve(self):
        """
        Returns a minimum dominating set (or an approximation) of the graph given to the solver. 

        :return: A list of Defender object.
        """
        raise NotImplementedError("solve method has not been implemented!")

    def sort(self, compare_func):
        """
        Sorts somme array in the graph (or in the solver if applicable). 

        :param compare_func: The comparing function to use (lambda function).
        """
        raise NotImplementedError("sort method has not been implemented!")