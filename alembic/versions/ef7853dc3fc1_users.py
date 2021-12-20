"""users

Revision ID: ef7853dc3fc1
Revises: c370b3f195b4
Create Date: 2021-12-15 13:40:23.523218

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ef7853dc3fc1'
down_revision = 'c370b3f195b4'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('firstname', sa.String(), nullable=False),
    sa.Column('lastname', sa.String(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
        server_default=sa.text('now()'), nullable=False),

    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
        )
    pass


def downgrade():
    op.drop_table('users')
    pass