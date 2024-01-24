from starlette.endpoints import HTTPEndpoint
from starlette.requests import Request
from starlette.routing import Mount, Route

from app.auth import routes as auth_routes
from app.templating import templates


class Index(HTTPEndpoint):
    def get(self, request: Request):
        return templates.TemplateResponse(request, "index.html")


routes = [
    Route("/", Index),
    Mount("/auth", routes=auth_routes, name="auth"),
]
