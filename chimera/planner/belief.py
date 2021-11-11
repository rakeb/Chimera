"""

__author__ = "Md Mazharul Islam Rakeb"
__email__ = "mislam7@uncc.edu"
__date__ = 5/28/20

"""
import copy


def generate_initial_belief(all_states):
    initial_belief = {}
    prob = 1 / len(all_states)
    for state in all_states:
        initial_belief[state] = prob
    return initial_belief


def generate_next_belief(b_s_current_state_belief_probability, all_states, s_prime_next_state, transition_matrix,
                         obs_matrix,
                         observation_index):
    '''
    :param s_prime is the next state
    :param b_s current state belief (initial belief)
    '''

    # calculate transition_sum
    s_prime_next_state_index = all_states.index(s_prime_next_state)
    t_s_prime_given_s_a_matrix = transition_matrix[s_prime_next_state_index]
    tran_sum_given_s_a_multi_b_s = 0
    for p in t_s_prime_given_s_a_matrix:
        tran_sum_given_s_a_multi_b_s += p * b_s_current_state_belief_probability

    o_given_s_prime_a = obs_matrix[s_prime_next_state_index][observation_index]

    # calculate eta
    obs_sum_o_given_s_prime_a = 0
    for i in range(len(obs_matrix)):
        obs_sum_o_given_s_prime_a += obs_matrix[i][observation_index]

    eta = 1 / (obs_sum_o_given_s_prime_a * tran_sum_given_s_a_multi_b_s)

    b_prime_s_prime = eta * o_given_s_prime_a * tran_sum_given_s_a_multi_b_s
    return b_prime_s_prime


def update_belief(all_states, current_observation_state, obs_matrix, observations, transition_matrix, initial_belief):
    # print("current_observation: {}".format(current_observation_state))
    # print("obs_matrix: {}".format(obs_matrix))
    # print("transition_matrix: {}".format(transition_matrix))
    # print("initial_belief: {}".format(initial_belief))

    next_belief = {}
    observation_index = observations.index(current_observation_state)
    for next_state, current_state_belief_probability in initial_belief.items():
        updated_belief = generate_next_belief(current_state_belief_probability, all_states, next_state,
                                              transition_matrix,
                                              obs_matrix,
                                              observation_index)
        next_belief[next_state] = updated_belief
    return next_belief
