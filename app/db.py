import sqlalchemy as sa
from databases import Database

from app import settings

db = Database(settings.DATABASE_URL)

metadata = sa.MetaData()

users = sa.Table(
    "users",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("username", sa.String, unique=True, nullable=False),
    sa.Column("password", sa.String, nullable=False),
)

notes = sa.Table(
    "notes",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("title", sa.String),
    sa.Column("body", sa.String),
)
