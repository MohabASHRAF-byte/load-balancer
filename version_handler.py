import json
from versions import v1

with open("config.json", "r") as f:
    config = json.load(f)


def get_app():
    version = config.get("version", 1)

    if version == 1:
        return v1.create_app(config)
    else:
        raise ValueError(f"Unsupported version: {version}")
