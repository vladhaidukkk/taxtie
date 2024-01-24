import sqlite3
from contextlib import asynccontextmanager
from pathlib import Path
from sqlite3 import Connection
from typing import AsyncIterator, TypedDict

from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.routing import Mount
from starlette.staticfiles import StaticFiles

from app.http import routes as http_routes
from app.middlewares import PrintClientMiddleware
from app.ws import routes as ws_routes


class State(TypedDict):
    db: Connection


@asynccontextmanager
async def lifespan(app: Starlette) -> AsyncIterator[State]:
    db = sqlite3.connect(Path.cwd() / "db.sqlite")
    yield {"db": db}
    db.close()


SECRET_KEY = "707h2YjMQPk9PiZjyR+syARNKcE+Uop+8Blnm8gIR5o="

app = Starlette(
    lifespan=lifespan,
    middleware=[
        Middleware(PrintClientMiddleware),
        Middleware(CORSMiddleware),
        Middleware(SessionMiddleware, secret_key=SECRET_KEY),
    ],
    routes=[
        *http_routes,
        Mount("/ws", routes=ws_routes, name="ws"),
        Mount("/static", StaticFiles(directory="static", html=True), name="static"),
    ],
)
