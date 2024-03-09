"""pay_modify

Revision ID: ded4014f1ba4
Revises: 6190fc616328
Create Date: 2024-02-15 10:20:48.888333

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ded4014f1ba4'
down_revision: Union[str, None] = '6190fc616328'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'payment', ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'payment', type_='unique')
    # ### end Alembic commands ###