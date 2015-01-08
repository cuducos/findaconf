# coding: utf-8

from csv import reader
from datetime import datetime
from findaconf.models import Conference, Continent, Country, Keyword
from random import choice
import faker


def fake_conference(db):

    fake = faker.Factory.create()

    # fake posters
    posters = [
        'http://www.memics.cz/2009/img/memics09poster.jpg',
        'http://www.memics.cz/2008/img/memics08-poster.jpg',
        'http://memphis.edu/philosophy/images/spindel_2013_poster_thumb.jpg'
    ] + ([''] * 4)

    # core fake data
    conf = {
        'title':  fake.catch_phrase(),
        'place': fake.address(),
        'starts': datetime.strptime(fake.date(), '%Y-%m-%d'),
        'ends': datetime.strptime(fake.date(), '%Y-%m-%d'),
        'deadline': datetime.strptime(fake.date(), '%Y-%m-%d'),
        'url': choice([fake.url(), '']),
        'email': choice([fake.email(), '']),
        'description': fake.paragraphs(),
        'country': choice([c for c in Country.query.all()]),
        'keywords': list(),
        'poster': choice(posters),
    }

    # fake keywords
    keywords = fake.words()
    for word in keywords:
        row = Keyword.query.filter(Keyword.title == word).first()
        if row is None:
            row = Keyword(title=word, count=1)
        else:
            row.count += 1
        db.session.add(row)
        db.session.commit()
        keyword_row = Keyword.query.filter(Keyword.title == word).first()
        conf['keywords'].append(keyword_row)

    # get continent
    row = Country.query.get(conf['country'].id)
    conf['continent_id'] = row.continent_id

    # return a random conference
    return Conference(**conf)


def seed(app, db):

    # only feed if tables are empty
    if not Country.query.first():

        # continents
        csv_path = app.config['BASEDIR'].child('migrations', 'csv', 'en')
        csv_file = csv_path.child('continents.csv')
        with open(csv_file) as file_handler:
            csv = list(reader(file_handler))
            csv.pop(0)
            for c in csv:
                db.session.add(Continent(alpha2=c[0].lower(), title=c[1]))

        # insert data
        db.session.commit()

        # load countries iso3166.csv and build a dictionary
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
            country_continent = list()
            for c in csv:
                country_continent.append({'country': c[0], 'continent': c[1]})

        # loop and feed countries table
        for item in country_continent:

            # get continent id
            guess = item['continent'].lower()
            continent = Continent.query.filter_by(alpha2=guess).first()

            # include country
            if continent is not None:
                country_name = countries.get(item['country'], False)
                if country_name:
                    db.session.add(Country(alpha2=item['country'].lower(),
                                           title=country_name,
                                           continent_id=continent.id))

        # insert data
        db.session.commit()
