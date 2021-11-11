"""

__author__ = "Md Mazharul Islam Rakeb"
__email__ = "mislam7@uncc.edu"
__date__ = 5/15/20

"""


class Action:
    def __init__(self, name):
        self.effectiveness = None
        self.effective_states = None
        self.giveup_state = None
        self.name = name
        self.cost = 0
        self.current_state = None
        self.next_state = None
        self.transition_matrix = None
        self.effective_states = []
        self.effectiveness_probability = {}
        self.rewards = {}
        self.risks = {}

    def set_risk(self, state_name, risk):
        self.risks[state_name] = risk

    def get_risk(self, state_name):
        return self.risks[state_name]

    def set_reward(self, state_name, reward):
        self.rewards[state_name] = reward

    def get_reward(self, state_name):
        return self.rewards[state_name]

    def set_effectiveness_probability(self, next_state, effectiveness_probability):
        self.effectiveness_probability[next_state] = effectiveness_probability

    def get_effectiveness_probability(self, next_state):
        return self.effectiveness_probability[next_state]

    def is_action_effects_on_current_state(self, current_state):
        return True if current_state.lower() == self.current_state else False

    def set_effective_states(self, effective_states):
        self.effective_states.append(effective_states)

    def set_transition_matrix(self):
        pass

    def get_effectiveness(self, from_to_key):
        return self.effectiveness[from_to_key] if from_to_key in self.effectiveness else 0.0

    def __str__(self):
        return self.name


def generate_actions_object(action_effectiveness):
    action_objects = {}
    for action_name, action_attribution in action_effectiveness.items():
        action = Action(action_name)
        action_objects[action_name] = action
        action.cost = action_attribution['cost']
        action.current_state = action_attribution['current_state']
        action.next_state = action_attribution['next_state']
        for effective_state, effective_probability in action_attribution['effectiveness'].items():
            action.set_effective_states(effective_state)
            action.set_effectiveness_probability(effective_state, effective_probability)
    return action_objects


def generate_actions_object_new(action_json):
    action_objects = {}
    for action_name, action_attribution in action_json.items():
        action = Action(action_name)
        action_objects[action_name] = action
        action.cost = action_attribution['cost']
        action.effective_states = action_attribution['effective_states']
        action.giveup_state = action_attribution['giveup_state']
        action.effectiveness = action_attribution['effectiveness']
    return action_objects
