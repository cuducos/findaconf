# coding: utf-8

from unittest import TestCase
from findaconf import app
from findaconf.tests.config import set_app, unset_app


class TestAssetsRoutes(TestCase):

    def setUp(self):
        self.app = set_app(app)

    def tearDown(self):
        unset_app()

    # test assets from assets.yaml

    def test_libs_js(self):
        resp = self.app.get('/assets/libs.min.js')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.mimetype, 'application/javascript')

    def test_init_js(self):
        resp = self.app.get('/assets/init.min.js')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.mimetype, 'application/javascript')

    def test_libs_css(self):
        resp = self.app.get('/assets/libs.min.css')
        print app.config['ASSETS_DEBUG']
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.mimetype, 'text/css')

    def test_style_css(self):
        resp = self.app.get('/assets/style.min.css')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.mimetype, 'text/css')
