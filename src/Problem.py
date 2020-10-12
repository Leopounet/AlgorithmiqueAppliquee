import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import math
from src.ProblemType import ProblemType

"""
This module is used to store inputs of the problem in a standardized manner. 
Every possible variants of the problem could be simulated with this class.
"""

class Problem:

    """
    Inputs encapsulates every possible set of inputs for the problem.
    """
    def __init__(self, decoding_function):
        """
        Construct a new 'Inputs' object.

        :param decoding_function: The function to use to decode the given file (should be different depending on its format).
        To add a decoding function, create a decoding file in the Decoders directory. Add the decoding function you would like to
        use and then pass this function as an argument when creating a Decoder object. 

        Note: All decoding function must take a file as an argument and return a dictionnary.
        :return: returns nothing
        """

        # This member is a function, it should take a file as an argument
        self.decoding_function = decoding_function

        # Dictionnary used to store all types of inputs
        # The reason why a dict. is used here is that it can be easily modified between two different instances of the
        # problem (even if they have different inputs set)
        #
        # Either: delete every unused key when possible
        # Or: Store None whenever a key is unused
        # Always: Add new keys when needed (keys names will probably be taken from the input file) 
        self.inputs = {}

        # The type of problem
        self.type = ProblemType.UNDEFINED

    def __getitem__(self, key):
        """
        Allows to type p[key] where p is a 'Problem' object and key is a valid key of 
        the inputs dictionnary.

        :param key: A valid key in inputs.
        :return: The corresponding value to key in inputs, if the key is not valid, returns None.
        """
        if key not in self.inputs:
            return None
        return self.inputs[key]

    def __str__(self):
        """
        Allows the use of print(p) where p is a 'Problem' object.

        :return: The corresponding string.
        """
        res = ""
        for i in self.inputs:
            if isinstance(self.inputs[i], list):
                res += i + ": "
                spaces = ""
                first = True
                for _ in range(len(i) + 2):
                    spaces += " "

                for e in self.inputs[i]:
                    if not first:
                        res += spaces
                    first = False
                    res += str(e) + " "
                    res += "\n"
            else:
                res += i + ": " + str(self.inputs[i])
            res += "\n"
        res = res[:-1]
        return res

    def decode(self, file):
        """
        Decodes the given file and stores its result in the corresponding member. 
        It deletes any previously stored result.

        :param file: The file to decode (currently supported: JSon)
        :return: Returns the resulting 'Input' object (or None if something went wrong)
        """
        res = self.decoding_function(file)
        if res != None:
            self.inputs = res[0]
            self.type = res[1]

    def add_input(self, key, value=None):
        """
        Adds a new valid key to the inputs dictionnary.
        If the key is already in the dictionnary, the previous value is replaced with the new given value.

        :param key: The new key to add.
        :param value: The default value assigned to the key (default: None)
        :return: returns nothing
        """
        self.inputs[key] = value

    def get_input_from_key(self, key):
        """
        Finds an element in the inputs dictionnary using the given key.
        Should we throw an error if something goes horribly wrong? (the key is not valid) or return None? Might be confusing?

        :param key: The key of the element to get
        :return: The corresponding element if the key is valid, something else or an error otherwise
        """
        if key in self.inputs:
            return self.inputs[key]
        return None

    def get_key_list(self):
        """
        Returns all the available keys in the dictionnary.

        :return: All the available keys in the dictionnary.
        """
        return list(self.inputs.keys())