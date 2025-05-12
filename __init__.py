import json
from flask import Flask, request, Response
import requests

# Load configuration from JSON file
with open("config.json", "r") as f:
    config = json.load(f)

app = Flask(__name__)
backend_servers = config["servers"]
routing_algorithm = config["routingAlgorithm"]

# Round-robin state
current_rr = 0

def get_next_server():
    global current_rr

    if routing_algorithm == "round-robin":
        server = backend_servers[current_rr]
        current_rr = (current_rr + 1) % len(backend_servers)
        return server

    # Placeholder for other algorithms
    elif routing_algorithm == "random":
        import random
        return random.choice(backend_servers)

    else:
        raise ValueError(f"Unsupported routing algorithm: {routing_algorithm}")

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE'])
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def forward_request(path):
    server = get_next_server()
    url = f"{server}/{path}"

    try:
        resp = requests.request(
            method=request.method,
            url=url,
            headers={key: value for key, value in request.headers if key.lower() != 'host'},
            data=request.get_data(),
            cookies=request.cookies,
            allow_redirects=False
        )

        response = Response(resp.content, status=resp.status_code)
        for key, value in resp.headers.items():
            response.headers[key] = value
        return response

    except requests.exceptions.RequestException as e:
        return Response(f"Failed to connect to backend: {str(e)}", status=502)

if __name__ == '__main__':
    app.run(port=5000)
