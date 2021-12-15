"""posts1

Revision ID: 3d421a6812c9
Revises: 
Create Date: 2021-12-15 11:22:35.630370

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3d421a6812c9'
down_revision = None
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
    
    pass


def downgrade():   
    op.drop_table('posts')
    pass