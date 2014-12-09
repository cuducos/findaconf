from datetime import datetime, timedelta
from findaconf import app
from random import choice, randrange


class Conf:

    def __init__(self):
        unis = open(app.config['BASEDIR'].child('contrib', 'universities.txt'))
        nations = open(app.config['BASEDIR'].child('contrib', 'countries.txt'))
        self.id = randrange(10000, 100000)
        self.title = self._title_generator()
        self.img = self._poster_generator()
        self.place = choice([k.strip() for k in unis if k])
        self.country = choice([c.strip() for c in nations if c])
        self.ini = self._date_generator()
        self.end = self._date_generator()
        self.deadline = self._date_generator()
        self.keywords = self._keywords_generator()
        self.url = choice(['#', None])
        self.email = choice(['#, None'])

    @staticmethod
    def _title_generator():
        num = choice(['V', 'XVII', 'XIX', 'XXXVI', 'XXI', 'VIII', 'III', 'IV'])
        thing = choice(['Meeting', 'Conference', 'Seminar', 'Workshop'])
        handler = open(app.config['BASEDIR'].child('contrib', 'keywords.txt'))
        area = choice([c.strip() for c in handler if c])
        return '{} {} on {}'.format(num, thing, area)

    @staticmethod
    def _poster_generator():
        handler = open(app.config['BASEDIR'].child('contrib', 'posters.txt'))
        posters = [p.strip() for p in handler if p]
        default = ['/poster.png'] * int(len(posters) / 3)
        return choice(default + posters)

    @staticmethod
    def _date_generator():
        y = randrange(2014, 2020)
        d = randrange(1, 365)
        dt = datetime(y, 1, 1) + timedelta(days=d)
        return dt.strftime('%d/%m/%Y')

    @staticmethod
    def _keywords_generator():
        handler = open(app.config['BASEDIR'].child('contrib', 'keywords.txt'))
        keywords = [c.strip() for c in handler if c]
        limit = randrange(3, 13)
        output = list()
        while len(output) < limit:
            keyword = choice(keywords)
            output.append(keyword)
            keywords.remove(keyword)
        return output
