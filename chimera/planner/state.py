"""

__author__ = "Md Mazharul Islam Rakeb"
__email__ = "mislam7@uncc.edu"
__date__ = 5/13/20

"""
from pprint import pprint

# from networkx_helper import get_shortest_path, get_all_path
from chimera.planner.networkx_helper import get_all_path, get_shortest_path


class State:
    def __init__(self, name=None):
        self.attack_propagation_probability = {}
        self.action = []
        self.name = name
        self.neighbours = []
        # self.data_exfiltration_probability = 0.00
        self.max_depth = 0.00

    def set_neighbour(self, next_state):
        self.neighbours.append(next_state)

    def set_action(self, action):
        self.action.append(action)

    def set_attack_propagation_probability(self, next_state, attack_propagation_probability):
        self.attack_propagation_probability[next_state] = attack_propagation_probability

    def get_attack_propagation_probability(self, next_state):
        return self.attack_propagation_probability[
            next_state] if next_state in self.attack_propagation_probability else 0.0

    def __str__(self):
        return self.name


def generate_states_tree(all_states, attack_propagation, attack_to_deceive_states, data_exfiltration_probability):
    states_objects = {}
    for i, state_name in enumerate(all_states):
        state = State(state_name)
        states_objects[state_name] = state
        state.data_exfiltration_probability = float(data_exfiltration_probability[i])

        if state_name in attack_propagation:
            found_state = attack_propagation[state_name]
            for next_state, attack_propagation_probability in found_state.items():
                state.set_neighbour(next_state)
                state.set_attack_propagation_probability(next_state, attack_propagation_probability)

    # TODO if we want to solve the honey-honey or honey-attack state transition problem, we need to create another JSON
    # file to take input as attack_propagation. In that case, we can merge the we have two options:
    # 1. comment the following codes and merge the new JSON file with the attack_propagation file (recommend)
    # 2. write new for loops to set honey attack propagation probabilities

    for attack_state, honey_states in attack_to_deceive_states.items():
        for neighbour_of_attack_state in states_objects[attack_state].neighbours:
            prob = states_objects[attack_state].get_attack_propagation_probability(neighbour_of_attack_state)
            neighbour_honey_states = attack_to_deceive_states[
                neighbour_of_attack_state] if neighbour_of_attack_state in attack_to_deceive_states else []
            for current_honey in honey_states:
                current_honey_state = states_objects[current_honey]
                for next_honey in neighbour_honey_states:
                    current_honey_state.set_neighbour(next_honey)
                    current_honey_state.set_attack_propagation_probability(next_honey, prob)

    return states_objects


def get_attack_propagation_prob(G, param, param1):
    pass


def get_exfiltration_prob_from_path_list(G, path_list, honey_state):
    grand_p = 0
    for path in path_list:
        pair_list = [(x, y) for x, y in zip(path[:-1], path[1:])]
        total_p = 1
        for pair in pair_list:
            p = get_attack_propagation_prob(G, pair[0], pair[1])
            if p == 0:
                total_p = 0
                break
            else:
                if pair[0] in honey_state and pair[1] in honey_state:
                    p = 1 - p
            total_p *= p
        grand_p += total_p
    return grand_p


def generate_states_exfiltration_probability(G, honey_states, destination_state):
    states_objects = {}
    for state_name in list(G.nodes):
        state = State(state_name)
        states_objects[state_name] = state
        path_list = get_shortest_path(G, state_name, destination_state)
        p = get_exfiltration_prob_from_path_list(G, path_list, honey_states)
        state.data_exfiltration_probability = p

    return states_objects


def get_longest_depth(path_list):
    return max([len(d) for d in path_list], default=0)


def generate_states_longest_depth(G, destination_state):
    states_objects = {}
    for state_name in list(G.nodes):
        state = State(state_name)
        states_objects[state_name] = state
        path_list = get_all_path(G, state_name, destination_state)
        d = get_longest_depth(path_list)
        state.max_depth = d

    return states_objects
