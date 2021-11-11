"""

__author__ = "Md Mazharul Islam Rakeb"
__email__ = "mislam7@uncc.edu"
__date__ = 5/16/20

"""


# normalized
def create_all_observation_normalized(agent, plan_file_name):
    all_states = agent.state_space.keys()
    observations = agent.observation_space.keys()
    with open(plan_file_name, 'a') as f:
        f.write("\nO:*\n")
    obs_matrix = []
    for a in all_states:
        current_row = []
        for o in observations:
            normalized_value = 0.2 / (len(observations) - 1)
            with open(plan_file_name, 'a') as f:
                if a == o:
                    f.write("0.80 ")
                    current_row.append(0.80)
                else:
                    f.write("%.6f " % normalized_value)
                    current_row.append(normalized_value)
        obs_matrix.append(current_row)
        with open(plan_file_name, 'a') as f:
            f.write("\n")
    agent.obs_matrix = obs_matrix
    return obs_matrix


def create_all_observation_mdp(all_states, observations, plan_file_name):
    with open(plan_file_name, 'a') as f:
        f.write("\nO:*\n")
    obs_matrix = []
    for a in all_states:
        current_row = []
        for o in observations:
            with open(plan_file_name, 'a') as f:
                if a == o:
                    f.write("1.0 ")
                    current_row.append(1.0)
                else:
                    f.write("0.0 ")
                    current_row.append(0.0)
        obs_matrix.append(current_row)
        with open(plan_file_name, 'a') as f:
            f.write("\n")
    return obs_matrix
