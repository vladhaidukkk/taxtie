from starlette.routing import WebSocketRoute
from starlette.websockets import WebSocket


async def index(websocket: WebSocket):
    await websocket.accept()
    async for text in websocket.iter_text():
        await websocket.send_text(f"Reply: {text}")
    print("Disconnected by", websocket.client)
    await websocket.close()


routes = [WebSocketRoute("/", index)]
