"""

__author__ = "Md Mazharul Islam Rakeb"
__email__ = "mislam7@uncc.edu"
__date__ = 5/14/20

"""
from collections import defaultdict


def create_transition(action, attack_states, action_attributes, all_states, plan_file_name):
    print("Action: {}".format(action))
    with open(plan_file_name, 'a') as f:
        f.write("\nT:{}\n".format(action))
    for current_state in all_states:
        current_state_attack_propagation = attack_states[current_state] if current_state in attack_states else None

        is_action_effects_on_current_state = True if current_state.lower() == action_attributes[
            'current_state'].lower() else False

        for next_state in all_states:
            if is_action_effects_on_current_state and current_state_attack_propagation is not None:
                if next_state.lower() in action_attributes:
                    t_r_c_a = current_state_attack_propagation[action_attributes['next_state']] * action_attributes[
                        next_state]
                else:
                    t_r_c_a = current_state_attack_propagation[
                        next_state] if next_state in current_state_attack_propagation else 0
            else:
                t_r_c_a = 0

            with open(plan_file_name, 'a') as f:
                f.write("%.2f " % t_r_c_a)
            print("{} --> {} : {}".format(current_state, next_state, t_r_c_a))
        with open(plan_file_name, 'a') as f:
            f.write("\n")


def create_all_transition(actions_effectiveness, attack_states, all_states, plan_file_name):
    for action in actions_effectiveness:
        action_attributes = actions_effectiveness[action]
        create_transition(action, attack_states, action_attributes, all_states, plan_file_name)


def generate_defense_transition(states_objects, action_objects, plan_file_name):
    for action_name, action in action_objects.items():
        # print("Action: {}".format(action))
        with open(plan_file_name, 'a') as f:
            f.write("\nT:{}\n".format(action))
        transition_matrix = []
        for _, current_state in states_objects.items():
            row = []
            for _, next_state in states_objects.items():
                if action.is_action_effects_on_current_state(current_state.name):
                    if next_state.name in action.effective_states:
                        t_r_c_a = current_state.get_attack_propagation_probability(
                            action.next_state) * action.get_effectiveness_probability(next_state.name)
                    else:
                        t_r_c_a = current_state.get_attack_propagation_probability(next_state.name)
                else:
                    t_r_c_a = current_state.get_attack_propagation_probability(next_state.name)

                with open(plan_file_name, 'a') as f:
                    # f.write("%.2f " % t_r_c_a)
                    f.write("{} ".format(t_r_c_a))
                # print("{} --> {} : {}".format(current_state, next_state, t_r_c_a))
                row.append(t_r_c_a)
            transition_matrix.append(row)
            with open(plan_file_name, 'a') as f:
                f.write("\n")
        action.transition_matrix = transition_matrix


# TODO old transition for honey states
# def generate_transition(G, states, action_objects, plan_file_name):
#     for action_name, action in action_objects.items():
#         # print("Action: {}".format(action))
#         with open(plan_file_name, 'a') as f:
#             f.write("\nT:{}\n".format(action))
#         transition_matrix = []
#         for current_state in states:
#             row = []
#             for next_state in states:
#                 if current_state in action.effective_states:
#                     from_to_key = current_state + '-->' + next_state
#                     if next_state == action.honey_state:
#                         t_r_c_a = 0
#                         for n in G.neighbors(current_state):
#                             from_to_key = current_state + '-->' + n
#                             effectiveness = action.get_effectiveness(from_to_key)
#                             app = get_attack_propagation_prob(G, current_state, n)
#                             t_r_c_a += app * effectiveness
#                     else:
#                         effectiveness = action.get_effectiveness(from_to_key)
#                         app = get_attack_propagation_prob(G, current_state, next_state)
#                         t_r_c_a = app * (1 - effectiveness)
#                 else:
#                     t_r_c_a = get_attack_propagation_prob(G, current_state, next_state)
#
#                 with open(plan_file_name, 'a') as f:
#                     # f.write("%.2f " % t_r_c_a)
#                     f.write("{} ".format(t_r_c_a))
#                 # print("{} --> {} : {}".format(current_state, next_state, t_r_c_a))
#                 row.append(t_r_c_a)
#             transition_matrix.append(row)
#             with open(plan_file_name, 'a') as f:
#                 f.write("\n")
#         action.transition_matrix = transition_matrix


