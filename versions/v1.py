from flask import Flask, request, Response
import requests
import importlib

def load_routing_algorithm(name, servers):
    module_name = f"routing.{name.lower().replace('-', '_')}"
    class_name = ''.join(part.capitalize() for part in name.split('-'))
    module = importlib.import_module(module_name)
    routing_class = getattr(module, class_name)
    return routing_class(servers)

def create_app(config):
    app = Flask(__name__)
    routing = load_routing_algorithm(config["routingAlgorithm"], config["servers"])

    @app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE'])
    @app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
    def forward_request(path):
        server = routing.get_next_server()
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

    return app
