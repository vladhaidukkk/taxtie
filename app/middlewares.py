from starlette.exceptions import HTTPException
from starlette.types import ASGIApp, Receive, Scope, Send

from app.db import execute_query


class PrintClientMiddleware:
    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if scope["type"] in ("http", "websocket"):
            print("Connected by", scope["client"])
        await self.app(scope, receive, send)


class SessionAuthMiddleware:
    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        session = scope["session"]
        if not session:
            raise HTTPException(403, "You're not logged in")

        with execute_query(
            scope["state"]["db"],
            "SELECT * FROM user WHERE id = ?",
            (session["id"],),
        ) as cur:
            user = cur.fetchone()

        if not user:
            raise HTTPException(403, "You're not logged in")

        scope["user"] = {
            "id": user[0],
            "username": user[1],
            "password": user[2],
        }
        await self.app(scope, receive, send)
