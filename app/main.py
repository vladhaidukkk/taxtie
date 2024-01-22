import json
import sqlite3
from pathlib import Path


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
    else:
        assert scope["type"] == "http"
        content_type = next(
            (value for header, value in scope["headers"] if header == b"content-type"),
            None,
        )
        assert content_type == b"application/json"
        db = scope["state"]["db"]

        msg = await receive()
        data = json.loads(msg["body"])

        if "username" in data and "password" in data:
            cur = db.cursor()
            cur.execute(
                "INSERT INTO user (username, password) VALUES (?, ?)",
                (data["username"], data["password"]),
            )
            db.commit()
            cur.close()

            status = 201
            response = b"user is successfully registered"
        else:
            status = 422
            response = b"'username' and 'password' are required"

        await send(
            {
                "type": "http.response.start",
                "status": status,
                "headers": [(b"content-type", b"text/plain")],
            }
        )
        await send(
            {
                "type": "http.response.body",
                "body": response,
                "more_body": False,
            }
        )
