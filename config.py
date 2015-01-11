# coding: utf-8

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
GOOGLE_PUBLIC_API = config('GOOGLE_PUBLIC_API',
                                     default=None)
GOOGLE_PLACES_PROXY = config('GOOGLE_PLACES_PROXY', default=None)

# oauth/oauth2 providers

# TODO oauth/oauth2 still not implemented for the following providers:
# * LinkedIn
# * Windows
# * Tumblr
# (what is needed: create dev account, create app, input API tokens and test)

OAUTH_CREDENTIALS = {

    'Amazon': {
        'class_': oauth2.Amazon,
        'consumer_key': config('AMAZON_CLIENT_ID', default=None),
        'consumer_secret': config('AMAZON_CLIENT_SECRET', default=None),
        'scope': oauth2.Amazon.user_info_scope
    },

    'Facebook': {
        'class_': oauth2.Facebook,
        'consumer_key': config('FACEBOOK_CLIENT_ID', default=None),
        'consumer_secret': config('FACEBOOK_CLIENT_SECRET', default=None),
        'scope': oauth2.Facebook.user_info_scope
    },

    'GitHub': {
        'class_': oauth2.GitHub,
        'consumer_key': config('GITHUB_CLIENT_ID', default=None),
        'consumer_secret': config('GITHUB_CLIENT_SECRET', default=None),
        'access_headers': {'User-Agent': 'Find-a-Conference'},
        'scope': oauth2.GitHub.user_info_scope,
    },

    'Google Plus': {
        'class_': oauth2.Google,
        'consumer_key': config('GOOGLE_CLIENT_ID', default=None),
        'consumer_secret': config('GOOGLE_CLIENT_SECRET', default=None),
        'scope': oauth2.Google.user_info_scope
    },

    'LinkedIn': {
        'class_': oauth2.LinkedIn,
        'consumer_key': config('LINKEDIN_CLIENT_ID', default=None),
        'consumer_secret': config('LINKEDIN_CLIENT_SECRET', default=None),
        'scope': oauth2.LinkedIn.user_info_scope
    },

    'Tumblr': {
        'class_': oauth1.Tumblr,
        'consumer_key': config('TUMBLR_CLIENT_ID', default=None),
        'consumer_secret': config('TUMBLR_CLIENT_SECRET', default=None),
    },

    'Windows': {
        'class_': oauth2.WindowsLive,
        'consumer_key': config('WINDOWS_CLIENT_ID', default=None),
        'consumer_secret': config('WINDOWS_CLIENT_SECRET', default=None),
        'scope': oauth2.WindowsLive.user_info_scope
    },

    'Yahoo': {
        'class_': oauth1.Yahoo,
        'consumer_key': config('YAHOO_CLIENT_ID', default=None),
        'consumer_secret': config('YAHOO_CLIENT_SECRET', default=None),
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