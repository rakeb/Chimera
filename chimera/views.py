import ast
import json
import logging
import os
from collections import defaultdict

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from mergedeep import merge

# Create your views here.
from chimera.planner.agent import Agent
from chimera.planner.main import create_pomdp_agent, generate_pomdp_file_skeleton, PLAN_FILE, solve_zmdp, \
    recommend_action
from chimera.planner.observation import create_all_observation_normalized
from chimera.planner.reward import calculate_reward
from chimera.planner.transition import state_transition
from chimeraweb.settings import STATICFILES_DIRS, TEMPLATES

logger = logging.getLogger('views.py')
logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d:%H:%M:%S',
                    level=logging.DEBUG)

AGENT = None


def get_agent():
    global AGENT
    if not AGENT:
        AGENT = create_pomdp_agent()
    return AGENT


def index(request):
    agent = get_agent()
    context = {
        'real_state': agent.real_state,
        'honey_states': agent.honey_states,
        'shared_state': agent.shared_states,
        'attacker_goal_state': agent.attacker_goal_state,
        'defender_goal_state': agent.defender_goal_state,
        'goal': agent.goal,
        'deception_actions': agent.deception_actions_json,
        'attack_action_prediction': agent.attack_action_prediction_json
    }
    logger.info("Index called")
    # return render(request, 'chimera/index.html', context=context)
    return render(request, 'chimera/index.html', context=context)


def get_planning_parameters_old(request_body):
    deception_actions = defaultdict(dict)
    attack_action_prediction = defaultdict(dict)
    deception_goal = {'diversion': 0, 'distortion': 0, 'depletion': 0, 'discovery': 0}
    for key, val in request_body.items():
        key = key.split(' ')
        # 'deception_action corrouptTraffic attack_action'
        if key[0] == 'deception_action':  # TODO benefit is not considered yet
            d_action = key[1]
            attr = key[2]
            if attr == 'attack_action':
                deception_actions[d_action][attr] = [val] if val else []
            else:
                deception_actions[d_action][attr] = float(val)
        # 'attack_action_prediction User_Execution_Malicious_File setFileAttribute'
        elif key[0] == 'attack_action_prediction':
            cur_state = key[1]
            a_action = key[2]
            attack_action_prediction[cur_state][a_action] = {'probability': float(val)}
        elif key[0] == 'deception_goal':
            for goal in val:
                deception_goal[goal] = 1

    logger.debug("Updated deception actions dict: {}".format(deception_actions))
    logger.debug("Updated attack_action_prediction dict: {}".format(attack_action_prediction))
    logger.debug("Updated deception_goal dict: {}".format(deception_goal))
    return deception_actions, attack_action_prediction, deception_goal


def get_planning_parameters(request_body):
    deception_actions = defaultdict(dict)
    attack_action_prediction = defaultdict(dict)
    deception_goal = {'diversion': 0, 'distortion': 0, 'depletion': 0, 'discovery': 0}
    for key, val in request_body.items():
        if key == 'deception_action':  # TODO benefit is not considered yet
            # deception_action = {
            #     "migrateInHE": {
            #         "attack_action": ["execute"],
            #         "effectiveness": 0.95,
            #         "cost": 95,
            #         "benefit": {
            #             "diversion": 1,
            #             "distortion": 1,
            #             "depletion": 1,
            #             "discovery": 1
            #         }
            #     }
            # }
            for d_action_dict in val:
                deception_actions[d_action_dict['deception_action_name']]['attack_action'] = ast.literal_eval(d_action_dict['attack_action'])
                deception_actions[d_action_dict['deception_action_name']]['effectiveness'] = float(d_action_dict['effectiveness'])
                deception_actions[d_action_dict['deception_action_name']]['cost'] = float(d_action_dict['cost'])
                deception_actions[d_action_dict['deception_action_name']]['benefit'] = ast.literal_eval(d_action_dict['benefit'])

        # 'attack_action_prediction User_Execution_Malicious_File setFileAttribute'
        elif key == 'attack_action_prediction':
            # attack_action_prediction = {
            #     "User_Execution_Malicious_File": {
            #         "setFileAttribute": {
            #             "probability": 0.41
            #         },
            #         "addToRegistryRunKeys": {
            #             "probability": 0.41
            #         },
            #         "tasklist": {
            #             "probability": 0.06
            #         },
            #         "queryRegistry": {
            #             "probability": 0.06
            #         },
            #         "listDir": {
            #             "probability": 0.06
            #         }
            #     }
            # }
            for a_action_pred_dict in val:
                d = {
                    a_action_pred_dict['attack_action']: {
                        'probability': float(a_action_pred_dict['probability'])
                    }
                }
                attack_action_prediction[a_action_pred_dict['current_state']].update(d)
        elif key[0] == 'deception_goal':
            for goal in val:
                deception_goal[goal] = 1

    logger.debug("Updated deception actions dict: {}".format(deception_actions))
    logger.debug("Updated attack_action_prediction dict: {}".format(attack_action_prediction))
    logger.debug("Updated deception_goal dict: {}".format(deception_goal))
    return deception_actions, attack_action_prediction, deception_goal


