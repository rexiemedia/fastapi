"""add foreignkey to post table

Revision ID: 22cd653f79a6
Revises: 96d9780a9206
Create Date: 2021-12-02 16:43:30.644348

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '22cd653f79a6'
down_revision = '96d9780a9206'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_user_id_fkey', source_table='posts', referent_table='users', local_cols=['owner_id'], remote_cols=['id'], ondelete=['CASCADE'])
    pass


def downgrade():
    op.drop_constraint('posts_user_id_fkey', table_name='posts')
    op.drop_column('posts', 'owner_id')
    pass
