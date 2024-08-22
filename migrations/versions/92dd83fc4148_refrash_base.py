"""refrash, base

Revision ID: 92dd83fc4148
Revises: 84b34edb6d7f
Create Date: 2024-08-17 23:37:52.078667

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '92dd83fc4148'
down_revision = '84b34edb6d7f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('section', schema=None) as batch_op:
        batch_op.alter_column('name',
               existing_type=mysql.VARCHAR(length=30),
               nullable=False)

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('username',
               existing_type=mysql.VARCHAR(length=20),
               nullable=False)
        batch_op.alter_column('email',
               existing_type=mysql.VARCHAR(length=30),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('email',
               existing_type=mysql.VARCHAR(length=30),
               nullable=True)
        batch_op.alter_column('username',
               existing_type=mysql.VARCHAR(length=20),
               nullable=True)

    with op.batch_alter_table('section', schema=None) as batch_op:
        batch_op.alter_column('name',
               existing_type=mysql.VARCHAR(length=30),
               nullable=True)

    # ### end Alembic commands ###
