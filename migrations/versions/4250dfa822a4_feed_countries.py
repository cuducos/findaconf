"""Feed: Countries

Revision ID: 4250dfa822a4
Revises: 1c5f54d4aa34
Create Date: 2014-12-10 22:24:01.089932

"""

# revision identifiers, used by Alembic.
revision = '4250dfa822a4'
down_revision = '1c5f54d4aa34'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column

from csv import reader
from findaconf import app
from findaconf.models import Continent, Country


def upgrade():

    # load countries iso3166.csv and build a dictionary
    csv_path = app.config['BASEDIR'].child('migrations', 'csv', 'en')
    csv_file = csv_path.child('iso3166.csv')
    countries = dict()
    with open(csv_file) as file_handler:
        csv = list(reader(file_handler))
        for c in csv:
            countries[c[0]] = c[1]

    # load countries-continents from country_continent.csv
    csv_file = csv_path.child('country_continent.csv')
    with open(csv_file) as file_handler:
        csv = list(reader(file_handler))
        country_continent = [{'country': c[0], 'continent': c[1]} for c in csv]

    # loop and feed countries table
    data = list()
    for item in country_continent:

        # get continent id
        continent_guess = item['continent'].lower()
        continent = Continent.query.filter_by(alpha2=continent_guess).first()

        # include country
        if continent is not None:
            country_name = countries.get(item['country'], False)
            if country_name:
                data.append({'alpha2': item['country'].lower(),
                             'title': country_name,
                             'continent_id': continent.id})

    # Create an ad-hoc table to use for the insert statement.
    country_table = table('country',
        column('alpha2', sa.String),
        column('title', sa.String),
        column('continent_id', sa.Integer),
    )

    # Insert data.
    op.bulk_insert(country_table, data)


def downgrade():
    op.execute(Country.__table__.delete())
