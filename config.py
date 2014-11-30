# coding: utf-8

from unipath import Path
from decouple import config

BASEDIR = Path(__file__).parent
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
