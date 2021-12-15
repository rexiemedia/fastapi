"""constrains-post

Revision ID: 8bb4737925ec
Revises: 12ef8ae2e456
Create Date: 2021-12-15 11:30:32.378050

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8bb4737925ec'
down_revision = '12ef8ae2e456'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table="posts", referent_table="users", local_cols=[
                          'id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint('post_users_fk', table_name="posts")
    op.drop_column('posts', 'user_id')
    pass
