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

from collections import defaultdict
from csv import reader
from findaconf import app
from string import letters

# Create ad-hoc tables to use for the insert statement.
country = table('country',
                column('id', sa.Integer),
                column('alpha2', sa.String),
                column('title', sa.String),
                column('continent_id', sa.Integer))
continent = table('continent',
                  column('id', sa.Integer),
                  column('alpha2', sa.String),
                  column('title', sa.String))


def upgrade():

    # get the path of the folder containing all the CSV files
    csv_path = app.config['BASEDIR'].child('migrations', 'csv', 'en')

    # load countries iso3166.csv and build a dictionary
    data = list()
    csv_file = csv_path.child('iso3166.csv')
    with open(csv_file) as file_handler:
        csv = [row for row in reader(file_handler) if row]
        for row in csv:
            if len(row[0]) == 2 and all(c in letters for c in row[0]):
                data.append({'alpha2': row[0].lower(), 'title': row[1]})
    # insert data
    op.bulk_insert(country, data)

    # load countries-continents from country_continent.csv
    continent_countries = defaultdict(list)
    csv_file = csv_path.child('country_continent.csv')

    with open(csv_file) as file_handler:

        # Get all the lines from the CSV file, while skipping:
        # - blank lines
        # - lines with all blank fields (e.g. "","")
        csv = [row for row in reader(file_handler) if any(row)]

        for country_code, continent_code in csv:
            continent_countries[continent_code].append(country_code.lower())

    # 4 countries non-classified in the CSV
    continent_countries['SA'].extend(['cw', 'bq', 'sx'])
    continent_countries['AF'].append('ss')

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
    bind = op.get_bind()
    for row in bind.execute(country.select()):
        op.execute(country.delete().where(country.c.id == row.id))
