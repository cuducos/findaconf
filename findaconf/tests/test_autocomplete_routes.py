# coding: utf-8

import unittest
from findaconf import app, db


class TestAutoCompleteRoutes(unittest.TestCase):

    def setUp(self):

        # init
        app.testing = True
        app.config['SQLALCHEMY_DATABASE_URI'] = app.config['DB_TESTS']
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.drop_all()

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
