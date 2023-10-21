"""create Merchant table

Revision ID: f18b4a995c59
Revises: b35cc22d1726
Create Date: 2023-10-21 15:15:56.586139

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'f18b4a995c59'
down_revision = 'b35cc22d1726'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('merchant',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('slug', sa.String(), nullable=False),
    sa.Column('content', sa.Text(), nullable=True),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('slug')
    )
    op.drop_table('blog')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('blog',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('title', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('slug', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('content', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('author_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('is_active', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['user.id'], name='blog_author_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='blog_pkey')
    )
    op.drop_table('merchant')
    # ### end Alembic commands ###
