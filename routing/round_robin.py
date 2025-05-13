from routing.base import RoutingAlgorithm

class RoundRobin(RoutingAlgorithm):
    def __init__(self, servers):
        super().__init__(servers)
        self.index = 0

    def get_next_server(self):
        server = self.servers[self.index]
        self.index = (self.index + 1) % len(self.servers)
        return server
