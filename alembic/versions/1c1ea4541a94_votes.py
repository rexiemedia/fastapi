"""votes

Revision ID: 1c1ea4541a94
Revises: 8bb4737925ec
Create Date: 2021-12-15 11:34:19.041592

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1c1ea4541a94'
down_revision = '8bb4737925ec'
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
