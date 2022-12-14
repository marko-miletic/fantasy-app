"""add league user connection approved status

Revision ID: ca71410ed48d
Revises: e2069e7ab78f
Create Date: 2022-12-14 13:18:06.062761

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ca71410ed48d'
down_revision = 'e2069e7ab78f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('userleague', sa.Column('approved_access', sa.Boolean(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('userleague', 'approved_access')
    # ### end Alembic commands ###