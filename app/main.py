import sqlite3
from contextlib import contextmanager
from pathlib import Path
from sqlite3 import Connection

from starlette.requests import Request
from starlette.responses import PlainTextResponse
from starlette.routing import Mount, Route, Router
from starlette.types import Receive, Scope, Send
from starlette.websockets import WebSocket


@contextmanager
def execute_query(conn: Connection, query: str, params=()):
    cur = conn.cursor()
    try:
        cur.execute(query, params)
        conn.commit()
        yield cur
    finally:
        cur.close()


def index(request: Request):
    return PlainTextResponse("Hello world!")


async def register(request: Request):
    db = request.state.db
    data = await request.json()

    if "username" not in data:
        return PlainTextResponse("'username' is required", 422)
    if "password" not in data:
        return PlainTextResponse("'password' is required", 422)

    with execute_query(
        db,
        """
        CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
        """,
    ):
        pass

    with execute_query(
        db,
        "INSERT INTO user (username, password) VALUES (?, ?)",
        (data["username"], data["password"]),
    ) as cur:
        cur.execute("SELECT * FROM user ORDER BY id DESC LIMIT 1")
        user = cur.fetchone()

    return PlainTextResponse(f"user {user[:2]} is successfully registered", 201)


async def app(scope: Scope, receive: Receive, send: Send):
    if scope["type"] == "lifespan":
        while True:
            msg = await receive()
            if msg["type"] == "lifespan.startup":
                scope["state"]["db"] = sqlite3.connect(Path.cwd() / "db.sqlite")
                await send({"type": "lifespan.startup.complete"})
            elif msg["type"] == "lifespan.shutdown":
                scope["state"]["db"].close()
                await send({"type": "lifespan.shutdown.complete"})
                break
    elif scope["type"] == "http":
        router = Router(
            routes=[
                Route("/", index),
                Mount(
                    "/auth",
                    routes=[
                        Route("/register", register, methods=["POST"]),
                    ],
                ),
            ]
        )
        await router(scope, receive, send)
    else:
        websocket = WebSocket(scope, receive, send)
        await websocket.accept()
        async for text in websocket.iter_text():
            await websocket.send_text(f"Reply: {text}")
        print("Disconnected by", websocket.client)
        await websocket.close()
