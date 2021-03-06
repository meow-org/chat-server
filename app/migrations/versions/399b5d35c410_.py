"""empty message

Revision ID: 399b5d35c410
Revises: 9cd119608f8c
Create Date: 2020-03-01 07:33:25.316404

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '399b5d35c410'
down_revision = '9cd119608f8c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('message', sa.Column('date', sa.DateTime(), nullable=False))
    op.drop_column('message', 'data')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('message', sa.Column('data', postgresql.TIMESTAMP(), autoincrement=False, nullable=False))
    op.drop_column('message', 'date')
    # ### end Alembic commands ###
