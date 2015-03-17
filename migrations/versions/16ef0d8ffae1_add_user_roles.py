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

from findaconf import db
from findaconf.models import Group


def upgrade():
    roles = ['user', 'moderator', 'admin']
    [db.session.add(Group(title=role)) for role in roles]
    db.session.commit()


def downgrade():
    [db.session.delete(role) for role in Group.query.all()]
    db.session.commit()
