"""Create users table

Revision ID: 56e16b51ce94
Revises: 616165f956df
Create Date: 2024-01-26 16:28:55.026692

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "56e16b51ce94"
down_revision: Union[str, None] = "616165f956df"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("username", sa.String, unique=True, nullable=False),
        sa.Column("password", sa.String, nullable=False),
    )


def downgrade() -> None:
    op.drop_table("users")
