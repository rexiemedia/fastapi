"""add content to  posts table

Revision ID: edafbf663c0a
Revises: 990468e30bf3
Create Date: 2021-12-02 16:08:23.947387

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'edafbf663c0a'
down_revision = '990468e30bf3'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    pass
