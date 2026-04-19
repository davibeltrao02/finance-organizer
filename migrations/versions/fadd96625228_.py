"""empty message

Revision ID: fadd96625228
Revises: e855e7d7a0ef
Create Date: 2026-04-19 15:24:51.554311

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fadd96625228'
down_revision: Union[str, None] = 'e855e7d7a0ef'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
