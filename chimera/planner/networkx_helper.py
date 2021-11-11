"""

__author__ = "Md Mazharul Islam Rakeb"
__email__ = "mislam7@uncc.edu"
__date__ = 7/30/20

"""
import json
import traceback
from pprint import pprint

import networkx as nx

from chimera.planner.config_util import config_section_map


class Graph:
    def __init__(self, graph_json):
        self.g = nx.DiGraph()
        self.graph_json = graph_json
        self.edge_set = None
        self.generate_graph()
        self.node_state = {}

    def generate_graph(self):
        for current_state, neighbour_list in self.graph_json.items():
            probability = 1 / len(neighbour_list)
            for item in neighbour_list:
                next_state = item['destination_node']
                attack_action = item['attack_action']
                self.g.add_edge(current_state, next_state, probability=probability, attack_action=attack_action)
        self.edge_set = set(self.g.edges)

    def get_attack_propagation_prob(self, current_node, next_node):
        prob = self.g.get_edge_data(current_node, next_node)
        return prob['probability'] if prob else 0.0

    def get_attack_action(self, current_node, next_node):
        attack_action = self.g.get_edge_data(current_node, next_node)
        return attack_action['attack_action'] if attack_action else ""

    def set_node_attributes(self, t):
        for n in self.g.nodes:
            res = [p for p in nx.all_shortest_paths(self.g, source=n, target=t)]
            shortest_path = res[0]
            l = len(shortest_path)
            risk = 1
            for i in range(l - 1):
                risk *= self.get_attack_propagation_prob(shortest_path[i], shortest_path[i + 1])
            attrb = {
                'depth': l,
                'risk': risk,
                's_path': shortest_path
            }
            self.node_state[n] = attrb


def load_json_data(path):
    with open(path) as f:
        data = json.load(f)
    return data


# def get_attack_propagation_prob(G, current_node, next_node):
#     prob = G.get_edge_data(current_node, next_node, default=0.0)
#
#     if type(prob) is float:
#         return prob
#     else:
#         return prob['weight']


# def generate_attack_graph(deception_graph_json):
#     graph = nx.DiGraph()
#
#     for current_state, neighbour_list in deception_graph_json.items():
#         probability = 1 / len(neighbour_list)
#         for item in neighbour_list:
#             next_state = item['destination_node']
#             attack_action = item['destination_node']
#             graph.add_edge(current_state, next_state, probability=probability, attack_action=attack_action)
#
#     e_list = [e for e in graph.edges]
#     edges = set(graph.edges)
#
#     print(len(e_list), e_list)
#     print(len(edges), edges)
#     return graph


def generate_attack_chain_graph(attack_propagation):
    G = nx.DiGraph()

    for state_name, neighbour_dict in attack_propagation.items():
        for next_state, propagation_probability in neighbour_dict.items():
            G.add_edge(state_name, next_state, weight=propagation_probability)
    return G


# def generate_attack_chain_graph(honey_state_propagation):
#     G = nx.DiGraph()
#
#     for state_name, neighbour_dict in attack_propagation.items():
#         for next_state, propagation_probability in neighbour_dict.items():
#             G.add_edge(state_name, next_state, weight=propagation_probability)
#     return G

def get_shortest_path(G, s, t):
    # print(nx.shortest_path(G, source=s, target=t))
    try:
        res = [p for p in nx.all_shortest_paths(G, source=s, target=t)]
    except:
        res = []
    return res


def get_all_path(G, s, t):
    try:
        res = [path for path in nx.all_simple_paths(G, source=s, target=t)]
    except:
        traceback.print_exc()
        res = []
    return res


MALWARE_SAMPLE_DIR = 'infostealer_updated'

if __name__ == '__main__':
    conf = config_section_map(MALWARE_SAMPLE_DIR)

    attack_propagation = load_json_data(conf['attack_propagation_path'][0])

    G = generate_attack_chain_graph(attack_propagation)
    path_list = get_all_path(G, 'Spearphishing_Attachment', 'Exfiltration_Over_C2_Channel')
    pprint(path_list)

    print(max([len(d) for d in path_list]))

    # nx.draw(G, with_labels=True)
    # plt.show()
    # print(nx.shortest_path(G, source="Spearphishing_Attachment", target="Exfiltration_Over_C2_Channel"))
    # print([p for p in nx.all_shortest_paths(G, source="Spearphishing_Attachment", target="Exfiltration_Over_C2_Channel")])
    # print(G.get_edge_data("Spearphishing_Attachment", "Command_and_Scripting_Interpreter", default=0))
    # print(get_attack_propagation_prob(G, 'Spearphishing_Attachment', 'Command_and_Scripting_Interpreter'))
    # n = G.neighbors('Process_Hollowing')
    # for n in G.neighbors('Process_Hollowing'):
    #     print(n)
