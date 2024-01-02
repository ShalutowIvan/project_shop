"""order_list

Revision ID: c4a0b2568fb6
Revises: e3e65bb1c64a
Create Date: 2024-01-02 07:49:35.886996

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c4a0b2568fb6'
down_revision: Union[str, None] = 'e3e65bb1c64a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('order_list', 'product_name')
    op.create_unique_constraint(None, 'payment', ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'payment', type_='unique')
    op.add_column('order_list', sa.Column('product_name', sa.VARCHAR(), autoincrement=False, nullable=False))
    # ### end Alembic commands ###
