"""teg_test2

Revision ID: d4a4853661d9
Revises: 92dd83fc4148
Create Date: 2024-08-18 00:19:53.770617

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd4a4853661d9'
down_revision = '92dd83fc4148'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tag',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=20), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('tag', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_tag_name'), ['name'], unique=False)

    op.create_table('tag_or_content',
    sa.Column('tags_id', sa.Integer(), nullable=False),
    sa.Column('contents_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['contents_id'], ['usercontent.id'], ),
    sa.ForeignKeyConstraint(['tags_id'], ['tag.id'], ),
    sa.PrimaryKeyConstraint('tags_id', 'contents_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tag_or_content')
    with op.batch_alter_table('tag', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_tag_name'))

    op.drop_table('tag')
    # ### end Alembic commands ###
