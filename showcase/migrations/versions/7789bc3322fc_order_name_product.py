"""order_name_product

Revision ID: 7789bc3322fc
Revises: 625c5a7a3eca
Create Date: 2023-12-12 01:51:09.332350

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7789bc3322fc'
down_revision: Union[str, None] = '625c5a7a3eca'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('order_list', sa.Column('product_name', sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('order_list', 'product_name')
    # ### end Alembic commands ###
