"""draft

Revision ID: b92502dc6dc1
Revises: 2eefc7483efb
Create Date: 2020-05-31 20:48:57.008574

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b92502dc6dc1'
down_revision = '2eefc7483efb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('draft',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('description', sa.String(length=300), nullable=False),
    sa.Column('cover_image', sa.String(length=20), nullable=False),
    sa.Column('date_posted', sa.DateTime(), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('draft')
    # ### end Alembic commands ###