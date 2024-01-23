from starlette.requests import Request
from starlette.responses import PlainTextResponse
from starlette.routing import Route

from app.db import execute_query


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


routes = [Route("/register", register, methods=["POST"])]
