"""

__author__ = "Md Mazharul Islam Rakeb"
__email__ = "mislam7@uncc.edu"
__date__ = 5/16/20

"""
import traceback
import networkx as nx

'''
R: <action> : <start-state> : <end-state> : <observation> %f

R:a0     : s0    : * : * 3
R:a0     : s1    : * : * 0
R:a0     : s2    : * : * 0

R:a1     : s0    : * : * 0
R:a1     : s1    : * : * 3
R:a1     : s2    : * : * 0

R:a2     : s0    : * : * 0
R:a2     : s1    : * : * 0
R:a2     : s2    : * : * 3

R:obs    : *     : * : * 1
'''


def generate_reward(action, state, c_impact_confidentiality, g, a_v_impact_integrity):
    risk = state.data_exfiltration_probability * int(c_impact_confidentiality[0]) + int(g[0]) * int(
        a_v_impact_integrity[0])
    action.set_risk(state.name, risk)
    reward = - risk - action.cost
    return reward


def calculate_reward_old(c_impact_confidentiality, g, a_v_impact_integrity, states_objects, action_objects,
                         plan_file_name):
    with open(plan_file_name, 'a') as f:
        f.write("\n")
    for action_name, action in action_objects.items():
        for state_name, state in states_objects.items():
            reward = generate_reward(action, state, c_impact_confidentiality, g, a_v_impact_integrity)
            action.set_reward(state_name, reward)
            with open(plan_file_name, 'a') as f:
                f.write("R:{}     : *    : {} : * ".format(action_name, state_name))
                f.write(" %.6f\n" % reward)


# def calculate_reward(penalty_state, penalty, states_objects, action_objects, plan_file_name):
#     with open(plan_file_name, 'a') as f:
#         f.write("\n")
#     for action_name, action in action_objects.items():
#         for current_state_name, current_state in states_objects.items():
#             for next_state_name, next_state in states_objects.items():
#                 if next_state_name != penalty_state:
#                     reward = - action.cost
#                 else:
#                     reward = - (current_state.max_depth * penalty) - action.cost
#                 action.set_reward(current_state_name, reward)
#                 with open(plan_file_name, 'a') as f:
#                     f.write("R:{}     : {}    : {} : * ".format(action_name, current_state_name, next_state_name))
#                     f.write(" %.6f\n" % reward)


# def calculate_reward(attack_graph, all_states, deception_actions_obj, penalty, honey_states, state_mapping, quit_state,
#                      goal, plan_file_name):
#     with open(plan_file_name, 'a') as f:
#         f.write("\n")
#     for action_name, action_attrb in deception_actions_obj.items():
#         # if action_name == "doNothing":
#         #     continue
#         for next_state in all_states:
#             weighted_depth = 0.0
#             # action_benefit = 0
#             # goal = 0
#             alpha_beta = sum([i * j for i, j in zip(goal, deception_actions_obj[action_name]['action_benefit'])])
#             cost = deception_actions_obj[action_name]['cost']
#             risk = 0.0
#             pen = 0.0
#             mapped_state = state_mapping[next_state]
#             if next_state != quit_state:
#                 if next_state in honey_states:
#                     weighted_depth = attack_graph.node_state[mapped_state]['depth']
#                 else:
#                     risk = attack_graph.node_state[mapped_state]['risk']
#             if next_state == quit_state:
#                 pen = penalty
#             # try:
#             reward = weighted_depth + alpha_beta - cost - risk - pen
#             # print("no error:")
#             # print(weighted_depth, alpha_beta, cost, risk, pen)
#             # except TypeError:
#             #     print("with error:")
#             # print(weighted_depth, alpha_beta, cost, risk, pen)
#             with open(plan_file_name, 'a') as f:
#                 f.write("R:{}     : *    : {} : * ".format(action_name, next_state))
#                 f.write(" %.6f\n" % reward)


def calculate_reward(agent, I, P, plan_file_name):
    """
    :param plan_file_name:
    :param P:
    :param I:
    :param agent:
    :param s: current state (observation)
    :param s_: next state (observation)
    :param a_v: attack action
    :param a_d: deception action
    :return: reward
    """
    with open(plan_file_name, 'a') as f:
        f.write("\n")
    for a_d, action_attr in agent.d_action_space.items():
        for s_ in agent.state_space.keys():
            H_s_ = 0  # is next state is honey(1) or real(0)
            W_d_s_ = 0
            if s_ in agent.honey_states:
                H_s_ = 1
                # W_d_s_: weight, the sooner the deception is better
                shortest_paths = [p for p in
                                  nx.all_shortest_paths(agent.dg, source=s_, target=agent.defender_goal_state)]
                W_d_s_ = len(shortest_paths[0])

            sum_ai_bi = 0
            for g in agent.DECEPTION_GOALS:
                ai = agent.goal[g]
                bi = agent.deception_actions_json[a_d]['benefit'][g]
                sum_ai_bi += ai * bi

            R_s_ = 0
            # risk
            if 1 - H_s_:
                # 𝐿 is 𝑛 shortest paths from 𝒔′ to exfiltration state
                L = [p for p in nx.all_shortest_paths(agent.dg, source=s_, target=agent.attacker_goal_state)]
                grand_product = 1
                for l in L:
                    product_sigma_i_i_ = 1
                    for i, i_ in zip(l[:-1], l[1:]):
                        attack_action = ''
                        for _, v in agent.dg.get_edge_data(i, i_, default=0).items():
                            if v['deception_action'][0] == 'doNothing':
                                attack_action = v['attack_action'][1]
                                break
                        if attack_action:
                            sigma_i_i_ = agent.attack_action_prediction_json[i][attack_action]['probability']
                        else:
                            sigma_i_i_ = 0
                        product_sigma_i_i_ *= sigma_i_i_
                    grand_product *= 1 - product_sigma_i_i_
                p_s_ = 1 - grand_product
                R_s_ = p_s_ * I
            c_a_d = agent.deception_actions_json[a_d]['cost']
            # c_a_d = 0
            reward = W_d_s_ * H_s_ + sum_ai_bi - c_a_d - (1 - H_s_) * R_s_ - (1 - H_s_) * P
            # print("reward: {}".format(reward))
            # return reward
            with open(plan_file_name, 'a') as f:
                f.write("R:{}     : *    : {} : * ".format(a_d, s_))
                f.write(" %.6f\n" % reward)
