"""add content to  votes  table

Revision ID: b2c56157a78a
Revises: 1ffe246231a4
Create Date: 2021-12-04 13:03:46.251713

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b2c56157a78a'
down_revision = '1ffe246231a4'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('votes',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'post_id')
    )
    pass


def downgrade():
    op.drop_table('votes')
    pass
