import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import math
import json
import random
from src.Problem.ProblemType import ProblemType
from src.Utils.Vector import Vector


def problem_generator(pb_type, name="auto_generated", opponents=None):
    """
    This function saves a random problem as json file. The saved file 
    will be located in src/dumps/.

    :param type: The type of problem, 'B' for Basic problem, 'MD' for Minimum Distance, 
    'IP' for Initial Positions, 'GK' for Goal Keeper, 'MG' for MultiGoal (default: 'B').

    :return: returns nothing.
    """

    # generates a generic base for a problem
    tmp = {}
    tmp["field_limits"] = [ [-4.5,4.5],[-3,3] ]
    tmp["goals"] = [
            {
                    "posts" : [[4.5, -0.5], [4.5,0.5]],
                    "direction" : [-1,0]
            }
        ]
    tmp["opponents"] = []
    tmp["robot_radius"] = 0.09
    tmp["theta_step"] = 0.031416
    tmp["pos_step"] = 0.1

    # generates a random number of opponents if it was not specified
    rng = opponents
    if rng == None:
        rng = random.randint(3, 8)

    # generates random positions for the opponents
    while len(tmp["opponents"]) < rng:
        x = random.uniform(tmp["field_limits"][0][0],tmp["field_limits"][0][1])
        y = random.uniform(tmp["field_limits"][1][0],tmp["field_limits"][1][1])
        if [x,y] not in tmp["opponents"]:
            tmp["opponents"].append([x,y].copy())


    # Minimum distance: generates a random minimum distance between radius and 2 * radius
    if pb_type == ProblemType.MIN_DIST:
        tmp["min_dist"] = random.uniform(tmp["robot_radius"], tmp["robot_radius"] * 2)


    # Initial Positions: generate as many random initial defender positions as number of opponents
    # it does not account for collisions but this fine (it is an abstraction of reality which accounts
    # for more than necessary possibilities)
    if pb_type == ProblemType.INITIAL_POS:
        tmp["defenders"] = []
        while len(tmp["defenders"]) < rng :
            x = random.uniform(tmp["field_limits"][0][0],tmp["field_limits"][0][1])
            y = random.uniform(tmp["field_limits"][1][0],tmp["field_limits"][1][1])
            if [x,y] not in tmp["defenders"] :
                tmp["defenders"].append([x,y].copy())


    # Goalkeeper area: ??
    if pb_type == ProblemType.GOAL_KEEPER:
        tmp["goalkeeper_area"] = []
        t = [(tmp["goals"][0]["posts"][0][0]+tmp["goals"][0]["posts"][1][0])/2,(tmp["goals"][0]["posts"][0][1]+tmp["goals"][0]["posts"][1][1])/2]
        x = tmp["goals"][0]["direction"][0]*random.gammavariate(2,abs(t[1]-tmp["goals"][0]["posts"][1][1]))
        y = random.gammavariate(2,abs(t[1]-tmp["goals"][0]["posts"][1][1]))
        tmp["goalkeeper_area"].append([min(t[0]+x,t[0]),max(t[0]+x,t[0])].copy())
        tmp["goalkeeper_area"].append([t[1]-y,t[1]+y].copy())


    # Multigoal: generates between 1 and 4 additional goals
    if pb_type == ProblemType.MULTI_GOAL:
        raise "Faulty implementation in the ssl viewer, these can not be verified for now"
        # tmp["goals"] = []
        # rng = random.randint(1, 4)
        # while len(tmp["goals"]) < rng :
        #     x_1 = random.uniform(tmp["field_limits"][0][0],tmp["field_limits"][0][1])
        #     y_1 = random.uniform(tmp["field_limits"][1][0],tmp["field_limits"][1][1])
        #     x_2 = random.uniform(tmp["field_limits"][0][0],tmp["field_limits"][0][1])
        #     y_2 = random.uniform(tmp["field_limits"][1][0],tmp["field_limits"][1][1])

        #     direction_x = -x_2 + x_1
        #     direction_y = -y_2 + y_1

        #     if random.randint(0, 1) == 0:
        #         direction_x *= -1
        #         direction_y *= -1
            
        #     tmp["goals"].append({
        #             "posts" : [[x_1,y_1],[x_2,y_2]].copy(),
        #             "direction" : [direction_x, direction_y]
        #     })


    with open(name + '_problem.json', 'w') as f:
        json.dump(tmp, f)