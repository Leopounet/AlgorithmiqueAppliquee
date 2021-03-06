import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from enum import Enum

basic_keys_set = {
    "field_limits",
    "goals",
    "opponents",
    "robot_radius",
    "theta_step",
    "pos_step"
}

goal_keeper_keys_set = basic_keys_set.copy()
goal_keeper_keys_set.add("goalkeeper_area")

# adding junk because otherwise in the enumeration, the values are the same
# although this actually wouldn't change anything (multigoal
# and basic problems are litterally treated the same way)
multi_goal_keys_set = basic_keys_set.copy()
multi_goal_keys_set.add("junk")

initial_pos_keys_set = basic_keys_set.copy()
initial_pos_keys_set.add("defenders")

min_dist_keys_set = basic_keys_set.copy()
min_dist_keys_set.add("min_dist")

max_speed_keys_set = basic_keys_set.copy()
max_speed_keys_set.add("ball_max_speed")
max_speed_keys_set.add("robot_max_speed")

class ProblemType(Enum):
    BASIC = basic_keys_set
    MIN_DIST = {}
    GOAL_KEEPER = goal_keeper_keys_set
    MULTI_GOAL = multi_goal_keys_set
    INITIAL_POS = initial_pos_keys_set
    CURVED_TRAJECTORIES = min_dist_keys_set
    MAX_SPEED = max_speed_keys_set
    UNDEFINED = {}

    @classmethod
    def get_key_set(self, problem_type):
        return problem_type.value

    @classmethod
    def identify_problem(self, problem):
        """
        Given a problem, returns the extension. 

        :param problem: The problem to find the extension of. 
            
        :return: The type of problem it is.
        """
        keys = problem.keys()

        # There should not be any duplicated fields so converting to a set should be fine
        keys_set = set(keys)

        # Is it basic or multi goal?
        if keys_set == basic_keys_set:

            # Is it multi goal?
            if len(problem["goals"]) > 1:
                return self.MULTI_GOAL
            return self.BASIC

        # Is it goal keeper?
        if keys_set == goal_keeper_keys_set: 
            return self.GOAL_KEEPER

        # Is it initial pos?
        if keys_set == initial_pos_keys_set:
            return self.INITIAL_POS

        # Is it min dist?
        if keys_set == min_dist_keys_set:
            return self.MIN_DIST

        # Is it max speed?
        if keys_set == max_speed_keys_set:
            return self.MAX_SPEED

        return self.UNDEFINED