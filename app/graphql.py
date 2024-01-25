import re

from starlette.requests import Request
from starlette.responses import JSONResponse


async def endpoint(request: Request):
    data = await request.json()
    query = "".join(
        re.sub(r"\s{2,}", " ", line)
        for line in data["query"].splitlines()
        if line and not line.startswith("#")
    )
    return JSONResponse({"query": query})
