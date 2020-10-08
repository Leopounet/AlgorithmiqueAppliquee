import json

"""
Very simple module that converts a .json file into a dictionnary.
"""

def decode(file):
    """
    This function creates a dictionnary out of a given file thanks to pre-existing json functions.

    :param file: The file to decode.
    :return: The corresponding Python dictionnary or None if something went wrong (i.e: the given file
    is invalid).
    """
    result = None
    try:
        with open(file, "r") as f:
            result = json.load(f)
    except Exception as e:
        print(e)
        return None
    return result