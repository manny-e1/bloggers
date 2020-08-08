"""asasa

Revision ID: 3ed31d701c28
Revises: c53293becddc
Create Date: 2020-07-31 15:40:08.171624

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3ed31d701c28'
down_revision = 'c53293becddc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('draft', sa.Column('tag', sa.String(length=20), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('draft', 'tag')
    # ### end Alembic commands ###
