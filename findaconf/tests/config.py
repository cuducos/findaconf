# coding: utf-8

import faker
from authomatic.providers.oauth2 import Google
from csv import reader
from datetime import datetime
from decouple import config
from findaconf.models import Conference, Continent, Country, Group, Keyword
from random import choice


class TestApp(object):
    """Create app and db for testing purposes"""

    def __init__(self, app, db=False):
        """Set the app and the db, init the app, and seed the db"""

        # some useful vars
        self.basedir = app.config['BASEDIR']
        self.testdir = app.config['BASEDIR'].child('findaconf', 'tests')

        # default oauth (as in findaconf/forms.py)
        oauth = {'Google Plus': {'class_': Google,
                                 'consumer_key': True,
                                 'consumer_secret': True}}

        # config test app
        app.config['ASSETS_DEBUG'] = False
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['ADMIN'] = ['admin@findaconf.info',
                                'second.admin@findaconf.info',
                                'third.admin@findaconf.info']
        app.config['OAUTH_CREDENTIALS'] = oauth

        # config and create db
        self.db = db
        if self.db:
            default = 'sqlite:///{}'.format(self.testdir.child('tests.db'))
            uri = config('DATABASE_URL_TEST', default=default)
            app.config['SQLALCHEMY_DATABASE_URI'] = uri
            self.clear_db()
            self.db.create_all()

        # create test app and seed db
        self.app = app.test_client()
        self.seed_db()

    def get_app(self):
        """Returns the app object"""
        return self.app

    def unset_app(self):
        """Commands to be run after tests"""
        self.clear_db()

    def clear_db(self):
        """Method to clean current session and drop all tables form db"""
        if self.db:
            self.db.session.remove()
            self.db.drop_all()

    def seed_db(self):
        """Seed required (countries, user roles) & fake data (conferences)"""

        #  only if db is set
        if self.db:

            # seed countries if table is empty
            if not Continent.query.count():
                for continent in self.continents():
                    self.db.session.add(continent)
                self.db.session.commit()

            # seed countries if table is empty (but continents exist)
            if Continent.query.count() and not Country.query.count():
                [self.db.session.add(country) for country in self.countries()]
                self.db.session.commit()

            # seed user groups if table is empty
            if not Group.query.count():
                [self.db.session.add(role) for role in self.user_roles()]

            # seed user groups if table is empty
            if not Conference.query.count():
                [self.db.session.add(conf) for conf in self.conferences()]

            # insert data
            self.db.session.commit()

    @staticmethod
    def user_roles(roles=['user', 'moderator', 'admin']):
        "Returns a list with the desired user roles (Group model)"""
        for role in roles:
            yield Group(title=role)

    def continents(self):
        """Returns a list with Continent rows"""
        csv_path = self.basedir.child('migrations', 'csv', 'en')
        csv_file = csv_path.child('continents.csv')
        with open(csv_file) as file_handler:
            csv = [row for row in reader(file_handler) if any(row)]
            csv.pop(0)
            for c in csv:
                yield Continent(alpha2=c[0].lower(), title=c[1])

    def countries(self):
        """Returns a list with Country rows"""

        # load countries from iso3166.csv and build a dictionary
        csv_path = self.basedir.child('migrations', 'csv', 'en')
        csv_file = csv_path.child('iso3166.csv')
        countries = dict()
        with open(csv_file) as file_handler:
            csv = [row for row in reader(file_handler) if any(row)]
            for c in csv:
                countries[c[0]] = c[1]

        # load countries-continents relationship from country_continent.csv
        csv_file = csv_path.child('country_continent.csv')
        with open(csv_file) as file_handler:
            csv = [row for row in reader(file_handler) if any(row)]
            country_continent = list()
            for c in csv:
                row = {'country': c[0], 'continent': c[1]}
                country_continent.append(row)

        # loop and seed countries table
        for item in country_continent:

            # get continent id
            guess = item['continent'].lower()
            continent = Continent.query.filter_by(alpha2=guess).first()

            # include country
            if continent is not None:
                country_name = countries.get(item['country'], False)
                if country_name:
                    yield Country(alpha2=item['country'].lower(),
                                  title=country_name,
                                  continent_id=continent.id)

    def get_conference(self):
        """Create a random conference (with fake data)"""

        # load faker factory
        fake = faker.Factory.create()

        # fake posters
        posters = ['http://placehold.it/768x1024/ffcc00/000000', '',
                   'http://placehold.it/768x1024/ccff00/000000', '',
                   'http://placehold.it/768x1024/ff00cc/000000', '']

        # fake core data
        conf = {'title':  fake.catch_phrase(),
                'place': fake.address(),
                'starts': datetime.strptime(fake.date(), '%Y-%m-%d'),
                'ends': datetime.strptime(fake.date(), '%Y-%m-%d'),
                'deadline': datetime.strptime(fake.date(), '%Y-%m-%d'),
                'url': choice([fake.url(), '']),
                'email': choice([fake.email(), '']),
                'description': fake.paragraphs(),
                'country': choice([c for c in Country.query.all()]),
                'keywords': list(),
                'poster': choice(posters)}

        # fake keywords
        keywords = fake.words()
        for word in keywords:
            row = Keyword.query.filter_by(title=word).first()
            if row is None:
                row = Keyword(title=word, count=1)
            else:
                row.count += 1
            self.db.session.add(row)
            self.db.session.commit()
            keyword_row = Keyword.query.filter_by(title=word).first()
            conf['keywords'].append(keyword_row)

        # get continent
        conf['continent_id'] = conf['country'].continent.id

        # return a random conference
        return Conference(**conf)

    def conferences(self, num=42):
        """Returns a list of Conference rows"""
        if num:
            for i in range(num):
                yield self.get_conference()
