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

initial_pos_keys_set = basic_keys_set.copy()
initial_pos_keys_set.add("defenders")

min_dist_keys_set = basic_keys_set.copy()
min_dist_keys_set.add("min_dist")

class Problemtype(Enum):
    BASIC = "Basic Problem"
    MIN_DIST = "Minimal Distance"
    GOAL_KEEPER = "Goal Keeper"
    MULTI_GOAL = "Multi Goal"
    INITIAL_POS = "Initial Positions"
    CURVED_TRAJECTORIES = "Curved Trajectories"
    UNDEFINED = "UNDEFINED"

    @classmethod
    def identifyProblem(self, problem):
        keys = problem.get_key_list()

        # There should not be any duplicated fields so converting to a set should be fine
        keys_set = set(keys)

        # Is it basic or multi goal?
        if keys_set == basic_keys_set:

            # Is it multi goal?
            if len(problem.get_input_from_key("goals")) > 1:
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

        return self.UNDEFINED