# coding: utf-8

from findaconf import app, db
from findaconf.helpers.providers import OAuthProvider
from findaconf.models import User
from findaconf.tests.config import TestApp
from findaconf.tests.mocks import MockAuthomatic
from mock import patch
from random import choice as random_choice
from unittest import TestCase


class TestSiteRoutes(TestCase):

    def setUp(self):
        self.test = TestApp(app, db)
        self.app = self.test.get_app()

    def tearDown(self):
        self.test.unset_app()

    def read_cookie(self, key):
        try:
            cookie = self.app.cookie_jar._cookies['localhost.local']['/'][key]
            return cookie.value
        except (KeyError, AttributeError):
            return False

    # test routes from blueprint/site.py
    def test_index(self):
        resp = self.app.get('/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.mimetype, 'text/html')

    def test_find(self):
        resp = self.app.get('/find', data={'query': 'sociology',
                                           'month': 'February',
                                           'year': 2015,
                                           'region': 'Europe',
                                           'location': 'University of Essex'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.mimetype, 'text/html')

    def test_login_pages(self):

        # test if login page exists
        resp = self.app.get('/login')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.mimetype, 'text/html')

        # test if are there links to oauth/oauth2 providers
        providers = OAuthProvider()
        for provider in providers.get_slugs():
            self.assertIn(' data-oauth="{}"'.format(provider), resp.data)

        # test if is there a link to login in the home page
        resp = self.app.get('/')
        self.assertIn('href="/login', resp.data)

    def test_login_providers(self):

        # test if links to the ouauth/oauth2 providers (20X or 30X)
        providers = OAuthProvider()
        for provider in providers.get_slugs():
            resp = self.app.get('/login/{}'.format(provider))
            self.assertEqual(resp.status_code, 302)

        # test if unauthorized provider returns 404
        resp = self.app.get('/login/anything_else')
        self.assertEqual(resp.status_code, 404)

    @patch('findaconf.blueprints.site.views.Authomatic', autospec=True)
    def test_new_user_login(self, mocked):

        # get a valid login link/provider
        providers = OAuthProvider()
        valid_providers = providers.get_slugs()
        self.assertTrue(valid_providers)

        # create a mock object for Authomatic.login()
        mocked.return_value = MockAuthomatic()

        # assert that we have no users in the database
        self.assertEqual(db.session.query(User).count(), 0,
                         'User count before login differs than 0')
        self.app.get('/login/{}'.format(valid_providers[0]))

        # assert a user was created
        self.assertEqual(db.session.query(User).count(), 1,
                         'User count after login differs than 1')

        # assert user data
        u = User.query.first()
        self.assertEqual(u.email, 'johndoe@john.doe', "Emails don't match")
        self.assertEqual(u.name, 'John Doe', "Name doesn't match")
        self.assertEqual(u.created_at, u.last_seen, "Time doesn't match")
        self.assertEqual(u.group.title, 'user')
        self.assertTrue(u.last_seen, "Last seen is blank")
        self.assertEqual(u.created_with, valid_providers[0],
                         "Provider doesn't match")


    @patch('findaconf.blueprints.site.views.Authomatic', autospec=True)
    def test_new_admin_user_login(self, mocked):

        # get a valid login link/provider
        providers = OAuthProvider()
        valid_providers = providers.get_slugs()
        self.assertTrue(valid_providers)

        # random pick an admin email from the config
        admin_email = random_choice(app.config['ADMIN'])

        # create a mock object for Authomatic.login()
        mocked.return_value = MockAuthomatic(email=admin_email)

        # create a new admin user
        self.app.get('/login/{}'.format(valid_providers[0]))

        # assert the new user is an admin
        u = User.query.first()
        self.assertEqual(u.group.title, 'admin')

    @patch('findaconf.blueprints.site.views.Authomatic', autospec=True)
    def test_unsuccessful_user_login_with_invalid_email(self, mocked):

        # get a valid login link/provider
        providers = OAuthProvider()
        valid_providers = providers.get_slugs()
        self.assertTrue(valid_providers)

        # create a mock object for Authomatic.login() & try to login
        mocked.return_value = MockAuthomatic(email='fulano-de.tal')
        resp = self.app.get('/login/{}'.format(valid_providers[0]),
                            follow_redirects=True)

        # assert error message was shown
        self.assertIn('is not a valid email', resp.data,
                      'No error shown after trying login w/ invalid email')

        # assert that we have no users in the database
        self.assertEqual(db.session.query(User).count(), 0,
                         'User count after login differs than 0')

    @patch('findaconf.blueprints.site.views.Authomatic', autospec=True)
    def test_unsuccessful_user_login_with_no_email(self, mocked):

        # get a valid login link/provider
        providers = OAuthProvider()
        valid_providers = providers.get_slugs()
        self.assertTrue(valid_providers)

        # create a mock object for Authomatic.login() & try to login
        mocked.return_value = MockAuthomatic(email=None)
        resp = self.app.get('/login/{}'.format(valid_providers[0]),
                            follow_redirects=True)

        # assert error message was shown
        self.assertIn('refusing to send us your email address', resp.data,
                      'No error shown after trying login without email')

        # assert that we have no users in the database
        self.assertEqual(db.session.query(User).count(), 0,
                         'User count after login differs than 0')

    @patch('findaconf.blueprints.site.views.Authomatic', autospec=True)
    def test_returning_user_login(self, mocked):

        # get a valid login link/provider
        providers = OAuthProvider()
        valid_providers = providers.get_slugs()
        self.assertTrue(valid_providers)

        # create a mock object for Authomatic.login()
        mocked.return_value = MockAuthomatic()

        # login & assert welcome message was shown
        resp1 = self.app.get('/login/{}'.format(valid_providers[0]),
                             follow_redirects=True)
        self.assertIn('Welcome, John Doe', resp1.data,
                      'No welcome message found after login')

        # logout & assert logout message was shown
        resp2 = self.app.get('/logout', follow_redirects=True)
        self.assertIn('You\'ve been logged out', resp2.data,
                      'No logout message found after logout')

        # login again & assert only one user was created
        self.app.get('/login/{}'.format(valid_providers[0]))
        u = User.query.first()
        self.assertEqual(u.email, 'johndoe@john.doe', "Emails don't match")
        self.assertEqual(u.name, 'John Doe', "Name doesn't match")
        self.assertNotEqual(u.created_at, u.last_seen,
                            "Last seen wasn't updated")
        self.assertEqual(db.session.query(User).count(), 1,
                         'User count after login differs than 1')

    @patch('findaconf.blueprints.site.views.Authomatic', autospec=True)
    def test_login_with_remember_me(self, mocked):

        # get a valid login link/provider
        providers = OAuthProvider()
        valid_providers = providers.get_slugs()
        self.assertTrue(valid_providers)

        # create a mock object for Authomatic.login()
        mocked.return_value = MockAuthomatic()

        # create new user
        self.app.delete_cookie('localhost', 'user_id')
        self.app.delete_cookie('localhost', 'remember_me')
        self.app.post('/login/process',
                      follow_redirects=True,
                      data={'remember_me': '1',
                            'provider': valid_providers[0]})

        # assert cookies were created accordingly
        user = User.query.first()
        self.assertEqual(user.id, int(self.read_cookie('user_id')))
        self.assertTrue(user.check_hash(self.read_cookie('remember_me')))

        # clean cookis for next sessions
        self.app.delete_cookie('localhost', 'user_id')
        self.app.delete_cookie('localhost', 'remember_me')

    @patch('findaconf.blueprints.site.views.Authomatic', autospec=True)
    def test_returning_user_with_remember_me(self, mocked):

        # get a valid login link/provider
        providers = OAuthProvider()
        valid_providers = providers.get_slugs()
        self.assertTrue(valid_providers)

        # create a mock object for Authomatic.login()
        mocked.return_value = MockAuthomatic()

        # create user and token
        user = User(email='user@remember.me')
        user.remember_me_token = user.get_token()
        db.session.add(user)
        db.session.commit()

        # create cookies
        self.app.set_cookie('localhost', 'user_id', '1')
        self.app.set_cookie('localhost', 'remember_me', user.get_hash())

        # assert user is logged in
        resp = self.app.get('/')
        self.assertIn('href="/logout"', resp.data)
        self.assertNotIn('href="/login', resp.data)

        # clean cookis for next sessions
        self.app.delete_cookie('localhost', 'user_id')
        self.app.delete_cookie('localhost', 'remember_me')

    @patch('findaconf.blueprints.site.views.Authomatic', autospec=True)
    def test_failed_login_with_api_error(self, mocked):

        # get a valid login link/provider
        providers = OAuthProvider()
        valid_providers = providers.get_slugs()
        self.assertTrue(valid_providers)

        # error in HTML and parsed
        html = """
        <html>
            <head>
                <title>Error Page</title>
            </head>
            <body>
                <div class="error">
                    <h1>Ooops...</h1>
                    <p>Error message</p>
                </div>
            </body>
        </html>
        """
        parsed = 'Error Page Ooops... Error message'

        # create a mock object for Authomatic.login()
        mocked.return_value = MockAuthomatic(error=html)

        # login & assert welcome message was shown
        resp1 = self.app.get('/login/{}'.format(valid_providers[0]),
                             follow_redirects=True)
        self.assertIn(parsed, resp1.data, 'API message does not match')
