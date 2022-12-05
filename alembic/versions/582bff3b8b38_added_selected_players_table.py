"""added selected players table

Revision ID: 582bff3b8b38
Revises: 48443153bee8
Create Date: 2022-12-05 11:51:31.236905

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '582bff3b8b38'
down_revision = '48443153bee8'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('selectedplayers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('player_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['player_id'], ['player.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_selectedplayers_id'), 'selectedplayers', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_selectedplayers_id'), table_name='selectedplayers')
    op.drop_table('selectedplayers')
    # ### end Alembic commands ###
