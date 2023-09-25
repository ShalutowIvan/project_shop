"""Database creation

Revision ID: 38c62b6ab9f1
Revises: 
Create Date: 2023-09-24 15:59:49.643022

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '38c62b6ab9f1'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('group',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name_group', sa.String(), nullable=False),
                    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('order_list',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('buyer', sa.Text(), nullable=False),
                    sa.Column('name_product', sa.String(), nullable=False),
                    sa.Column('quantity', sa.Float(), nullable=False),
                    sa.Column('order_number', sa.Integer(), nullable=False),
                    sa.Column('time_create', sa.TIMESTAMP(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('organization',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name_org', sa.String(), nullable=False),
                    sa.Column('inn', sa.Integer(), nullable=True),
                    sa.Column('kpp', sa.Integer(), nullable=True),
                    sa.Column('ogrn', sa.Integer(), nullable=True),
                    sa.Column('working_mode', sa.String(), nullable=True),
                    sa.Column('about', sa.Text(), nullable=True),
                    sa.Column('adres', sa.String(), nullable=True),
                    sa.Column('phone', sa.Integer(), nullable=True),
                    sa.Column('email_name', sa.String(), nullable=False),
                    sa.Column('telegram', sa.String(), nullable=True),
                    sa.Column('whatsApp', sa.String(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('goods',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name_product', sa.String(), nullable=False),
                    sa.Column('vendor_code', sa.String(), nullable=False),
                    sa.Column('stock', sa.Float(), nullable=True),
                    sa.Column('photo', sa.String(), nullable=False),
                    sa.Column('availability', sa.Boolean(), nullable=False),
                    sa.Column('time_create', sa.TIMESTAMP(), nullable=True),
                    sa.Column('name_group', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(['name_group'], ['group.id'], ),
                    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('goods')
    op.drop_table('organization')
    op.drop_table('order_list')
    op.drop_table('group')
    # ### end Alembic commands ###