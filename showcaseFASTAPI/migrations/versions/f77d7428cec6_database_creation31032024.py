"""Database creation31032024

Revision ID: f77d7428cec6
Revises: 
Create Date: 2024-03-31 06:42:38.340783

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f77d7428cec6'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('group',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name_group', sa.String(), nullable=False),
    sa.Column('slug', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('order_counter',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('organization',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name_org', sa.String(), nullable=False),
    sa.Column('inn', sa.Integer(), nullable=False),
    sa.Column('kpp', sa.Integer(), nullable=False),
    sa.Column('ogrn', sa.Integer(), nullable=False),
    sa.Column('working_mode', sa.String(), nullable=False),
    sa.Column('about', sa.String(), nullable=False),
    sa.Column('adres', sa.String(), nullable=False),
    sa.Column('phone', sa.Integer(), nullable=False),
    sa.Column('email_name', sa.String(), nullable=False),
    sa.Column('telegram', sa.String(), nullable=False),
    sa.Column('whatsApp', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=256), nullable=False),
    sa.Column('time_create_user', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', now())"), nullable=False),
    sa.Column('email', sa.String(length=320), nullable=False),
    sa.Column('hashed_password', sa.String(length=1024), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_id'), 'user', ['id'], unique=False)
    op.create_table('goods',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name_product', sa.String(), nullable=False),
    sa.Column('price', sa.Float(), nullable=False),
    sa.Column('vendor_code', sa.String(), nullable=False),
    sa.Column('stock', sa.Float(), nullable=True),
    sa.Column('slug', sa.String(), nullable=False),
    sa.Column('photo', sa.String(), nullable=False),
    sa.Column('availability', sa.Boolean(), nullable=False),
    sa.Column('time_create', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', now())"), nullable=False),
    sa.Column('group_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['group_id'], ['group.id'], ondelete='RESTRICT'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('token',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('refresh_token', sa.String(length=320), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_token_id'), 'token', ['id'], unique=False)
    op.create_index(op.f('ix_token_refresh_token'), 'token', ['refresh_token'], unique=True)
    op.create_table('basket',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('quantity', sa.Float(), server_default='1', nullable=False),
    sa.Column('created_timestamp', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', now())"), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['product_id'], ['goods.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('order_list',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('order_number', sa.Integer(), nullable=False),
    sa.Column('fio', sa.String(), nullable=False),
    sa.Column('delivery_address', sa.String(), nullable=False),
    sa.Column('phone', sa.String(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=True),
    sa.Column('quantity', sa.Float(), nullable=False),
    sa.Column('time_create', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', now())"), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('state', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['product_id'], ['goods.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('order_list')
    op.drop_table('basket')
    op.drop_index(op.f('ix_token_refresh_token'), table_name='token')
    op.drop_index(op.f('ix_token_id'), table_name='token')
    op.drop_table('token')
    op.drop_table('goods')
    op.drop_index(op.f('ix_user_id'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_table('organization')
    op.drop_table('order_counter')
    op.drop_table('group')
    # ### end Alembic commands ###
