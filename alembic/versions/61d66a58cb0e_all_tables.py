"""all-tables

Revision ID: 61d66a58cb0e
Revises: 1c1ea4541a94
Create Date: 2021-12-15 11:55:03.450148

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '61d66a58cb0e'
down_revision = '1c1ea4541a94'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', 
    sa.Column('id', sa.Integer(), nullable=False, primary_key=True), 
    sa.Column('title', sa.String(), nullable=False), 
    sa.Column('content', sa.String(), nullable=False),
    sa.Column('published', sa.Boolean(), server_default=sa.schema.DefaultClause('True'), nullable=False), 
    sa.Column('rating', sa.Integer(),server_default=sa.schema.DefaultClause('0'), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False)
    )

    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('firstname', sa.String(), nullable=False),
    sa.Column('lastname', sa.String(), nullable=False),
    sa.Column('isAdmin', sa.Boolean(), server_default=sa.schema.DefaultClause('True'), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
        server_default=sa.text('now()'), nullable=False),

    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
        )
    
    op.add_column('posts', sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table="posts", referent_table="users", local_cols=[
                          'user_id'], remote_cols=['id'], ondelete="CASCADE")
    
    
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

    op.drop_constraint('post_users_fk', table_name="posts")
    op.drop_column('posts', 'user_id')
    
    op.drop_table('posts')
    op.drop_table('users')
    pass