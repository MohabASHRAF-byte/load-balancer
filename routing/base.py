from abc import ABC, abstractmethod

class RoutingAlgorithm(ABC):
    def __init__(self, servers):
        self.servers = servers

    @abstractmethod
    def get_next_server(self):
        pass
