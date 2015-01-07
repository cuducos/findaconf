# coding: utf-8

from decouple import config
from findaconf.tests.fake_data import fake_conference, seed


def set_app(app, db=False):

    # set test vars
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['ASSETS_DEBUG'] = False

    # set test db
    if db:
        app.config['SQLALCHEMY_DATABASE_URI'] = config(
            'DATABASE_URL_TEST',
            default='sqlite:///' + app.config['BASEDIR'].child('findaconf',
                                                               'tests',
                                                               'tests.db')
        )

    # create test app
    test_app = app.test_client()

    # create and feed db tables
    if db:

        # start from a clean db
        db.session.remove()
        db.drop_all()

        # create tables and feed them
        db.create_all()
        seed(app, db)
        [db.session.add(fake_conference(db)) for i in range(1, 43)]
        db.session.commit()

    # return test app
    return test_app


def unset_app(db=False):
    if db:
        db.session.remove()
        db.drop_all()
