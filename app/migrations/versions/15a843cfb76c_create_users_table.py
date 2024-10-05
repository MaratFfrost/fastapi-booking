"""create users table

Revision ID: 15a843cfb76c
Revises: 6da58a22ac25
Create Date: 2024-10-04 17:57:16.645137

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '15a843cfb76c'
down_revision: Union[str, None] = '6da58a22ac25'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
