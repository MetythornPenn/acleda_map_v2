"""create table

Revision ID: 53676ed7300a
Revises: 
Create Date: 2023-10-26 09:25:56.675923

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '53676ed7300a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('merchant',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('latitude', sa.Float(), nullable=False),
    sa.Column('longitude', sa.Float(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('merchant')
    # ### end Alembic commands ###
