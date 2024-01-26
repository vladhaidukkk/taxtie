from starlette.authentication import (
    AuthCredentials,
    AuthenticationBackend,
    AuthenticationError,
    BaseUser,
    requires,
)
from starlette.endpoints import HTTPEndpoint
from starlette.exceptions import HTTPException
from starlette.requests import HTTPConnection, Request
from starlette.responses import PlainTextResponse
from starlette.routing import Route

from app.db import db, users


class User(BaseUser):
    def __init__(self, id: int, username: str):
        self.id = id
        self.username = username

    @property
    def is_authenticated(self):
        return True

    @property
    def display_name(self):
        return self.username


class SessionAuthBackend(AuthenticationBackend):
    async def authenticate(self, conn: HTTPConnection):
        user_id = conn.session.get("id")
        if not user_id:
            return

        query = users.select().filter_by(id=user_id)
        result = await db.fetch_one(query)

        if not result:
            raise AuthenticationError("Invalid credentials")

        return AuthCredentials(["authenticated"]), User(result["id"], result["username"]
                                                        )


class Register(HTTPEndpoint):
    @db.transaction()
    async def post(self, request: Request):
        data = await request.json()

        if "username" not in data:
            return PlainTextResponse("'username' is required", 422)
        if "password" not in data:
            return PlainTextResponse("'password' is required", 422)

        query = users.insert().values(
            username=data["username"], password=data["password"],
        )
        await db.execute(query)

        return PlainTextResponse(
            f"user {data["username"]} is successfully registered",
            201,
        )


class Login(HTTPEndpoint):
    async def post(self, request: Request):
        data = await request.json()

        if "username" not in data:
            return PlainTextResponse("'username' is required", 422)
        if "password" not in data:
            return PlainTextResponse("'password' is required", 422)

        query = users.select().filter_by(username=data["username"])
        result = await db.fetch_one(query)

        if not result or result["password"] != data["password"]:
            raise HTTPException(401, "Invalid 'username' or 'password'")

        request.scope["session"] = {
            "id": result["id"],
            "username": result["username"],
        }
        return PlainTextResponse(f"Welcome, {result[1]}!", 200)


class Me(HTTPEndpoint):
    @requires(["authenticated"])
    def get(self, request: Request):
        return PlainTextResponse(
            f"ID: {request.user.id}, Username: {request.user.username}"
        )


routes = [
    Route("/register", Register),
    Route("/login", Login),
    Route("/me", Me),
]
