from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.middleware.errors import ServerErrorMiddleware
from starlette.middleware.exceptions import ExceptionMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request
from starlette.responses import PlainTextResponse
from starlette.types import ASGIApp, Receive, Scope, Send


def print_client_middleware(app: ASGIApp):
    async def wrapper(scope: Scope, receive: Receive, send: Send):
        if scope["type"] in ("http", "ws"):
            print("Connected by", scope["client"])
        await app(scope, receive, send)

    return wrapper


class AllowCORSMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, origins: list[str] | None = None):
        super().__init__(app)
        self.app = app
        self.origins = [] if origins is None else origins

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        response = await call_next(request)
        origin = request.headers.get("origin")
        if origin:
            if "*" in self.origins:
                response.headers["access-control-allow-origin"] = "*"
            elif origin in self.origins:
                response.headers["access-control-allow-origin"] = origin
        return response


def server_error_handler(request: Request, exc: Exception):
    return PlainTextResponse("Oops.", 500)


SECRET_KEY = "707h2YjMQPk9PiZjyR+syARNKcE+Uop+8Blnm8gIR5o="


def apply_middlewares(app: ASGIApp):
    middlewares = [
        Middleware(ServerErrorMiddleware, handler=server_error_handler),
        print_client_middleware,
        Middleware(AllowCORSMiddleware, origins=["*"]),
        Middleware(SessionMiddleware, secret_key=SECRET_KEY),
        Middleware(ExceptionMiddleware),
    ]
    for middleware in reversed(middlewares):
        if callable(middleware):
            app = middleware(app)
        else:
            cls, args, kwargs = middleware
            app = cls(app, *args, **kwargs)
    return app
