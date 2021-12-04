"""add content to  users table

Revision ID: 06cc015d2b15
Revises: 9ee1d5a53052
Create Date: 2021-12-04 12:50:07.313491

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '06cc015d2b15'
down_revision = '9ee1d5a53052'
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
    pass
