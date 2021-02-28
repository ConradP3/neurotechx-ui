"""empty message

Revision ID: 12b8c95c59d6
Revises: 91d9a3c93e80
Create Date: 2021-02-28 11:58:14.703872

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '12b8c95c59d6'
down_revision = '91d9a3c93e80'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('answer',
    sa.Column('answer_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('trail_number', sa.Integer(), nullable=True),
    sa.Column('answer', sa.String(length=100), nullable=True),
    sa.Column('correction', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['trail_number'], ['trial.trial_id'], ),
    sa.PrimaryKeyConstraint('answer_id')
    )
    # op.drop_table('sqlite_sequence')
    op.create_foreign_key(None, 'model_response', 'answer', ['expected_response'], ['answer_id'])
    op.create_foreign_key(None, 'model_response', 'answer', ['recorded_response'], ['answer_id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'model_response', type_='foreignkey')
    op.drop_constraint(None, 'model_response', type_='foreignkey')
    # op.create_table('sqlite_sequence',
    # sa.Column('name', sa.NullType(), nullable=True),
    # sa.Column('seq', sa.NullType(), nullable=True)
    # )
    op.drop_table('answer')
    # ### end Alembic commands ###
