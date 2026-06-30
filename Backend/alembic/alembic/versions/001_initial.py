"""Initial schema

Revision ID: 001_initial
Revises:
Create Date: 2026-06-15

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "001_initial"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Tables are created via Base.metadata.create_all on startup.
    # Run `alembic revision --autogenerate -m "description"` against a live DB
    # to generate incremental migrations from model changes.
    pass


def downgrade() -> None:
    pass
