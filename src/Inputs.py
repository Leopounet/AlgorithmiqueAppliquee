"""
This module is used to store inputs of the problem in a standardized manner. 
Every possible variants of the problem could be simulated with this class.
"""

class Inputs:

    """
    Inputs encapsulates every possible set of inputs for the problem.
    """
    def __init__(self):
        """
        Construct a new 'Inputs' object.

        :return: returns nothing
        """

        # Dictionnary used to store all types of inputs
        # The reason why a dict. is used here is that it can be easily modified between two different instances of the
        # problem (even if they have different inputs set)
        #
        # Either: delete every unused key when possible
        # Or: Store None whenever a key is unused
        # Always: Add new keys when needed (keys names will probably be taken from the input file) 
        self.inputs = {}

    def add_input(self, key, value=None):
        """
        Adds a new valid key to the inputs dictionnary.
        If the key is already in the dictionnary, the previous value is replaced with the new given value.

        :param key: The new key to add.
        :param value: The default value assigned to the key (default: None)
        :return: returns nothing
        """
        self.inputs[key] = value

    def get_input(self, key):
        """
        Finds an element in the inputs dictionnary using the given key.
        Should we throw an error if something goes horribly wrong? (the key is not valid) or return None? Might be confusing?

        :param key: The key of the element to get
        :return: The corresponding element if the key is valid, something else or an error otherwise
        """
        if key in self.inputs:
            return self.inputs[key]
        return None