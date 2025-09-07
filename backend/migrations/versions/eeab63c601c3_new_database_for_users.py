"""New database for users

Revision ID: eeab63c601c3
Revises: 
Create Date: 2025-09-02 14:39:36.117176

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'eeab63c601c3'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
         'users',
        sa.Column('id',sa.Integer, primary_key =True),
        sa.Column('username', sa.String(100), nullable = False, unique = True),
        sa.Column('email', sa.String(150), nullable = False, unique = True),
        sa.Column('hashed_password', sa.String(255), nullable = False),
        )


def downgrade() -> None:
    """Downgrade schema."""
    pass
