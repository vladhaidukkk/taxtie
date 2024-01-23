from starlette.endpoints import WebSocketEndpoint
from starlette.routing import WebSocketRoute
from starlette.websockets import WebSocket


class Index(WebSocketEndpoint):
    encoding = "text"

    async def on_connect(self, websocket: WebSocket):
        await websocket.accept()

    async def on_receive(self, websocket: WebSocket, data: str):
        await websocket.send_text(f"Reply: {data}")

    async def on_disconnect(self, websocket: WebSocket, close_code: int):
        print("Disconnected by", websocket.client)
        await websocket.close()


routes = [WebSocketRoute("/", Index)]
