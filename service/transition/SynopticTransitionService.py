from dao.SessionHandler import SessionHandler
from config.SessionConfig import session_config
from service.transition.BaseTransitionService import BaseTransitionService
import collections
import pydot
import random

class SynopticTransitionService(BaseTransitionService):
    """
    来自synoptic的transition方法
    """

    def __init__(self):
        self.message_texts = session_config.message_texts
        self.message_dict = session_config.message_dict
        self.nodeid2label = None
        self.transition_prob = None
        self.INITIAL = self.TERMINAL = None

    def read_dot(self):
        graphs = pydot.graph_from_dot_file("twopc.dot")
        graph = graphs[0]
        self.nodeid2label = {}  # {'0':'INITIAL'}
        for k, v in graph.obj_dict["nodes"].items():
            label = v[0]["attributes"]["label"][1:-1]
            self.nodeid2label[k] = label
            if label == "INITIAL":
                self.INITIAL = k
            elif label == "TERMINAL":
                self.TERMINAL = k
        self.transition_prob = collections.defaultdict(lambda: {}) # {'0': {'1': 0.4, '2': 0.6}}
        for k, v in graph.obj_dict["edges"].items():
            source, target = k[0], k[1]
            self.transition_prob[source][target] = float(v[0]["attributes"]["label"][1:-1].split(":")[1])
        assert all((abs(sum(v.values())-1.0) <= 0.02) for k, v in self.transition_prob.items())

    def __random_pick(self, some_list, probabilities):
        x = random.uniform(0, 1)
        cumulative_probability = 0.0
        for item, item_probability in zip(some_list, probabilities):
            cumulative_probability += item_probability
            if x < cumulative_probability: break
        return item

    def sample(self):
        behaviors = []
        cur_node = self.INITIAL
        while True:
            choices = self.transition_prob[cur_node]
            next_node = self.__random_pick(list(choices.keys()), list(choices.values()))
            if next_node == self.TERMINAL:
                break
            behaviors.append(self.nodeid2label[next_node])
            cur_node, next_node = next_node, None
        print(behaviors)
        return behaviors






if __name__ == "__main__":

    synoptic_transition = SynopticTransitionService()
    synoptic_transition.read_dot()
    synoptic_transition.sample()
