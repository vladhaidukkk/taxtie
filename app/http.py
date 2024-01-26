from starlette.endpoints import HTTPEndpoint
from starlette.requests import Request
from starlette.routing import Mount, Route
from starlette.schemas import SchemaGenerator

from app.auth import routes as auth_routes
from app.templating import templates

schema = SchemaGenerator(
    {"openapi": "3.0.0", "info": {"title": "RESTful API", "version": "0.1.0"}}
)


class Index(HTTPEndpoint):
    def get(self, request: Request):
        """
        responses:
          200:
            description: Index page.
        """
        return templates.TemplateResponse(request, "index.html")


def openapi_schema(request: Request):
    return schema.OpenAPIResponse(request)


routes = [
    Route("/", Index),
    Mount("/auth", routes=auth_routes, name="auth"),
    Route("/schema", openapi_schema, include_in_schema=False),
]
