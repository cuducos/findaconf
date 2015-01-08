# coding: utf-8

import faker
from unittest import TestCase
from findaconf import app
from findaconf.models import User
from findaconf.tests.config import set_app, unset_app


class TestModelMethods(TestCase):

    def setUp(self):
        self.app = set_app(app)

    def tearDown(self):
        unset_app()

    # test methods from User
    def test_valid_email(self):
        fake = faker.Factory.create()
        valid_emails = ['USER@foo.COM',
                        'THE_US-ER@foo.bar.org',
                        'first.last@foo.jp']
        invalid_emails = ['user@example,com',
                          'user_at_foo.org',
                          'user.name@example.',
                          'foo@bar_baz.com',
                          'foo@bar+baz.com']
        should_be_valid_emails = [fake.email() for i in range(0, 42)]
        johndoe = User()
        for email in valid_emails:
            johndoe.email = email
            assert johndoe.valid_email()
        for email in invalid_emails:
            johndoe.email = email
            assert not johndoe.valid_email()
        for email in should_be_valid_emails:
            johndoe.email = email
            assert johndoe.valid_email()
