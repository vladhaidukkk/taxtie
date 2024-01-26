from contextlib import contextmanager
from sqlite3 import Connection

import sqlalchemy
from databases import Database

from app import settings

db = Database(settings.DATABASE_URL)

metadata = sqlalchemy.MetaData()

notes = sqlalchemy.Table(
    "notes",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("title", sqlalchemy.String),
    sqlalchemy.Column("body", sqlalchemy.String),
)


@contextmanager
def execute_query(conn: Connection, query: str, params=()):
    cur = conn.cursor()
    try:
        cur.execute(query, params)
        conn.commit()
        yield cur
    finally:
        cur.close()
