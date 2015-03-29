"""Add user roles

Revision ID: 16ef0d8ffae1
Revises: 8acb1453abb
Create Date: 2015-03-17 15:45:05.406297

"""

# revision identifiers, used by Alembic.
revision = '16ef0d8ffae1'
down_revision = '8acb1453abb'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column

from findaconf.models import Group


def upgrade():
    roles = ['user', 'moderator', 'admin']
    data = [{'title': r} for r in roles]

    # Create an ad-hoc table to use for the insert statement.
    group_table = table('group',
        column('title', sa.String),
    )

    # Insert data.
    op.bulk_insert(group_table, data)


def downgrade():
    op.execute(Group.__table__.delete())
