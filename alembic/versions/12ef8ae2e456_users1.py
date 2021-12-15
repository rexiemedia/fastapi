"""users1

Revision ID: 12ef8ae2e456
Revises: 3d421a6812c9
Create Date: 2021-12-15 11:29:15.499260

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '12ef8ae2e456'
down_revision = '3d421a6812c9'
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
