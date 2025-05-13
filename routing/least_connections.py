from routing.base import RoutingAlgorithm


class LeastConnections(RoutingAlgorithm):
    def __init__(self, servers):
        super().__init__(servers)
        self.connection_count = {server: 0 for server in servers}

    def get_next_server(self):
        return min(self.connection_count, key=self.connection_count.get)

    def mark_start(self, server):
        self.connection_count[server] += 1

    def mark_end(self, server):
        pass

