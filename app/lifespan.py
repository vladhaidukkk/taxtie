import sqlite3
from contextlib import asynccontextmanager
from pathlib import Path
from sqlite3 import Connection
from typing import AsyncIterator, TypedDict

from starlette.applications import Starlette


class State(TypedDict):
    db: Connection


@asynccontextmanager
async def lifespan(app: Starlette) -> AsyncIterator[State]:
    db = sqlite3.connect(Path.cwd() / "db.sqlite")
    yield {"db": db}
    db.close()
