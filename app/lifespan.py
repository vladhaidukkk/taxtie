from contextlib import asynccontextmanager
from typing import AsyncIterator, TypedDict

from databases import Database
from starlette.applications import Starlette

from app.db import db


class State(TypedDict):
    db: Database


@asynccontextmanager
async def lifespan(app: Starlette) -> AsyncIterator[State]:
    await db.connect()
    yield {"db": db}
    await db.disconnect()
