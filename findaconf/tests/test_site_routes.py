# coding: utf-8

import unittest
from findaconf import app


class TestSiteRoutes(unittest.TestCase):

    def setUp(self):

        # init
        app.testing = True
        self.app = app.test_client()

    def tearDown(self):
        pass

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
