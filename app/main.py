from starlette.responses import HTMLResponse


async def app(scope, receive, send):
    assert scope["type"] == "http"
    if scope["path"] == "/":
        response = HTMLResponse("Hello world!")
    else:
        response = HTMLResponse("Not found", 404)
    await response(scope, receive, send)
