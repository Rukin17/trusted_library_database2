"""2 migration

Revision ID: 064a3ff2c3d7
Revises: 8a7280543e0f
Create Date: 2024-02-09 16:04:13.953401

"""
from typing import Sequence
from typing import Union

import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision: str = '064a3ff2c3d7'
down_revision: Union[str, None] = '8a7280543e0f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('roles', sa.Column('registered_at', sa.TIMESTAMP(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('roles', 'registered_at')
    # ### end Alembic commands ###
