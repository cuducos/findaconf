"""Feed: Continents

Revision ID: 1c5f54d4aa34
Revises: 312c1d408043
Create Date: 2014-12-10 22:22:23.565032

"""

# revision identifiers, used by Alembic.
revision = '1c5f54d4aa34'
down_revision = '312c1d408043'

from alembic import op
import sqlalchemy as sa

from csv import reader
from findaconf import app
from findaconf.models import Continent


def upgrade():
    csv_path = app.config['BASEDIR'].child('migrations', 'csv', 'en')
    csv_file = csv_path.child('continents.csv')
    with open(csv_file) as file_handler:
        csv = list(reader(file_handler))
        csv.pop(0)
        data = [{'alpha2': c[0].lower(), 'title': c[1]} for c in csv]
        op.bulk_insert(Continent.__table__, data)


def downgrade():
    op.execute(Continent.__table__.delete())
