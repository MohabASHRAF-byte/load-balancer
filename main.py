import json
from app_factory import create_app
from backend_loader.handler import get_version_instance

with open("config.json", "r") as f:
    config = json.load(f)

version = get_version_instance(config.get("version", "version1"))
servers = version.load_servers(config)

app = create_app(config, servers)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
