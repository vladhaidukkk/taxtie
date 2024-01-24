from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.routing import Mount
from starlette.staticfiles import StaticFiles

from app import settings
from app.http import routes as http_routes
from app.lifespan import lifespan
from app.middlewares import PrintClientMiddleware
from app.ws import routes as ws_routes

app = Starlette(
    lifespan=lifespan,
    middleware=[
        Middleware(PrintClientMiddleware),
        Middleware(CORSMiddleware),
        Middleware(SessionMiddleware, secret_key=settings.SECRET_KEY),
    ],
    routes=[
        *http_routes,
        Mount("/ws", routes=ws_routes, name="ws"),
        Mount("/static", StaticFiles(directory="static", html=True), name="static"),
    ],
    debug=settings.DEBUG,
)
