# coding: utf-8

import authomatic
from authomatic.providers import oauth1, oauth2
from unipath import Path
from decouple import config

# file paths
BASEDIR = Path(__file__).parent
SITE_STATIC = BASEDIR.child('findaconf', 'blueprints', 'site', 'static')

# db settings
uri = 'sqlite:///' + BASEDIR.child('app.db')
SQLALCHEMY_DATABASE_URI = config('DATABASE_URL', default=uri)

# debug settings
DEBUG = config('DEBUG', default=False, cast=bool)
ASSETS_DEBUG = config('ASSETS_DEBUG', default=False, cast=bool)

# security keys
SECRET_KEY = config('SECRET_KEY', default=False)

# public api keys
GOOGLE_DEVELOPER_PUBLIC_API = config('GOOGLE_DEVELOPER_PUBLIC_API', default=None)
GOOGLE_PLACES_PROXY = config('GOOGLE_PLACES_PROXY', default=None)

# oauth/oauth2 providers
OAUTH_CREDENTIALS = {

    'Google': {
        'class_': oauth2.Google,
        'consumer_key': config('GOOGLE_DEVELOPER_CLIENT_ID', default=None),
        'consumer_secret': config('GOOGLE_DEVELOPER_CLIENT_SECRET', default=None),
        'id': authomatic.provider_id(),
        'scope': oauth2.Google.user_info_scope,
    },

    'Twitter': {
        'class_': oauth1.Twitter,
        'consumer_key': config('TWITTER_DEVELOPER_CLIENT_ID', default=None),
        'consumer_secret': config('TWITTER_DEVELOPER_CLIENT_SECRET', default=None),
        'id': authomatic.provider_id(),
    },

    'Facebook': {
        'class_': oauth2.Facebook,
        'consumer_key': config('FACEBOOK_DEVELOPER_CLIENT_ID', default=None),
        'consumer_secret': config('FACEBOOK_DEVELOPER_CLIENT_SECRET', default=None),
        'id': authomatic.provider_id(),
        'scope': oauth2.Facebook.user_info_scope,
    },

    'Yahoo': {
        'class_': oauth1.Yahoo,
        'consumer_key': '##########--',
        'consumer_secret': '##########',
        'id': authomatic.provider_id(),
    },
}

# content settings
TITLE = 'Find a Conference'
HEADLINE = 'Find academic conferences and call for papers all over the world'

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
