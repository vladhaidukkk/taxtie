from starlette.applications import Starlette
from starlette.responses import HTMLResponse
from starlette.routing import Route


def index(request):
    return HTMLResponse("Hello world!")


app = Starlette(
    debug=True,
    routes=[Route("/", index)],
)
