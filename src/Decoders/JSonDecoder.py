import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import math
from src.ProblemUtils.ProblemType import ProblemType
from src.Utils.Point import Point
from src.Utils.Vector import Vector
from src.Utils.UsefulTypes import Goal, Opponent, Shot, Defender

import json

"""
Very simple module that converts a .json file into a dictionnary.
"""

def decode(file):
    """
    This function creates a dictionnary out of a given file thanks to pre-existing json functions. 
    
    :param file: The file to decode. 
    :return: The corresponding Python dictionnary or None if something went wrong (i.e: the given file \
    is invalid).
    """
    # Json to dictionnary
    tmp_res = None
    try:
        with open(file, "r") as f:
            tmp_res = json.load(f)
    except Exception as e:
        print(e)
        return None

    # Gets the type of problem handled here
    problem_type = ProblemType.identify_problem(tmp_res)
    res = {}

    # Gets the field's limits + the bottom left and top right points of the field
    res["field_limits"] = tmp_res["field_limits"]
    res["bottom_left"] = Point(res["field_limits"][0][0], res["field_limits"][1][0])
    res["top_right"] = Point(res["field_limits"][0][1], res["field_limits"][1][1])

    # Gets the list of goals
    res["goals"] = []
    for goal in tmp_res["goals"]:
        posts = goal["posts"]
        direction = goal["direction"]

        post1 = Point(posts[0][0], posts[0][1])
        post2 = Point(posts[1][0], posts[1][1])
        direction = Vector(direction[0], -direction[1])
        goal = Goal(post1, post2, direction)
        res["goals"].append(goal)

    # Gets the list of opponents
    res["opponents"] = []
    for opponent in tmp_res["opponents"]:
        res["opponents"].append(Opponent(Point(opponent[0], opponent[1])))

    # Gets the radius of the robots
    res["radius"] = tmp_res["robot_radius"]

    # Gets theta and pos steps for opponents' shots and defenders's position respectively
    res["theta_step"] = tmp_res["theta_step"]
    res["pos_step"] = tmp_res["pos_step"]

    # Gets the list of defenders if the problem is initial positions
    if problem_type == ProblemType.INITIAL_POS:
        res["defenders"] = []
        for defender in tmp_res["defenders"]:
            res["defenders"].append(Defender(Point(defender[0], defender[1]), res["radius"]))

    # Gets the min dist if the problem is min dist
    if problem_type == ProblemType.MIN_DIST:
        res["min_dist"] = tmp_res["min_dist"]

    # Gets the goalkeeper area if the problem is goal keeper
    if problem_type == ProblemType.GOAL_KEEPER:
        res["goalkeeper_area"] = tmp_res["goalkeeper_area"]
        res["gk_bottom_left"] = Point(res["goalkeeper_area"][0][0], res["goalkeeper_area"][1][0])
        res["gk_top_right"] = Point(res["goalkeeper_area"][0][1], res["goalkeeper_area"][1][1])

    if problem_type == ProblemType.MAX_SPEED:
        res["ball_max_speed"] = tmp_res["ball_max_speed"]
        res["robot_max_speed"] = tmp_res["robot_max_speed"]

    return (res, problem_type)

def save_json(defenders, name="data.json"):
    """
    This function saves the given results (list of defenders) as json file. The saved file 
    will be located in src/dumps/.

    :param defenders: The list of defenders to save (default: data.json).
    :param name (opt): The name of the file.
    :return: returns nothing.
    """
    data = {}
    data["defenders"] = []

    # Write the results
    for r in defenders:
        data["defenders"].append([r.pos.x, r.pos.y])

    with open(name, 'w') as f:
        json.dump(data, f)