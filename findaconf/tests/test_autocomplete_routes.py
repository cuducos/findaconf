# coding: utf-8

import unittest
from findaconf import app


class TestAutoCompleteRoutes(unittest.TestCase):

    def setUp(self):

        # init
        app.testing = True
        self.app = app.test_client()

    def tearDown(self):
        pass

    # test routes from blueprint/autocomplete.py

    def test_keywords(self):
        url = '/autocomplete/keywords?query=sociology&limit=10'
        resp = self.app.get(url)
        print 'resp.status_code=', resp.status_code
        assert resp.status_code == 200
        assert resp.mimetype == 'application/json'

    def test_google_places(self):
        url = '/autocomplete/places?query=University%20of%20Essex'
        resp = self.app.get(url)
        print 'resp.status_code=', resp.status_code
        assert resp.status_code == 200
        assert resp.mimetype == 'application/json'
