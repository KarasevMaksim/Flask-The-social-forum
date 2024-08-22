"""add_content_links

Revision ID: 1e6c733b7acd
Revises: d4a4853661d9
Create Date: 2024-08-18 03:03:50.466215

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1e6c733b7acd'
down_revision = 'd4a4853661d9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('link_content',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=30), nullable=True),
    sa.Column('content_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['content_id'], ['usercontent.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('link_content', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_link_content_content_id'), ['content_id'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('link_content', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_link_content_content_id'))

    op.drop_table('link_content')
    # ### end Alembic commands ###
