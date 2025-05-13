import random
from routing.base import RoutingAlgorithm

class RandomChoice(RoutingAlgorithm):
    def get_next_server(self):
        return random.choice(self.servers)
