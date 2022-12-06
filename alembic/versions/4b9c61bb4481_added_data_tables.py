"""

Revision ID: 4b9c61bb4481
Revises: 2d898c09b9df
Create Date: 2022-11-30 13:06:47.691109

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4b9c61bb4481'
down_revision = '2d898c09b9df'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('group',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=1), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_index(op.f('ix_group_id'), 'group', ['id'], unique=False)
    op.create_table('country',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('country', sa.String(length=50), nullable=False),
    sa.Column('world_ranking', sa.Integer(), nullable=False),
    sa.Column('tournament_ranking', sa.Integer(), nullable=False),
    sa.Column('group_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['group_id'], ['group.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('country'),
    sa.UniqueConstraint('tournament_ranking'),
    sa.UniqueConstraint('world_ranking')
    )
    op.create_index(op.f('ix_country_id'), 'country', ['id'], unique=False)
    op.create_table('player',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('number', sa.Integer(), nullable=False),
    sa.Column('position', sa.Integer(), nullable=False),
    sa.Column('birth_date', sa.Date(), nullable=False),
    sa.Column('country_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['country_id'], ['country.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_player_id'), 'player', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_player_id'), table_name='player')
    op.drop_table('player')
    op.drop_index(op.f('ix_country_id'), table_name='country')
    op.drop_table('country')
    op.drop_index(op.f('ix_group_id'), table_name='group')
    op.drop_table('group')
    # ### end Alembic commands ###
