# coding: utf-8

from findaconf import app
from findaconf.tests.config import TestApp
from random import randrange
from unittest import TestCase


class TestFileRoutes(TestCase):

    def setUp(self):
        self.test = TestApp(app)
        self.app = self.test.get_app()

    def tearDown(self):
        self.test.unset_app()

    # test routes from blueprint/file_routes.py

    def test_poster(self):
        resp = self.app.get('/poster.png', data={'rand': randrange(100, 999)})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.mimetype, 'image/png')

    def test_favicon(self):
        types = ['image/vnd.microsoft.icon', 'image/x-icon']
        resp = self.app.get('/favicon.ico')
        self.assertEqual(resp.status_code, 200)
        self.assertIn(resp.mimetype, types)

    def test_robots(self):
        resp = self.app.get('/robots.txt')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.mimetype, 'text/plain')

    def test_foundation_icons(self):
        base_url = '/assets/'
        extensions = ['eot', 'svg', 'ttf', 'woff', 'py']
        types = ['application/vnd.ms-fontobject',
                 'application/octet-stream',
                 'application/x-font-woff',
                 'image/svg+xml']
        for ext in extensions:
            path = '{}foundation-icons.{}'.format(base_url, ext)
            resp = self.app.get(path)
            if ext != 'py':
                self.assertEqual(resp.status_code, 200)
                self.assertIn(resp.mimetype, types)
            else:
                self.assertEqual(resp.status_code, 404)