# new transition for giveup states
# def _generate_transition(G, states, action_objects, plan_file_name):
#     for action_name, action in action_objects.items():
#         # print("Action: {}".format(action))
#         with open(plan_file_name, 'a') as f:
#             f.write("\nT:{}\n".format(action))
#         transition_matrix = []
#         for current_state in states:
#             row = []
#             for next_state in states:
#                 if current_state in action.effective_states:
#                     from_to_key = current_state + '-->' + next_state
#                     if next_state == action.giveup_state:
#                         t_r_c_a = 0
#                         for n in G.neighbors(current_state):
#                             from_to_key = current_state + '-->' + n
#                             effectiveness = action.get_effectiveness(from_to_key)
#                             app = get_attack_propagation_prob(G, current_state, n)
#                             t_r_c_a += app * (1 - effectiveness)
#                     else:
#                         effectiveness = action.get_effectiveness(from_to_key)
#                         app = get_attack_propagation_prob(G, current_state, next_state)
#                         t_r_c_a = app * effectiveness
#                 else:
#                     if next_state == action.giveup_state:
#                         t_r_c_a = 1.0
#                     else:
#                         t_r_c_a = 0.0
#
#                 with open(plan_file_name, 'a') as f:
#                     # f.write("%.2f " % t_r_c_a)
#                     f.write("{} ".format(t_r_c_a))
#                 # print("{} --> {} : {}".format(current_state, next_state, t_r_c_a))
#                 row.append(t_r_c_a)
#             transition_matrix.append(row)
#             with open(plan_file_name, 'a') as f:
#                 f.write("\n")
#         action.transition_matrix = transition_matrix


def generate_transition(graph, states, action_objects, plan_file_name, real_states, honey_states, shared_states,
                        quit_state, defender_goal_state, state_mapping):
    for action_name, action_attributes in action_objects.items():
        # if action_name == "doNothing":
        #     continue
        with open(plan_file_name, 'a') as f:
            f.write("\nT:{}\n".format(action_name))
        transition_matrix = []
        effectiveness = action_attributes["effectiveness"]
        quit = action_attributes["quit"]
        effective_transition = action_attributes["transition"]  # dict

        for current_state in states:
            row = []
            for next_state in states:
                t_r_c_a = 0.0
                if current_state in (quit_state, defender_goal_state):
                    if next_state == current_state:
                        t_r_c_a = 1.0
                elif current_state in real_states:
                    if current_state in effective_transition:
                        destination_node = effective_transition[current_state]['destination_node']
                        attack_action = effective_transition[current_state]['attack_action']
                        app = graph.get_attack_propagation_prob(current_state, next_state)
                        if next_state == quit_state:
                            for neib in graph.g.neighbors(current_state):
                                if attack_action == graph.get_attack_action(current_state, neib):
                                    app = graph.get_attack_propagation_prob(current_state, neib)
                                    break
                            t_r_c_a = quit * app
                        elif next_state == destination_node:
                            for neib in graph.g.neighbors(current_state):
                                if attack_action == graph.get_attack_action(current_state, neib):
                                    app = graph.get_attack_propagation_prob(current_state, neib)
                                    break
                            t_r_c_a = app * effectiveness
                        elif attack_action == graph.get_attack_action(current_state, next_state):
                            t_r_c_a = app * (1 - effectiveness - quit)
                        else:
                            t_r_c_a = app
                    else:
                        t_r_c_a = graph.get_attack_propagation_prob(current_state, next_state)
                else:
                    if current_state in effective_transition:
                        destination_node = effective_transition[current_state]['destination_node']
                        attack_action = effective_transition[current_state]['attack_action']
                        mapped_current_state = state_mapping[current_state]
                        app = 0.0
                        if next_state == quit_state:
                            for neib in graph.g.neighbors(mapped_current_state):
                                if attack_action == graph.get_attack_action(mapped_current_state, neib):
                                    app = graph.get_attack_propagation_prob(mapped_current_state, neib)
                                    break
                            t_r_c_a = quit * app
                        elif next_state == destination_node:
                            for neib in graph.g.neighbors(mapped_current_state):
                                if attack_action == graph.get_attack_action(mapped_current_state, neib):
                                    app = graph.get_attack_propagation_prob(mapped_current_state, neib)
                                    break
                            t_r_c_a = app * effectiveness
                        elif attack_action == graph.get_attack_action(mapped_current_state, next_state):
                            app = graph.get_attack_propagation_prob(mapped_current_state, next_state)
                            t_r_c_a = app * (1 - effectiveness - quit)
                        else:
                            if next_state in honey_states or next_state in shared_states:
                                t_r_c_a = graph.get_attack_propagation_prob(mapped_current_state,
                                                                            state_mapping[next_state])
                            else:
                                t_r_c_a = 0
                    else:
                        if next_state in honey_states or next_state in shared_states:
                            mapped_state = state_mapping[current_state]
                            t_r_c_a = graph.get_attack_propagation_prob(mapped_state, state_mapping[next_state])
                        else:
                            t_r_c_a = 0.0
                    # if current_state in effective_transition:
                    #     destination_node = effective_transition[current_state]['destination_node']
                    #     attack_action = effective_transition[current_state]['attack_action']
                    #     mapped_current_state = state_mapping[current_state]
                    #     app = 0.0
                    #     if next_state == quit_state:
                    #         for neib in graph.g.neighbors(mapped_current_state):
                    #             if attack_action == graph.get_attack_action(mapped_current_state, neib):
                    #                 app = graph.get_attack_propagation_prob(mapped_current_state, neib)
                    #                 break
                    #         t_r_c_a = quit * app
                    #     elif next_state == destination_node:
                    #         for neib in graph.g.neighbors(mapped_current_state):
                    #             if attack_action == graph.get_attack_action(mapped_current_state, neib):
                    #                 app = graph.get_attack_propagation_prob(mapped_current_state, neib)
                    #                 break
                    #         t_r_c_a = app * effectiveness
                    #     elif attack_action == graph.get_attack_action(mapped_current_state, next_state):
                    #         app = graph.get_attack_propagation_prob(mapped_current_state, next_state)
                    #         t_r_c_a = app * (1 - effectiveness - quit)
                    #     else:
                    #         t_r_c_a = graph.get_attack_propagation_prob(mapped_current_state, next_state)
                    # else:
                    #     if next_state in real_states:
                    #         mapped_state = state_mapping[current_state]
                    #         t_r_c_a = graph.get_attack_propagation_prob(mapped_state, next_state)
                    #     else:
                    #         t_r_c_a = 0.0

                # t_r_c_a = round(t_r_c_a, 2)
                with open(plan_file_name, 'a') as f:
                    # f.write("%.2f " % t_r_c_a)
                    f.write("{} ".format(t_r_c_a))
                # print("{} --> {} : {}".format(current_state, next_state, t_r_c_a))
                row.append(t_r_c_a)
            if sum(row) != 1:
                print(action_name, sum(row))
                # raise RuntimeError("probability sum not 1 error")
            transition_matrix.append(row)
            with open(plan_file_name, 'a') as f:
                f.write("\n")
        action_objects[action_name]['transition_matrix'] = transition_matrix


