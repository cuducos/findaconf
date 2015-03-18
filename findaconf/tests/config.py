# coding: utf-8

from decouple import config
from findaconf.tests.fake_data import seed


def set_app(app, db=False):

    # set test vars
    app.config['ASSETS_DEBUG'] = False
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['ADMIN'] = ['admin@findaconf.info']

    # set test db
    if db:
        path = app.config['BASEDIR'].child('findaconf', 'tests', 'tests.db')
        default = 'sqlite:///{}'.format(path)
        app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URL_TEST',
                                                       default=default)

    # create test app
    test_app = app.test_client()

    # create and feed db tables once the test app is created
    if db:
        db.session.remove()
        db.drop_all()
        db.create_all()
        seed(app, db)

    # return test app
    return test_app


def unset_app(db=False):
    if db:
        db.session.remove()
        db.drop_all()
