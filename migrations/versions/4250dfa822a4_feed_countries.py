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
# Create ad-hoc tables to use for the insert statement.
country = table('country',
                column('alpha2', sa.String),
                column('title', sa.String),
                column('continent_id', sa.Integer))
continent = table('continent',
                  column('id', sa.Integer),
                  column('alpha2', sa.String),
                  column('title', sa.String))


def upgrade():

    # load countries iso3166.csv and build a dictionary
    data = list()
    csv_path = app.config['BASEDIR'].child('migrations', 'csv', 'en')
    csv_file = csv_path.child('iso3166.csv')
    with open(csv_file) as file_handler:
        csv = list(reader(file_handler))
        for row in csv:
                data.append({'alpha2': row[0].lower(), 'title': row[1]})

    # insert data
    op.bulk_insert(country, data)

    # load countries-continents from country_continent.csv
    continent_countries = dict()
    csv_file = csv_path.child('country_continent.csv')
    with open(csv_file) as file_handler:
        csv = list(reader(file_handler))
        for row in csv:
            continent_countries[row[1]] = continent_countries.get(row[1], [])
            continent_countries[row[1]].append(row[0].lower())

    # 4 countries non-classified in the CSV
    continent_countries['SA'].extend(['cw', 'bq', 'sx'])
    continent_countries['AF'].append('cw')

    # update country table with continent data
    bind = op.get_bind()
    for key in continent_countries.iterkeys():

        # get continent id
        query = bind.execute(continent.select().
                             where(continent.c.alpha2 == key.lower()))
        result = query.first()
        if result:
            continent_id = result.id

            # update country row
            op.execute(country.update().
                       where(country.c.alpha2.in_(continent_countries[key])).
                       values({'continent_id': continent_id}))


def downgrade():
    op.execute(country.delete())
