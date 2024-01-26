import asyncio

from starlette.background import BackgroundTask
from starlette.endpoints import HTTPEndpoint
from starlette.exceptions import HTTPException
from starlette.middleware import Middleware
from starlette.requests import Request
from starlette.responses import PlainTextResponse
from starlette.routing import Route

from app.db import execute_query
from app.middlewares import SessionAuthMiddleware


async def print_new_user(username: str):
    await asyncio.sleep(1)
    print(f"{username} was registered")


class Register(HTTPEndpoint):
    async def post(self, request: Request):
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

        task = BackgroundTask(print_new_user, username=user[1])
        return PlainTextResponse(
            f"user {user[:2]} is successfully registered",
            201,
            background=task,
        )


class Login(HTTPEndpoint):
    async def post(self, request: Request):
        db = request.state.db
        data = await request.json()

        if "username" not in data:
            return PlainTextResponse("'username' is required", 422)
        if "password" not in data:
            return PlainTextResponse("'password' is required", 422)

        with execute_query(
            db,
            "SELECT * FROM user WHERE username = ?",
            (data["username"],),
        ) as cur:
            user = cur.fetchone()

        if not user or user[2] != data["password"]:
            raise HTTPException(401, "Invalid 'username' or 'password'")

        request.scope["session"] = {
            "id": user[0],
            "username": user[1],
        }
        return PlainTextResponse(f"Welcome, {user[1]}!", 200)


class Me(HTTPEndpoint):
    def get(self, request: Request):
        user = request.scope["user"]
        return PlainTextResponse(f"ID: {user["id"]}, Username: {user["username"]}")


routes = [
    Route("/register", Register),
    Route("/login", Login),
    Route("/me", Me, middleware=[Middleware(SessionAuthMiddleware)]),
]
