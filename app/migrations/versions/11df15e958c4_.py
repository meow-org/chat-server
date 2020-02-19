"""empty message

Revision ID: 11df15e958c4
Revises: 96e0aa576018
Create Date: 2020-02-18 19:42:22.236674

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '11df15e958c4'
down_revision = '96e0aa576018'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'img',
               existing_type=sa.BOOLEAN(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'img',
               existing_type=sa.BOOLEAN(),
               nullable=True)
    # ### end Alembic commands ###
