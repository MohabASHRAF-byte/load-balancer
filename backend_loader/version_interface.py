from abc import ABC, abstractmethod

class Version(ABC):
    @abstractmethod
    def load_servers(self, config):
        pass
