"""product in order_list not foreignkey 2

Revision ID: 84e954a9dc18
Revises: 57faeb6dabe5
Create Date: 2024-03-29 15:59:35.197908

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '84e954a9dc18'
down_revision: Union[str, None] = '57faeb6dabe5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###