def state_transition(agent, plan_file):
    for deception_action, action_attributes in agent.d_action_space.items():
        with open(plan_file, 'a') as f:
            f.write("\nT:{}\n".format(deception_action))
        transition_matrix = []
        effectiveness = action_attributes['effectiveness']
        attack_action = action_attributes['attack_action']

        for current_state in agent.state_space.keys():
            row = []
            for next_state in agent.state_space.keys():
                if next_state == current_state and current_state in (agent.attacker_goal_state, agent.defender_goal_state):
                    t_r_c_a = 1.0
                else:
                    t_r_c_a = 0.0
                    nei = agent.dg.get_edge_data(current_state, next_state, default=None)
                    if nei:
                        same_attack_action_edge = set()
                        for _, edge_attr in nei.items():
                            app = edge_attr['app']
                            if edge_attr['attack_action'] in attack_action:  # defense action is effective to the edge
                                if edge_attr['deception_action'] == deception_action:  # this is a honey transaction
                                    t_r_c_a += app * effectiveness
                                elif edge_attr['deception_action'] == 'doNothing':  # this is a real transaction under deception action
                                    t_r_c_a += app * (1 - effectiveness)
                            else:
                                if edge_attr['attack_action'] not in same_attack_action_edge:
                                    same_attack_action_edge.add(edge_attr['attack_action'])
                                    if current_state in agent.honey_states and next_state in (agent.honey_states.union(agent.shared_states)):
                                        t_r_c_a += app
                                    elif current_state not in agent.honey_states and next_state not in agent.honey_states:
                                        # if edge_attr['deception_action'] == 'doNothing':
                                        t_r_c_a += app

                # end code
                with open(plan_file, 'a') as f:
                    # f.write("%.2f " % t_r_c_a)
                    f.write("{} ".format(t_r_c_a))
                # print("{} --> {} : {}".format(current_state, next_state, t_r_c_a))
                row.append(t_r_c_a)
            if sum(row) != 1:
                pass
                # print(deception_action, current_state, sum(row))
                # raise RuntimeError("probability sum not 1 error")
            transition_matrix.append(row)
            with open(plan_file, 'a') as f:
                f.write("\n")
        action = agent.d_action_space[deception_action]
        action['transition_matrix'] = transition_matrix
