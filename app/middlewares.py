from starlette.types import ASGIApp, Receive, Scope, Send


class PrintClientMiddleware:
    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if scope["type"] in ("http", "websocket"):
            print("Connected by", scope["client"])
        await self.app(scope, receive, send)
