# coding: utf-8

from unipath import Path
from decouple import config

BASEDIR = Path(__file__).parent
SITE_STATIC = BASEDIR.child('findaconf', 'blueprints', 'site', 'static')
SQLALCHEMY_DATABASE_URI = config('DATABASE_URL',
                                 default='sqlite:///' + BASEDIR.child('app.db'))

DEBUG = config('DEBUG', default=False, cast=bool)
ASSETS_DEBUG = config('ASSETS_DEBUG', default=False, cast=bool)
SECRET_KEY = config('SECRET_KEY', default=False)

GOOGLE_PLACES_API = config('GOOGLE_PLACES_API', default=None)
GOOGLE_PLACES_API_PROXY = config('GOOGLE_PLACES_API_PROXY', default=None)

TITLE = 'Find a Conference'
LANGS = [
    {'code': 'zh', 'title': '中文'},
    {'code': 'el', 'title': 'Ελληνικά'},
    {'code': 'en', 'title': 'English'},
    {'code': 'es', 'title': 'Español'},
    {'code': 'it', 'title': 'Italiano'},
    {'code': 'pt', 'title': 'Português'},
    {'code': 'ro', 'title': 'Română'}
]

MONTHS = {
    1: 'January',
    2: 'February',
    3: 'March',
    4: 'April',
    5: 'May',
    6: 'June',
    7: 'July',
    8: 'August',
    9: 'September',
    10: 'October',
    11: 'November',
    12: 'December'
}
