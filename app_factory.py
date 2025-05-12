import httpx
from fastapi import FastAPI, Request
from fastapi.responses import Response

from backend_loader.routing_loader import load_routing_algorithm


def create_app(config, servers):
    app = FastAPI()
    routing = load_routing_algorithm(config["routingAlgorithm"], servers)

    @app.api_route("/{full_path:path}", methods=["GET", "POST", "PUT", "DELETE"])
    async def proxy(full_path: str, request: Request):
        backend = routing.get_next_server()
        url = f"{backend}/{full_path}"

        try:
            async with httpx.AsyncClient() as client:
                resp = await client.request(
                    method=request.method,
                    url=url,
                    headers={k: v for k, v in request.headers.items() if k.lower() != "host"},
                    content=await request.body(),
                    cookies=request.cookies,
                    timeout=10.0,
                )

            return Response(content=resp.content, status_code=resp.status_code, headers=dict(resp.headers))

        except httpx.RequestError as e:
            return Response(content=f"Error contacting backend: {str(e)}", status_code=502)

    return app
