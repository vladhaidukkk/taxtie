from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.routing import Mount, Route
from starlette.staticfiles import StaticFiles

from app import settings
from app.graphql import endpoint as graphql_endpoint
from app.http import routes as http_routes
from app.lifespan import lifespan
from app.middlewares import PrintClientMiddleware
from app.ws import routes as ws_routes

app = Starlette(
    lifespan=lifespan,
    middleware=[
        Middleware(PrintClientMiddleware),
        Middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"]),
        Middleware(SessionMiddleware, secret_key=settings.SECRET_KEY),
    ],
    routes=[
        *http_routes,
        Route("/graphql", graphql_endpoint, methods=["POST"]),
        Mount("/ws", routes=ws_routes, name="ws"),
        Mount("/static", StaticFiles(directory="static", html=True), name="static"),
    ],
    debug=settings.DEBUG,
)
