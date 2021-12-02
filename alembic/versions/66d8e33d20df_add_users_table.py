"""add users table

Revision ID: 66d8e33d20df
Revises: edafbf663c0a
Create Date: 2021-12-02 16:18:53.777729

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '66d8e33d20df'
down_revision = 'edafbf663c0a'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('firstname', sa.String(), nullable=False),
    sa.Column('lastname', sa.String(), nullable=False),
    sa.Column('isAdmin', sa.String(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
        server_default=sa.text('now()'), nullable=False),

    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
        )
    pass


def downgrade():
    op.drop_table('users')
    pass
