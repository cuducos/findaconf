# coding: utf-8

from findaconf import db
from hashlib import md5

conferences_keywords = db.Table(
    'conferences_keywords',
    db.metadata,
    db.Column('conference_id', db.Integer, db.ForeignKey('conference.id')),
    db.Column('keyword_id', db.Integer, db.ForeignKey('keyword.id'))
)


class Group(db.Model):

    __tablename__ = 'group'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(16))
    users = db.relationship('User', backref='group')

    def __repr__(self):
        return '<Group #{}: {}>'.format(self.id, self.title)


class User(db.Model):

    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(256), index=True, unique=True)
    name = db.Column(db.String(256))
    language = db.Column(db.String(2))
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))

    def __repr__(self):
        return '<User #{}: {}>'.format(self.id, self.name)

    def avatar(self, size):
        base_url = 'http://www.gravatar.com/avatar/'
        user_hash = md5(self.email.encode('utf_8')).hexdigest()
        return '{}{}?s={}'.format(base_url, user_hash, size)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)


class Conference(db.Model):

    __tablename__ = 'conference'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140), index=True)
    place = db.Column(db.String(256), index=True)
    starts = db.Column(db.Date, index=True)
    ends = db.Column(db.Date, index=True)
    deadline = db.Column(db.Date, index=True)
    poster = db.Column(db.String(256))
    url = db.Column(db.String(256))
    email = db.Column(db.String(256))
    description = db.Column(db.Text())
    continent_id = db.Column(db.Integer, db.ForeignKey('continent.id'))
    country_id = db.Column(db.Integer, db.ForeignKey('country.id'))
    country = db.relationship('Country', backref='conferences')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref='conferences')
    keywords = db.relationship('Keyword',
                            secondary=conferences_keywords,
                            backref=' conferences')

    def __repr__(self):
        return '<Conference #{}: {}>'.format(self.id, self.title)


class Keyword(db.Model):

    __tablename__ = 'keyword'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140), index=True, unique=True)
    count = db.Column(db.Integer, index=True)

    def __repr__(self):
        return '<Keyword #{}: {}>'.format(self.id, self.title)


class Year(db.Model):

    __tablename__ = 'year'
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.SmallInteger, index=True, unique=True)


class Country(db.Model):

    __tablename__ = 'country'
    id = db.Column(db.Integer, primary_key=True)
    alpha2 = db.Column(db.String(2), index=True, unique=True)
    title = db.Column(db.String(140))
    continent_id = db.Column(db.Integer, db.ForeignKey('continent.id'))
    continent = db.relationship('Continent', backref='countries')

    def __repr__(self):
        return '<Country #{}: {}>'.format(self.id, self.title)


class CountryTranslation(db.Model):

    __tablename__ = 'country_translation'
    id = db.Column(db.Integer, primary_key=True)
    language = db.Column(db.String(2), index=True)
    country_id = db.Column(db.Integer, db.ForeignKey('country.id'))
    country = db.relationship('Country', backref='translation')
    title = db.Column(db.String(140))

    def __repr__(self):
        return '<CountryTranslation #{}: {}>'.format(self.id, self.title)


class Continent(db.Model):

    __tablename__ = 'continent'
    id = db.Column(db.Integer, primary_key=True)
    alpha2 = db.Column(db.String(2), index=True, unique=True)
    title = db.Column(db.String(140))

    def __repr__(self):
        return '<Continent #{}: {}>'.format(self.id, self.title)


class ContinentTranslation(db.Model):

    __tablename__ = 'continent_translation'
    id = db.Column(db.Integer, primary_key=True)
    language = db.Column(db.String(2), index=True)
    continent_id = db.Column(db.Integer, db.ForeignKey('continent.id'))
    continent = db.relationship('Continent', backref='translation')
    title = db.Column(db.String(140))

    def __repr__(self):
        return '<ContinentTranslation #{}: {}>'.format(self.id, self.title)


class MagicNumber(db.Model):

    __tablename__ = 'magic_number'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140), index=True, unique=True)
    count = db.Column(db.Integer)

    def __repr__(self):
        return '<MagicNumber #{}: {} ({})>'.format(self.id,
                                                   self.title,
                                                   self.count)
