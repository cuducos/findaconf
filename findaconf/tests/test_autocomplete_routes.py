# coding: utf-8

from findaconf import app, db
from unittest import TestCase
from findaconf.tests.config import set_app, unset_app


class TestAutoCompleteRoutes(TestCase):

    def setUp(self):
        self.app = set_app(app, db)

    def tearDown(self):
        unset_app(db)

    # test routes from blueprint/autocomplete.py

    def test_keywords(self):
        url = '/autocomplete/keywords?query=sociology&limit=10'
        resp = self.app.get(url)
        assert resp.status_code == 200
        assert resp.mimetype == 'application/json'

    def test_google_places(self):
        url = '/autocomplete/places?query=University%20of%20Essex'
        resp = self.app.get(url)
        assert resp.status_code == 200
        assert resp.mimetype == 'application/json'

    def test_google_places_blank(self):
        resp = self.app.get('/autocomplete/places?query=')
        assert resp.status_code == 404
        print resp.data

    def test_google_places_wrong_proxy(self):
        original_proxy = app.config['GOOGLE_PLACES_PROXY']
        app.config['GOOGLE_PLACES_PROXY'] = 'http://python.org/ruby'
        url = '/autocomplete/places?query=University'
        resp = self.app.get(url)
        assert resp.status_code == 404
        app.config['GOOGLE_PLACES_PROXY'] = original_proxy
