"""Create notes table

Revision ID: 616165f956df
Revises:
Create Date: 2024-01-26 13:18:43.168197

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "616165f956df"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "notes",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("title", sa.String),
        sa.Column("body", sa.String),
    )


def downgrade() -> None:
    op.drop_table("notes")
