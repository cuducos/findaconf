# coding: utf-8

import unittest
from findaconf import app


class TestAssetsRoutes(unittest.TestCase):

    def setUp(self):

        # init
        app.testing = True
        self.app = app.test_client()

    def tearDown(self):
        pass

    # test assets from assets.yaml

    def test_libs_js(self):
        resp = self.app.get('/static/js/libs.min.js')
        assert resp.status_code == 200
        assert resp.mimetype == 'application/javascript'

    def test_init_js(self):
        resp = self.app.get('/static/js/init.min.js')
        assert resp.status_code == 200
        assert resp.mimetype == 'application/javascript'

    def test_libs_css(self):
        resp = self.app.get('/static/css/libs.min.css')
        assert resp.status_code == 200
        assert resp.mimetype == 'text/css'

    def test_style_css(self):
        resp = self.app.get('/static/css/style.min.css')
        assert resp.status_code == 200
        assert resp.mimetype == 'text/css'

