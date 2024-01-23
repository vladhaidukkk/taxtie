from starlette.endpoints import HTTPEndpoint
from starlette.requests import Request
from starlette.responses import PlainTextResponse
from starlette.routing import Mount, Route

from app.auth import routes as auth_routes


class Index(HTTPEndpoint):
    def get(self, request: Request):
        return PlainTextResponse("Hello world!")


routes = [
    Route("/", Index),
    Mount("/auth", routes=auth_routes, name="auth"),
]