def update_planning_parameter(json_loads):
    agent = get_agent()
    deception_actions, attack_action_prediction, deception_goal = get_planning_parameters(json_loads)
    agent.deception_actions_json = merge({}, agent.deception_actions_json, deception_actions)
    agent.attack_action_prediction_json = merge({}, agent.attack_action_prediction_json, attack_action_prediction)
    agent.goal.update(deception_goal)

    generate_pomdp_file_skeleton(agent=agent, discount=0.5, values='reward')
    state_transition(agent=agent, plan_file=PLAN_FILE)
    create_all_observation_normalized(agent=agent, plan_file_name=PLAN_FILE)

    calculate_reward(agent=agent, I=100, P=10, plan_file_name=PLAN_FILE)


# def generate_plan_old(request):
#     output = {
#         'status': 400,
#         'message': 'Failed'
#     }
#     if not agent:
#         output = {
#             'status': 200,
#             'message': 'No parameter is updated. Plan did not updated!'
#         }
#     else:
#         try:
#             solve_zmdp()
#             output = {
#                 'status': 200,
#                 'message': 'New Plan Generated!'
#             }
#         except Exception as e:
#             logger.error("Failed to generate plan: {}".format(e))
#
#     return HttpResponse(
#         json.dumps(output),
#         content_type="application/json"
#     )


def visualize_deception_graph(request):
    return render(request, 'deception_graph_visualization.html')


def generate_deception_graph(request):
    agent = get_agent()
    output = {
        'status': 400,
        'message': 'Failed'
    }
    if request.method == 'POST':
        logger.info("Request for Deception Graph generation starts")

        json_loads = json.loads(request.body.decode("utf-8"))
        logger.info("Request body: {}".format(json_loads))
        template_dir = TEMPLATES[0]['DIRS'][0]
        graph_path = os.path.join(template_dir, 'deception_graph_visualization.html')
        agent.visualize_graph(graph_path)

        output['message'] = 'Deception graph generation success'
        output['status'] = 200

        return HttpResponse(
            json.dumps(output),
            content_type="application/json"
        )

    if request.method == 'GET':
        deception_graph = agent.dg

        _context = []
        for edge in deception_graph.edges(data=True):
            output = {'start_state': edge[0], 'end_state': edge[1]}
            output.update(edge[2])
            _context.append(output)
        logger.info(_context)
        context = {'edge_list': _context}
        return render(request, 'chimera/deception_graph_generate.html', context=context)


def update_plan(request):
    output = {
        'status': 400,
        'message': 'Failed'
    }
    if request.method == 'POST':
        logger.info("Request for Planning starts")

        json_loads = json.loads(request.body.decode("utf-8"))
        logger.info("Request body: {}".format(json_loads))

        update_planning_parameter(json_loads)

        logger.debug("ZMDP solve starts...")
        c = solve_zmdp()
        logger.debug("ZMDP solved in: {} microseconds".format(c.microseconds))

        output[
            'message'] = 'New deception plan generated in {} seconds!'.format(c.microseconds / 1000000)
        output['status'] = 200

        return HttpResponse(
            json.dumps(output),
            content_type="application/json"
        )


def recommend_optimal_action(request):
    agent = get_agent()
    output = {
        'status': 400,
        'message': 'Failed'
    }
    if request.method == 'POST':
        logger.info("Request for Planning starts")

        json_loads = json.loads(request.body.decode("utf-8"))
        logger.info("Request body: {}".format(json_loads))
        current_observed_state = json_loads['current_observed_state']
        rec_action = recommend_action(current_observed_state, agent)

        output['message'] = rec_action
        output['status'] = 200

        return HttpResponse(
            json.dumps(output),
            content_type="application/json"
        )

    if request.method == 'GET':
        context = {
            'real_state': agent.real_state,
            'honey_states': agent.honey_states,
            'shared_state': agent.shared_states,
            'attacker_goal_state': agent.attacker_goal_state,
            'defender_goal_state': agent.defender_goal_state,
            'goal': agent.goal,
            'deception_actions': agent.deception_actions_json,
            'attack_action_prediction': agent.attack_action_prediction_json,
            'state_space': agent.state_space.keys()
        }

        _context = []
        for current_observed_state in agent.state_space.keys():
            rec_action = recommend_action(current_observed_state, agent)
            output = {'current_observed_state': current_observed_state, 'rec_action': rec_action}
            _context.append(output)
        logger.info(_context)
        context['recommended_action_list'] = _context

        return render(request, 'chimera/action_recommendation.html', context=context)
