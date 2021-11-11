"""

__author__ = "Md Mazharul Islam Rakeb"
__email__ = "mislam7@uncc.edu"
__date__ = 4/25/21

"""
from collections import OrderedDict
from pprint import pprint

import networkx as nx
from pyvis.network import Network

# from state import State
from chimera.planner.state import State


class Agent:
    DECEPTION_GOALS = {'diversion', 'distortion', 'depletion', 'discovery'}

    def __init__(self, deception_graph_json=None, deception_actions_json=None, attack_action_prediction_json=None,
                 honey_states=None, attacker_goal_state=None, defender_goal_state=None, shared_states=None,
                 deception_goal=None, real_states=None):
        self.deception_graph_json = deception_graph_json
        self.deception_actions_json = deception_actions_json
        self.attack_action_prediction_json = attack_action_prediction_json
        self.honey_states = honey_states
        self.attacker_goal_state = attacker_goal_state
        self.defender_goal_state = defender_goal_state
        self.shared_states = shared_states
        self.goal = deception_goal
        self.obs_matrix = None
        self.real_state = real_states

        self.dg = nx.MultiDiGraph()
        self.create_deception_graph()

        self.state_space = OrderedDict({state: State() for state in self.dg.nodes()})
        self.observation_space = self.state_space

        self.d_action_space = OrderedDict(deception_actions_json)

        # for k in self.dg.neighbors('Honey_Data_Staged'):
        #     for _, v in self.dg.get_edge_data('Honey_Data_Staged', k).items():
        #         print(('Honey_Data_Staged', k), v)
        #
        # print()
        # print()
        # s = 'Honey_Software_Discovery'
        # for k in self.dg.neighbors(s):
        #     for _, v in self.dg.get_edge_data(s, k).items():
        #         print((s, k), v)
        # exit(1)

    def create_deception_graph(self):
        """
        "Phishing_Spearphishing_Attachment": {
            "doNothing,execute": {
              "next_state": "User_Execution_Malicious_File"
            },
            "migrateInHE,execute": {
              "next_state": "User_Execution_in_HE"
            }
          },
        """

        for current_state, neighbor in self.deception_graph_json.items():
            for action_pair, attr in neighbor.items():
                deception_action, attack_action = action_pair.replace(' ', '').split(',')
                next_state = attr['next_state']
                # attack_propagation_probability = None
                # if (current_state in self.honey_states and next_state in self.honey_states) or (
                #         current_state not in self.honey_states and next_state not in self.honey_states):
                attack_propagation_probability = self.attack_action_prediction_json[current_state][attack_action][
                    'probability']
                self.dg.add_edge(current_state, next_state, deception_action=deception_action,
                                 attack_action=attack_action, app=attack_propagation_probability)

        # print(self.dg.edges(data=True))
        # for i, v in enumerate(self.dg.nodes(data=False)):
        #     print(i + 1, v)

    def visualize_graph(self, f_name='deception_graph_visualization.html'):
        # nt = Network('500px', '500px')
        nt = Network(height='1500px', width='2000px', directed=True)
        # populates the nodes and edges data structures

        nt.from_nx(self.dg)
        nt.set_edge_smooth('dynamic')

        # nt.enable_physics(True)
        nt.show_buttons(filter_=['physics', 'edges'])
        # nt.show_buttons(filter_=['edges', 'physics'])
        nt.show(f_name)
