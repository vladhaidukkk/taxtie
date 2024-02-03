from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import PlainTextResponse
from starlette.routing import Route

from app.config import DEBUG


def index(request: Request):
    return PlainTextResponse("Hello world!")


app = Starlette(routes=[Route("/", index)], debug=DEBUG)
