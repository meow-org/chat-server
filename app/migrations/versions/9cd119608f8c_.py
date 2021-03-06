"""empty message

Revision ID: 9cd119608f8c
Revises: ce0b7b411fc2
Create Date: 2020-02-27 12:46:28.523803

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9cd119608f8c'
down_revision = 'ce0b7b411fc2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('message', sa.Column('text', sa.Text(), nullable=False))
    op.drop_column('message', 'text1')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('message', sa.Column('text1', sa.TEXT(), autoincrement=False, nullable=False))
    op.drop_column('message', 'text')
    # ### end Alembic commands ###
