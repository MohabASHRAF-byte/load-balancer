from fastapi import FastAPI, Request
from fastapi.responses import Response
from backend_loader.routing_loader import load_routing_algorithm
import httpx


def create_app(config, servers):
    app = FastAPI()
    routing = load_routing_algorithm(config["routingAlgorithm"], servers)

    client = None

    @app.on_event("startup")
    async def startup_event():
        nonlocal client
        client = httpx.AsyncClient(
            timeout=10.0,
            limits=httpx.Limits(max_connections=100, max_keepalive_connections=20)
        )

    @app.on_event("shutdown")
    async def shutdown_event():
        nonlocal client
        if client:
            await client.aclose()

    @app.api_route("/{full_path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"])
    async def proxy(full_path: str, request: Request):
        nonlocal client
        try:
            server = routing.get_next_server()
            headers = {k: v for k, v in request.headers.items() if k.lower() != "host"}
            body = await request.body()
            response = await client.request(
                method=request.method,
                url=f"{server}/{full_path}",
                headers=headers,
                content=body,
                cookies=request.cookies
            )

            return Response(
                content=response.content,
                status_code=response.status_code,
                headers={k: v for k, v in response.headers.items()
                         if k.lower() not in ('content-encoding', 'transfer-encoding')}
            )

        except httpx.RequestError as e:
            return Response(
                content=f"Error connecting to backend server: {str(e)}",
                status_code=502
            )
        except Exception as e:
            return Response(
                content=f"Unexpected error: {str(e)}",
                status_code=500
            )

    return app