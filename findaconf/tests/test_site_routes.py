# coding: utf-8

from mock import patch
from findaconf import app, db
from findaconf.helpers.providers import OAuthProvider
from findaconf.models import User
from findaconf.tests.config import set_app, unset_app
from findaconf.tests.mocks import MockAuthomatic
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

    def test_login_pages(self):

        # test if login page exists
        resp = self.app.get('/login')
        assert resp.status_code == 200
        assert resp.mimetype == 'text/html'

        # test if are there links to oauth/oauth2 providers
        providers = OAuthProvider()
        for provider in providers.get_slugs():
            assert 'href="/login/{}'.format(provider) in resp.data

        # test if is there a link to login in the home page
        resp = self.app.get('/')
        assert 'href="/login"' in resp.data

    def test_login_providers(self):

        # test if links to the ouauth/oauth2 providers (20X or 30X)
        providers = OAuthProvider()
        for provider in providers.get_slugs():
            resp = self.app.get('/login/{}'.format(provider))
            assert resp.status_code == 302

        # test if unauthorized provider returns 404
        resp = self.app.get('/login/anything_else')
        assert resp.status_code == 404

    @patch('findaconf.blueprints.site.views.Authomatic', autospec=True)
    def test_new_user_login(self, mocked):

        # get a valid login link/provider
        providers = OAuthProvider()
        valid_providers = providers.get_slugs()
        if valid_providers:

            # create a mock object for Authomatic.login()
            mocked.return_value = MockAuthomatic(name='Fulano de Tal',
                                                 email='fulano@de.tal')

            # assert that we have no users in the database
            self.assertEqual(db.session.query(User).count(), 0,
                             'Count of users before login differs than 0')
            self.app.get('/login/{}'.format(valid_providers[0]))

            # assert a user was created
            self.assertEqual(db.session.query(User).count(), 1,
                             'Count of users after login differs than 1')

            # assert user data
            u = User.query.first()
            self.assertEqual(u.email, 'fulano@de.tal', "Email doesn't match")
            self.assertEqual(u.name, 'Fulano de Tal', "Name doesn't match")
