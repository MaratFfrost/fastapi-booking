"""create new_table

Revision ID: 6da58a22ac25
Revises: 4fa5edc2bf5f
Create Date: 2024-10-04 17:53:15.235601

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6da58a22ac25'
down_revision: Union[str, None] = '4fa5edc2bf5f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
