from starlette.endpoints import HTTPEndpoint
from starlette.requests import Request
from starlette.responses import PlainTextResponse
from starlette.routing import Mount, Route
from starlette.schemas import SchemaGenerator

from app.auth import routes as auth_routes
from app.db import db, notes
from app.templating import templates

schema = SchemaGenerator(
    {"openapi": "3.0.0", "info": {"title": "RESTful API", "version": "0.1.0"}}
)


class Index(HTTPEndpoint):
    async def get(self, request: Request):
        """
        responses:
          200:
            description: Index page.
        """
        query = notes.select()
        results = await db.fetch_all(query)
        content = [
            {
                "id": result["id"],
                "title": result["title"],
                "body": result["body"],
            }
            for result in results
        ]
        return templates.TemplateResponse(
            request, "index.html", context={"notes": content}
        )

    @db.transaction()
    async def post(self, request: Request):
        data = await request.json()
        query = notes.insert().values(
            title=data["title"],
            body=data["body"],
        )
        await db.execute(query)
        return PlainTextResponse("note created")


def openapi_schema(request: Request):
    return schema.OpenAPIResponse(request)


routes = [
    Route("/", Index),
    Mount("/auth", routes=auth_routes, name="auth"),
    Route("/schema", openapi_schema, include_in_schema=False),
]
