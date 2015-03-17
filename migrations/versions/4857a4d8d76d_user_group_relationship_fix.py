"""User/Group relationship fix

Revision ID: 4857a4d8d76d
Revises: 16ef0d8ffae1
Create Date: 2015-03-17 16:24:02.728627

"""

# revision identifiers, used by Alembic.
revision = '4857a4d8d76d'
down_revision = '16ef0d8ffae1'

from alembic import op
import sqlalchemy as sa

from findaconf import app, db
from findaconf.models import Group, User


def upgrade():
    role = Group()
    for user in User.query.all():
        if user.email in app.config['ADMIN']:
            user.group = role.default('admin')
        else:
            user.group = role.default()
        db.session.add(user)
    db.session.commit()


def downgrade():
    for user in User.query.all():
        del(user.group)
        db.session.add(user)
    db.session.commit()
