import numpy as np
import json
import random

def problem_generator(type, opponents=None):
    """
    This function saves a random problem as json file. The saved file 
    will be located in src/dumps/examples/problems.

    :param type: The type of problem, 'B' for Basic problem, 'MD' for Minimum Distance, 'IP' for Initial Positions, 'GK' for Goal Keeper, 'MG' for MultiGoal (default: 'B').
    :return: returns nothing.
    """

#print("B : Basic problem")
#print("MD : Minimum Distance")
#print("IP : Initial Positions")
#print("GK : Goal Keeper")
#print("MG : MultiGoal")
#type = input("Enter extension type : ")


# Basic Problem : generate between 3 and 6 random opponents

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

    rng = 0
    if opponents == None:
        rng = random.randint(3, 8)
    else:
        rng = random.randint(opponents, opponents)

    while len(tmp["opponents"]) < rng :
        x = random.uniform(tmp["field_limits"][0][0],tmp["field_limits"][0][1])
        y = random.uniform(tmp["field_limits"][1][0],tmp["field_limits"][1][1])
        if [x,y] not in tmp["opponents"] :
            tmp["opponents"].append([x,y].copy())


# Minimum distance

    if type == 'MD' :
        tmp["min_dist"] = input("Enter minimum distance between robots : ")


# Initial Positions : generate as many random initial defender positions as number of opponents

    if type == 'IP' :
        tmp["defenders"] = []
        while len(tmp["defenders"]) < rng :
            x = random.uniform(tmp["field_limits"][0][0],tmp["field_limits"][0][1])
            y = random.uniform(tmp["field_limits"][1][0],tmp["field_limits"][1][1])
            if [x,y] not in tmp["defenders"] :
                tmp["defenders"].append([x,y].copy())


# Goalkeeper area

    if type == 'GK' :
        tmp["goalkeeper_area"] = []
        t = [(tmp["goals"][0]["posts"][0][0]+tmp["goals"][0]["posts"][1][0])/2,(tmp["goals"][0]["posts"][0][1]+tmp["goals"][0]["posts"][1][1])/2]
        x = tmp["goals"][0]["direction"][0]*random.gammavariate(2,abs(t[1]-tmp["goals"][0]["posts"][1][1]))
        y = random.gammavariate(2,abs(t[1]-tmp["goals"][0]["posts"][1][1]))
        tmp["goalkeeper_area"].append([min(t[0]+x,t[0]),max(t[0]+x,t[0])].copy())
        tmp["goalkeeper_area"].append([t[1]-y,t[1]+y].copy())


# Multigoal

    if type == 'MG' :
        tmp["goals"] = []
        rng = int(input("Enter number of goals : "))
        while len(tmp["goals"]) < rng :
            x_1 = random.uniform(tmp["field_limits"][0][0],tmp["field_limits"][0][1])
            y_1 = random.uniform(tmp["field_limits"][1][0],tmp["field_limits"][1][1])
            x_2 = random.uniform(tmp["field_limits"][0][0],tmp["field_limits"][0][1])
            y_2 = random.uniform(tmp["field_limits"][1][0],tmp["field_limits"][1][1])
            direction = np.random.randint(-1,1,2)
            tmp["goals"].append({
                    "posts" : [[x_1,y_1],[x_2,y_2]].copy(),
                    "direction" : direction.copy()
                    })


    with open('dumps/'+ type + '_problem.json', 'w') as f:
            json.dump(tmp, f)

# Problem incompatibilities :
        # GK and MG incompatible