"""empty message

Revision ID: d2fe341180a2
Revises: 522298a90a93
Create Date: 2020-01-29 11:29:52.361563

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd2fe341180a2'
down_revision = '522298a90a93'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('online', sa.Boolean(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'online')
    # ### end Alembic commands ###
