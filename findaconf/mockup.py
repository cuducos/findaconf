from datetime import datetime, timedelta
from findaconf import app
from random import choice, randrange


class Conf:

    def __init__(self, id=None, title=None, img=None, place=None, country=None, ini=None, end=None, deadline=None,
                 keywords=None, url=None, email=None):
        self.id = randrange(10000, 100000)
        self.title = self._title_generator()
        self.img = self._poster_generator()
        self.place = choice([k.strip() for k in open(app.config['BASEDIR'].child('contrib', 'universities.txt')) if k])
        self.country = choice([c.strip() for c in open(app.config['BASEDIR'].child('contrib', 'countries.txt')) if c])
        self.ini = self._date_generator()
        self.end = self._date_generator()
        self.deadline = self._date_generator()
        self.keywords = self._keywords_generator()
        self.url = choice(['#', None])
        self.email = choice(['#, None'])

    @staticmethod
    def _title_generator():
        num = choice(['V', 'XVII', 'II', 'XIX', 'XXXVI', 'XXI', 'VIII', 'I', 'III', 'IV', 'XVIII'])
        thing = choice(['Meeting', 'Conference', 'Seminar', 'Workshop'])
        area = choice([c.strip() for c in open(app.config['BASEDIR'].child('contrib', 'keywords.txt')) if c])
        return '{} {} on {}'.format(num, thing, area)

    @staticmethod
    def _poster_generator():
        posters = [
            'http://www2.warwick.ac.uk/newsandevents/events/challenging_orthodoxies/critical_governance_conference_poster.jpg',
            'http://www.memics.cz/2009/img/memics09poster.jpg',
            'http://www.memics.cz/2008/img/memics08-poster.jpg',
            'http://www.wordsinspace.net/lib-arch-data/wordpress_libarchdata/wp-content/uploads/2011/03/Media-Histories_Conference-Poster1.jpg',
            'http://www.memphis.edu/philosophy/images/spindel_2013_poster_thumb.jpg',
            'http://www.physics.purdue.edu/conference/wip/files/images/poster%20-%20v.1.preview.jpg',
            ]
        default = ['/poster.png'] * int(len(posters) / 3)
        return choice(default + posters)

    @staticmethod
    def _date_generator():
        y = randrange(2014, 2020)
        d = randrange(1, 365)
        dt = datetime(y, 1, 1) + timedelta(days=d)
        return datetime.strftime(dt, '%d/%m/%Y')

    @staticmethod
    def _keywords_generator():
        keywords = [c.strip() for c in open(app.config['BASEDIR'].child('contrib', 'keywords.txt')) if c]
        limit = randrange(3, 13)
        output = list()
        while len(output) < limit:
            keyword = choice(keywords)
            output.append(keyword)
            keywords.remove(keyword)
        return output
