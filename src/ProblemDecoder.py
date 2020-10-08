import Inputs

"""
This module is used to decode the given problems. 
See examples here: https://github.com/medrimonia/ssl_defender_viewer
"""

class Decoder:

    """
    Decoder is used to decode an input problem and store the important values in dedicated members.
    """
    def __init__(self, decoding_function):
        """
        Construct a new 'Decoder' object.

        :param decoding_function: The function to use to decode the given file (should be different depending on its format).
        To add a decoding function, create a decoding file in the Decoders directory. Add the decoding function you would like to
        use and then pass this function as an argument when creating a Decoder object. 

        Note: All decoding function must take a file as an argument and return a dictionnary.
        :return: returns nothing
        """

        # This member is a function, it should take a file as an argument
        self.decoding_function = decoding_function

        # Used to store the result of the decoding function
        # The output should be standardized (not thought about yet)
        self.result = Inputs.Inputs()

    def decode(self, file):
        """
        Decodes the given file and stores its result in the corresponding member. 
        It deletes any previously stored result.

        :param file: The file to decode (currently supported: JSon)
        :return: Returns the resulting 'Input' object (or None if something went wrong)
        """
        output = self.decoding_function(file)
        self.result.set_entire_dictionnary(output) 
