# coding: utf-8

from decouple import config


def set_app(app, db=False):
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    if db:
        app.config['SQLALCHEMY_DATABASE_URI'] = config(
            'DATABASE_URL_TEST',
            default='sqlite:///' + app.config['BASEDIR'].child('findaconf',
                                                               'tests',
                                                               'tests.db')
        )
    test_app = app.test_client()
    if db:
        db.create_all()
    return test_app


def unset_app(db=False):
    if db:
        db.session.remove()
        db.drop_all()