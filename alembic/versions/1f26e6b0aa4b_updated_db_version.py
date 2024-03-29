"""

Revision ID: 1f26e6b0aa4b
Revises: 
Create Date: 2022-12-08 15:15:38.682278

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1f26e6b0aa4b'
down_revision = None
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
    op.create_table('lineuplimits',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('gk', sa.Integer(), nullable=False),
    sa.Column('df', sa.Integer(), nullable=False),
    sa.Column('mf', sa.Integer(), nullable=False),
    sa.Column('fw', sa.Integer(), nullable=False),
    sa.Column('lineup_status', sa.String(length=10), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('lineup_status')
    )
    op.create_index(op.f('ix_lineuplimits_id'), 'lineuplimits', ['id'], unique=False)
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('email', sa.String(length=50), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('role', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('name')
    )
    op.create_index(op.f('ix_user_id'), 'user', ['id'], unique=False)
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
    op.create_table('match',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('confirmed', sa.Boolean(), nullable=False),
    sa.Column('home_score', sa.Integer(), nullable=True),
    sa.Column('away_score', sa.Integer(), nullable=True),
    sa.Column('home_team_id', sa.Integer(), nullable=True),
    sa.Column('away_team_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['away_team_id'], ['country.id'], ),
    sa.ForeignKeyConstraint(['home_team_id'], ['country.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_match_id'), 'match', ['id'], unique=False)
    op.create_table('player',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('number', sa.Integer(), nullable=False),
    sa.Column('position', sa.String(), nullable=False),
    sa.Column('birth_date', sa.Date(), nullable=False),
    sa.Column('country_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['country_id'], ['country.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_player_id'), 'player', ['id'], unique=False)
    op.create_table('goalsscored',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('number_of_goals', sa.Integer(), nullable=False),
    sa.Column('match_id', sa.Integer(), nullable=True),
    sa.Column('player_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['match_id'], ['match.id'], ),
    sa.ForeignKeyConstraint(['player_id'], ['player.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_goalsscored_id'), 'goalsscored', ['id'], unique=False)
    op.create_table('points',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('number_of_points', sa.Integer(), nullable=False),
    sa.Column('match_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['match_id'], ['match.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_points_id'), 'points', ['id'], unique=False)
    op.create_table('selectedplayers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('active', sa.Boolean(), nullable=False),
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
    op.drop_index(op.f('ix_points_id'), table_name='points')
    op.drop_table('points')
    op.drop_index(op.f('ix_goalsscored_id'), table_name='goalsscored')
    op.drop_table('goalsscored')
    op.drop_index(op.f('ix_player_id'), table_name='player')
    op.drop_table('player')
    op.drop_index(op.f('ix_match_id'), table_name='match')
    op.drop_table('match')
    op.drop_index(op.f('ix_country_id'), table_name='country')
    op.drop_table('country')
    op.drop_index(op.f('ix_user_id'), table_name='user')
    op.drop_table('user')
    op.drop_index(op.f('ix_lineuplimits_id'), table_name='lineuplimits')
    op.drop_table('lineuplimits')
    op.drop_index(op.f('ix_group_id'), table_name='group')
    op.drop_table('group')
    # ### end Alembic commands ###
