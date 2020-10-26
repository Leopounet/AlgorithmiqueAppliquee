import numpy as np
import json
import random

print("B : Basic problem")
print("MD : Minimum Distance")
print("IP : Initial Positions")
print("GK : Goal Keeper")
print("MG : MultiGoal")
type = input("Enter extension type : ")


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

rng = random.randint(3,6)

while len(tmp["opponents"]) < rng :
    x = random.uniform(tmp["field_limits"][0][0],tmp["field_limits"][0][1])
    y = random.uniform(tmp["field_limits"][1][0],tmp["field_limits"][1][1])
    if [x,y] not in sampl :
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
        if [x,y] not in sampl :
            tmp["defenders"].append([x,y].copy())


# Goalkeeper area

if type == 'GK' :
    tmp["goalkeeper_area"] = []


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
    
        
#else :
#    tmp["goals"] = [
#                {
#                    "posts" : [[4.5, -0.5], [4.5,0.5]],
#                    "direction" : [-1,0]
#                }
#            ]


with open('dumps/examples/problems/'+ type + '_problem.json', 'w') as f:
        json.dump(tmp, f)
