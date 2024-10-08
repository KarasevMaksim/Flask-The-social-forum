"""first table

Revision ID: e83571c3322f
Revises: 
Create Date: 2024-08-10 21:11:06.401344

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e83571c3322f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('section',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=30), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('username', sa.String(length=20), nullable=True),
    sa.Column('email', sa.String(length=30), nullable=True),
    sa.Column('password', sa.String(length=256), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_user_timestamp'), ['timestamp'], unique=False)
        batch_op.create_index(batch_op.f('ix_user_username'), ['username'], unique=True)

    op.create_table('usercontent',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=20), nullable=True),
    sa.Column('link', sa.String(length=100), nullable=True),
    sa.Column('is_private', sa.Boolean(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('section_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['section_id'], ['section.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('usercontent', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_usercontent_name'), ['name'], unique=False)
        batch_op.create_index(batch_op.f('ix_usercontent_timestamp'), ['timestamp'], unique=False)
        batch_op.create_index(batch_op.f('ix_usercontent_user_id'), ['user_id'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('usercontent', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_usercontent_user_id'))
        batch_op.drop_index(batch_op.f('ix_usercontent_timestamp'))
        batch_op.drop_index(batch_op.f('ix_usercontent_name'))

    op.drop_table('usercontent')
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_user_username'))
        batch_op.drop_index(batch_op.f('ix_user_timestamp'))

    op.drop_table('user')
    op.drop_table('section')
    # ### end Alembic commands ###
