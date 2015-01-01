# coding: utf-8

from findaconf import app, db
from findaconf.tests.config import set_app, unset_app
from unittest import TestCase


class TestSiteRoutes(TestCase):

    def setUp(self):
        self.app = set_app(app, db)

    def tearDown(self):
        unset_app(db)

    # test routes from blueprint/site.py
    def test_index(self):
        resp = self.app.get('/')
        assert resp.status_code == 200
        assert resp.mimetype == 'text/html'

    def test_find(self):
        resp = self.app.get('/find', data={'query': 'sociology',
                                           'month': 'February',
                                           'year': 2015,
                                           'region': 'Europe',
                                           'location': 'University of Essex'})
        assert resp.status_code == 200
        assert resp.mimetype == 'text/html'

    def test_login(self):

        # test if login page exists
        resp = self.app.get('/login')
        assert resp.status_code == 200
        assert resp.mimetype == 'text/html'

        # test if are links to oauth/oauth2 providers
        providers = app.config['OAUTH_CREDENTIALS'].keys()
        for provider in providers:
            assert 'href="/login/{}'.format(provider) in resp.data

        # test if is there a link to login in the home page
        resp = self.app.get('/')
        assert 'href="/login"' in resp.data

    def test_login_providers(self):

        # test if links to the ouauth/oauth2 providers
        providers = app.config['OAUTH_CREDENTIALS'].keys()
        for provider in providers:
            resp = self.app.get('/login/{}'.format(provider))
            assert resp.status_code == 200

        # test if unauthorized provider returns 404
        resp = self.app.get('/login/anything_else')
        assert resp.status_code == 404
