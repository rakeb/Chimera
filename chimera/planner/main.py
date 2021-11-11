"""
__author__ = "Md Mazharul Islam Rakeb"
__email__ = "mislam7@uncc.edu"
__date__ = 5/11/20
"""
import datetime
import json
import os
import pickle
import secrets
import statistics

# from belief import update_belief, generate_initial_belief
# from networkx_helper import get_all_path, Graph
# from observation import create_all_observation_normalized
# from parse_policy import find_optimal_action
# from pomdp_planner.config_util import config_section_map
# from reward import calculate_reward
# from transition import generate_transition, state_transition

from chimera.planner.agent import Agent
from chimera.planner.belief import update_belief, generate_initial_belief
from chimera.planner.config_util import config_section_map
from chimera.planner.networkx_helper import get_all_path
from chimera.planner.observation import create_all_observation_normalized
from chimera.planner.parse_policy import find_optimal_action
from chimera.planner.reward import calculate_reward
from chimera.planner.transition import state_transition
from chimeraweb.settings import BASE_DIR

APP_DIR = os.path.join(BASE_DIR, 'chimera/planner')

CONF_DIR = os.path.join(APP_DIR, 'paper_graph')
pomdp_file_name = os.path.join(APP_DIR, 'deception_plan.pomdp')
ZMDP_FILE = os.path.join(APP_DIR, 'zmdp-master/bin/darwin18/zmdp')
PLAN_FILE = os.path.join(CONF_DIR, pomdp_file_name)

belief, recommended_action = None, None


def load_json_data(path):
    with open(path) as f:
        data = json.load(f)
    return data


def generate_pomdp_file_skeleton(agent, discount, values):
    with open(PLAN_FILE, 'w') as f:
        f.writelines("discount: {}\n".format(discount))
        f.writelines("values: {}\n".format(values))
        f.write("states: ")
        for s in agent.state_space.keys():
            f.write("{} ".format(s))
        f.write("\n")

        f.write("actions: ")
        for a in agent.d_action_space.keys():
            f.write("{} ".format(a))
        f.write("\n")

        f.write("observations: ")
        for o in agent.observation_space.keys():
            f.write("{} ".format(o))
        f.write("\n\n")

        f.write("start: uniform\n")
        # f.write("\n")


def solve_zmdp():
    # global plan_file_name
    a = datetime.datetime.now()
    os.system(ZMDP_FILE + " solve " + PLAN_FILE)
    b = datetime.datetime.now()
    c = b - a
    return c
    # print("solve time: {} microseconds".format(c.microseconds))


def create_pomdp_agent():
    # global state_space, d_action_space, observation_space, obs_matrix, plan_file_name, deception_actions_obj, attack_graph

    conf = config_section_map(CONF_DIR)
    discount = conf['discount']
    values = conf['values']
    penalty = int(conf['penalty'])
    goal = conf['goal']
    goal = [int(i) for i in goal]
    attacker_goal_state = conf['attacker_goal_state'][0]
    defender_goal_state = conf['defender_goal_state'][0]
    quit_state = conf['quit_state'][0]

    real_states = conf['real_states']
    honey_states = set(conf['honey_states'])
    shared_states = set(conf['shared_states'])

    deception_graph_json = load_json_data(os.path.join(CONF_DIR, conf['deception_graph'][0]))
    deception_actions_json = load_json_data(os.path.join(CONF_DIR, conf['deception_actions'][0]))
    attack_action_prediction_json = load_json_data(os.path.join(CONF_DIR, conf['attack_action_prediction'][0]))
    deception_goal = {'diversion': 1, 'distortion': 0, 'depletion': 0, 'discovery': 1}
    agent = Agent(deception_actions_json=deception_actions_json, deception_graph_json=deception_graph_json,
                  attack_action_prediction_json=attack_action_prediction_json, honey_states=honey_states,
                  attacker_goal_state=attacker_goal_state, defender_goal_state=defender_goal_state,
                  shared_states=shared_states, deception_goal=deception_goal, real_states=real_states)

    generate_pomdp_file_skeleton(agent=agent, discount=discount, values=values)
    state_transition(agent=agent, plan_file=PLAN_FILE)
    create_all_observation_normalized(agent=agent, plan_file_name=PLAN_FILE)

    calculate_reward(agent=agent, I=100, P=10, plan_file_name=PLAN_FILE)

    return agent


def optimal_action(belief, agent):
    # global state_space, all_actions, observation_space, obs_matrix, d_action_space

    recommended_action_index = find_optimal_action(belief, 'out.policy')
    recommended_action = list(agent.d_action_space.keys())[recommended_action_index]
    return recommended_action


def generate_updated_belief(belief, recommended_action, current_observation_state, agent):
    # global state_space, observation_space, obs_matrix, deception_actions_obj

    transition_matrix = agent.deception_actions_json[recommended_action]['transition_matrix']
    observation_space = state_space = list(agent.state_space.keys())

    next_belief = update_belief(state_space, current_observation_state, agent.obs_matrix, observation_space,
                                transition_matrix, belief)
    return next_belief


def generate_mdp_belief(all_states, current_state):
    belief = {}
    for state in all_states:
        belief[state] = 1 if state == current_state else 0
    return belief


def recommend_action(current_observation_state, agent):
    global belief, recommended_action
    if not belief:
        belief = generate_initial_belief(agent.state_space.keys())
    if not recommended_action:
        recommended_action = optimal_action(belief, agent)
    belief = generate_updated_belief(belief, recommended_action, current_observation_state, agent)
    recommended_action = optimal_action(belief, agent)
    return recommended_action


if __name__ == '__main__':
    # y = input("Solve? press 'y': ")
    print("Generation POMDP model...")
    agent = create_pomdp_agent()
    print("POMDP model generation complete")
    #
    solve_time = []

    if not os.path.isfile('all_attack_scenario.pickle'):
        all_attack_scenario = get_all_path(agent.dg, "Phishing_Spearphishing_Attachment", agent.attacker_goal_state)
        with open('all_attack_scenario.pickle', 'wb') as handle:
            pickle.dump(all_attack_scenario, handle, protocol=pickle.HIGHEST_PROTOCOL)
    else:
        with open('all_attack_scenario.pickle', 'rb') as handle:
            all_attack_scenario = pickle.load(handle)

    print(len(all_attack_scenario))
    # exit(1)
    all_pomdp_defense_actions = []
    for attack_scenario in all_attack_scenario:
        belief = generate_initial_belief(agent.state_space.keys())
        recommended_action = optimal_action(belief)
        pomdp_recommended_actions = []
        optimal_action_selection_time = []
        for current_observation_state in attack_scenario:
            # print(current_observation_state)
            a = datetime.datetime.now()
            belief = generate_updated_belief(belief, recommended_action, current_observation_state)
            recommended_action = optimal_action(belief)
            pomdp_recommended_actions.append(recommended_action)

            b = datetime.datetime.now()

            c = b - a
            optimal_action_selection_time.append(c.microseconds)
        print("attack_scenario: {}".format(attack_scenario))
        print("pomdp_recommended_actions: {}".format(pomdp_recommended_actions))
        print("optimal_action_selection_time: {}".format(optimal_action_selection_time))

        # print(statistics.mean(optimal_action_selection_time))

        all_pomdp_defense_actions.append(pomdp_recommended_actions)
    # print(all_attack_scenario)
    # print(all_pomdp_defense_actions)
