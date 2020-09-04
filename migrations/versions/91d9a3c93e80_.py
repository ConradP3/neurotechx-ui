"""empty message

Revision ID: 91d9a3c93e80
Revises: 335c946fe62d
Create Date: 2020-09-04 13:12:57.281027

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '91d9a3c93e80'
down_revision = '335c946fe62d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('trial',
    sa.Column('trial_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('question', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('trial_id')
    )
    op.drop_table('trail')
    #op.drop_table('sqlite_sequence')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    #op.create_table('sqlite_sequence',
    #sa.Column('name', sa.NullType(), nullable=True),
    #sa.Column('seq', sa.NullType(), nullable=True)
    #)
    op.create_table('trail',
    sa.Column('trail_id', sa.INTEGER(), nullable=False),
    sa.Column('question', sa.VARCHAR(length=50), nullable=True),
    sa.Column('word', sa.VARCHAR(length=50), nullable=True),
    sa.PrimaryKeyConstraint('trail_id')
    )
    op.drop_table('trial')
    # ### end Alembic commands ###
