"""Foreign key for company and user

Revision ID: 5bdfbb5042aa
Revises: eeab63c601c3
Create Date: 2025-09-02 18:36:21.418546

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5bdfbb5042aa'
down_revision: Union[str, Sequence[str], None] = 'eeab63c601c3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column('Company_Info', 'user_id')


def downgrade() -> None:
    op.drop_column('Company_Info', 'user_id')
    pass
