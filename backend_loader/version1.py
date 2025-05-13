from backend_loader.version_interface import Version

class Version1(Version):
    def load_servers(self, config):
        return config["servers"]
