import sqlite3
from pathlib import Path

from starlette.routing import Mount, Router
from starlette.staticfiles import StaticFiles
from starlette.types import Receive, Scope, Send

from app.http import routes as http_routes
from app.middlewares import apply_middlewares
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


@apply_middlewares
async def app(scope: Scope, receive: Receive, send: Send):
    if scope["type"] == "lifespan":
        await lifespan(scope, receive, send)
    else:
        router = Router(
            routes=[
                *http_routes,
                Mount("/ws", routes=ws_routes, name="ws"),
                Mount(
                    "/static", StaticFiles(directory="static", html=True), name="static"
                ),
            ]
        )
        await router(scope, receive, send)
