import sqlite3
from functools import partial
from pathlib import Path

from starlette.datastructures import Headers
from starlette.middleware.errors import ServerErrorMiddleware
from starlette.middleware.exceptions import ExceptionMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request
from starlette.responses import PlainTextResponse
from starlette.routing import Mount, Router
from starlette.types import ASGIApp, Message, Receive, Scope, Send

from app.http import routes as http_routes
from app.ws import routes as ws_routes


async def lifespan(scope: Scope, receive: Receive, send: Send):
    while True:
        msg = await receive()
        if msg["type"] == "lifespan.startup":
            scope["state"]["db"] = sqlite3.connect(Path.cwd() / "db.sqlite")
            await send({"type": "lifespan.startup.complete"})
        elif msg["type"] == "lifespan.shutdown":
            scope["state"]["db"].close()
            await send({"type": "lifespan.shutdown.complete"})
            break


async def app(scope: Scope, receive: Receive, send: Send):
    if scope["type"] == "lifespan":
        await lifespan(scope, receive, send)
    else:
        router = Router(
            routes=[
                *http_routes,
                Mount("/ws", routes=ws_routes, name="ws"),
            ]
        )
        await router(scope, receive, send)


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

app = ServerErrorMiddleware(
    PrintClientMiddleware(
        AllowCORSMiddleware(
            SessionMiddleware(
                ExceptionMiddleware(app),
                secret_key=SECRET_KEY,
            ),
            origins=["null"],
        )
    ),
    handler=server_error_handler,
)
