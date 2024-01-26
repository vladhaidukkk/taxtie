from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.routing import Mount
from starlette.staticfiles import StaticFiles
from strawberry.asgi import GraphQL

from app import settings
from app.auth import SessionAuthBackend
from app.http import routes as http_routes
from app.lifespan import lifespan
from app.middlewares import PrintClientMiddleware
from app.schema import schema
from app.ws import routes as ws_routes

app = Starlette(
    lifespan=lifespan,
    middleware=[
        Middleware(PrintClientMiddleware),
        Middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"]),
        Middleware(SessionMiddleware, secret_key=settings.SECRET_KEY),
        Middleware(AuthenticationMiddleware, backend=SessionAuthBackend()),
    ],
    routes=[
        *http_routes,
        Mount("/graphql", GraphQL(schema)),
        Mount("/ws", routes=ws_routes, name="ws"),
        Mount("/static", StaticFiles(directory="static", html=True), name="static"),
    ],
    debug=settings.DEBUG,
)
