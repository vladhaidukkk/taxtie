from functools import partial

from starlette.datastructures import Headers
from starlette.middleware import Middleware
from starlette.middleware.errors import ServerErrorMiddleware
from starlette.middleware.exceptions import ExceptionMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request
from starlette.responses import PlainTextResponse
from starlette.types import ASGIApp, Message, Receive, Scope, Send


class PrintClientMiddleware:
    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if scope["type"] in ("http", "ws"):
            print("Connected by", scope["client"])
        await self.app(scope, receive, send)


class AllowCORSMiddleware:
    def __init__(self, app: ASGIApp, origins: list[str] | None = None):
        self.app = app
        self.origins = origins if origins is not None else []

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        send = partial(self.send, scope=scope, send=send)
        await self.app(scope, receive, send)

    async def send(self, message: Message, scope: Scope, send: Send):
        if message["type"] == "http.response.start":
            headers = Headers(scope=scope)
            origin = "*" if "*" in self.origins else headers.get("origin", None)
            if origin and origin in self.origins:
                message["headers"].append(
                    (b"access-control-allow-origin", origin.encode())
                )
        await send(message)


def server_error_handler(request: Request, exc: Exception):
    return PlainTextResponse("Oops.", 500)


SECRET_KEY = "707h2YjMQPk9PiZjyR+syARNKcE+Uop+8Blnm8gIR5o="


def apply_middlewares(app: ASGIApp):
    middlewares = [
        Middleware(ServerErrorMiddleware, handler=server_error_handler),
        Middleware(PrintClientMiddleware),
        Middleware(AllowCORSMiddleware, origins=["*"]),
        Middleware(SessionMiddleware, secret_key=SECRET_KEY),
        Middleware(ExceptionMiddleware),
    ]
    for cls, args, kwargs in reversed(middlewares):
        app = cls(app, *args, **kwargs)
    return app
