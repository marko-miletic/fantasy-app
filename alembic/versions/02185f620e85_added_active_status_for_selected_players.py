"""

Revision ID: 02185f620e85
Revises: 582bff3b8b38
Create Date: 2022-12-05 13:58:44.268134

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '02185f620e85'
down_revision = '582bff3b8b38'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('selectedplayers', sa.Column('active', sa.Boolean(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('selectedplayers', 'active')
    # ### end Alembic commands ###
