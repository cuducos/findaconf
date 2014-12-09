# coding: utf-8

import unittest
from random import randrange
from findaconf import app


class TestFileRoutes(unittest.TestCase):

    def setUp(self):

        # init
        app.testing = True
        self.app = app.test_client()

    def tearDown(self):
        pass

    # test routes from blueprint/file_routes.py

    def test_poster(self):
        resp = self.app.get('/poster.png', data={'rand': randrange(1000, 9999)})
        assert resp.status_code == 200
        assert resp.mimetype == 'image/png'

    def test_favicon(self):
        resp = self.app.get('/favicon.ico')
        assert resp.status_code == 200
        assert resp.mimetype == 'image/x-icon'

    def test_robots(self):
        resp = self.app.get('/robots.txt')
        assert resp.status_code == 200
        assert resp.mimetype == 'text/plain'

    def test_foundation_icons(self):
        base_urls = ['/static/css/', '/static/webassets-external/']
        extensions = ['eot', 'svg', 'ttf', 'woff', 'py']
        for base_url in base_urls:
            for ext in extensions:
                path = '{}foundation-icons.{}'.format(base_url, ext)
                resp = self.app.get(path)
                print 'url:', path
                print 'status:', resp.status_code
                if ext != 'py':
                    assert resp.status_code == 200
                    if ext == 'svg':
                        assert resp.mimetype == 'image/svg+xml'
                    else:
                        assert resp.mimetype == 'application/octet-stream'
                else:
                    assert resp.status_code == 404