from starlette.requests import Request
from starlette.responses import PlainTextResponse
from starlette.routing import Mount, Route

from app.auth import routes as auth_routes


def index(request: Request):
    return PlainTextResponse("Hello world!")


routes = [
    Route("/", index),
    Mount("/auth", routes=auth_routes, name="auth"),
]
