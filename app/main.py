import sqlite3
from pathlib import Path

from starlette.requests import Request
from starlette.responses import PlainTextResponse
from starlette.websockets import WebSocket, WebSocketDisconnect


async def app(scope, receive, send):
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
        request = Request(scope, receive)
        assert request.headers["content-type"] == "application/json", request.headers[
            "content-type"
        ]
        data = await request.json()

        if "username" in data and "password" in data:
            cur = request.state.db.cursor()
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS user (
                    id INTEGER PRIMARY KEY,
                    username TEXT NOT NULL,
                    password TEXT NOT NULL
                )
                """
            )
            cur.execute(
                "INSERT INTO user (username, password) VALUES (?, ?)",
                (data["username"], data["password"]),
            )
            request.state.db.commit()
            cur.close()

            response = PlainTextResponse("user is successfully registered", 201)
        else:
            response = PlainTextResponse("'username' and 'password' are required", 422)

        await response(scope, receive, send)
    else:
        websocket = WebSocket(scope, receive, send)
        await websocket.accept()
        while True:
            try:
                text = await websocket.receive_text()
            except WebSocketDisconnect:
                break
            else:
                await websocket.send_text(f"Reply: {text}")
        print("Disconnected by", websocket.client)
        await websocket.close()
