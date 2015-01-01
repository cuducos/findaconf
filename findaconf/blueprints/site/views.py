# coding: utf-8

import sys

from authomatic import Authomatic
from authomatic.adapters import WerkzeugAdapter
from findaconf import app, db, lm
from findaconf.blueprints.site.helpers.minify import render_minified
from findaconf.models import Continent, Country, User, Year
from flask import Blueprint, flash, g, redirect, request, make_response, url_for
from flask.ext.login import current_user, login_user, logout_user

reload(sys)
sys.setdefaultencoding('utf-8')

site_blueprint = Blueprint(
    'site',
    __name__,
    template_folder='templates',
    static_folder='static'
)


@site_blueprint.route('/')
def index():
    return render_minified('home.slim')


@site_blueprint.route('/find')
def results():

    # parse vars
    url_vars = ['query', 'month', 'year', 'region', 'location']
    req_vars = [request.args.get(v) for v in url_vars]
    query = dict(zip(url_vars, req_vars))

    return render_minified('results.slim', **query)


@site_blueprint.route('/login', methods=['GET'])
def login_options():
    providers = app.config['OAUTH_CREDENDIALS'].keys()
    return render_minified('login.slim', providers=providers)


@site_blueprint.route('/login/<provider_name>', methods=['GET', 'POST'])
def login(provider_name):

    # create authomatic and response objects
    authomatic = Authomatic(app.config['OAUTH_CREDENDIALS'],
                            app.config['SECRET_KEY'],
                            report_errors=True)
    response = make_response()

    # try login
    result = authomatic.login(WerkzeugAdapter(request, response), provider_name)
    if result:

        # if success
        if result.user:
            result.user.update()

            # manage user data in db
            user = User.query.filter_by(email=result.user.email).first()
            if not user:
                new_user = User(email=result.user.email, name=result.user.name)
                db.session.add(new_user)
                db.session.commit()
                user = User.query.filter_by(email=result.user.email).first()

            # save user info
            login_user(user)
            flash({'type': 'success',
                   'text': 'Welcome, {}'.format(result.user.name)})
            return redirect(url_for('site.index'))

    return response


@site_blueprint.route('/logout')
def logout():
    logout_user()
    flash({'type': 'success', 'text': 'You\'ve been logged out.'})
    return redirect(url_for('site.index'))


@site_blueprint.before_request
def before_request():
    g.user = current_user


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@site_blueprint.context_processor
def inject_main_vars():
    return {
        'continents': Continent.query.order_by(Continent.title).all(),
        'countries': Country.query.order_by(Country.title).all(),
        'months': app.config['MONTHS'],
        'years': Year.query.order_by(Year.year).all()
    }
