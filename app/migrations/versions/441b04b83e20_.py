"""empty message

Revision ID: 441b04b83e20
Revises: b1c94a23184d
Create Date: 2020-02-18 20:35:18.439744

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '441b04b83e20'
down_revision = 'b1c94a23184d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('img', sa.String(length=128), nullable=True))
    op.drop_column('user', 'image')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('image', sa.VARCHAR(length=128), autoincrement=False, nullable=False))
    op.drop_column('user', 'img')
    # ### end Alembic commands ###