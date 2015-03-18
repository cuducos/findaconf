# coding: utf-8

import sys

from authomatic import Authomatic
from authomatic.adapters import WerkzeugAdapter
from bs4 import BeautifulSoup
from datetime import datetime
from findaconf import app, db, lm
from findaconf.forms import LoginForm
from findaconf.helpers.minify import render_minified
from findaconf.helpers.providers import OAuthProvider
from findaconf.helpers.titles import get_search_title
from findaconf.models import Continent, Country, Group, User, Year
from flask import (
    abort, Blueprint, flash, g, make_response, redirect, render_template,
    request, session, url_for
)
from flask.ext.login import current_user, login_user, logout_user
from random import randrange

reload(sys)
sys.setdefaultencoding('utf-8')

site_blueprint = Blueprint(
    'site',
    __name__,
    template_folder='templates',
    static_folder='static'
)


@site_blueprint.route('/')
@render_minified
def index():
    return render_template('home.slim')


@site_blueprint.route('/find')
@render_minified
def results():

    # parse vars
    url_vars = ['query', 'month', 'year', 'region', 'location']
    req_vars = [request.args.get(v) for v in url_vars]
    query = dict(zip(url_vars, req_vars))

    # page title
    page_title = get_search_title(randrange(8), query['query'])

    return render_template('results.slim', page_title=page_title, **query)


@site_blueprint.route('/login', methods=['GET'])
@render_minified
def login_options():
    return render_template('login.slim',
                           page_title='Log in',
                           providers=OAuthProvider(),
                           form=LoginForm())


@site_blueprint.route('/login/process', methods=('POST',))
def login_process():

    form = LoginForm()
    if form.validate_on_submit():

        # redirect to provider
        provider = form.provider.data
        if provider:

            # check remember_me and store it to be processed after oauth
            session['remember_me'] = form.remember_me.data
            session['provider'] = form.provider.data
            return redirect('/login/{}'.format(provider))

    # abort if no provider of if form fails
    return abort(404)


@site_blueprint.route('/login/<provider>')
def login(provider):

    # after login url
    next_page = 'site.index'

    # check if provider is valid
    providers = OAuthProvider()
    if provider not in providers.get_slugs():
        abort(404)

    # create authomatic and response objects
    authomatic = Authomatic(providers.credentials,
                            app.config['SECRET_KEY'],
                            report_errors=True)
    oauth_response = make_response()

    # try login
    provider_name = providers.get_name(provider)
    adapter = WerkzeugAdapter(request, oauth_response)
    result = authomatic.login(adapter, provider_name)
    if result:

        # flash error message if any
        if result.error and app.debug:
            session['remember_me'] = False
            session['provider'] = None
            msg = BeautifulSoup(result.error.message).findAll(text=True)
            flash({'type': 'alert', 'text': ' '.join(msg)})

        # if success
        redir_resp = make_response(redirect(url_for(next_page)))
        if result.user:
            result.user.update()

            # check if api sent email address
            if not result.user.email:
                msg = '{} is refusing to send us your email address. '
                msg += 'Please, try another log in provider.'
                flash({'type': 'error', 'text': msg.format(provider_name)})
                next_page = 'site.login_options'

            # manage user data in db
            else:

                # convert all emails to lowercase (avoids duplicity in db)
                result.user.email = result.user.email.lower()

                # if existing user
                user = User.query.filter_by(email=result.user.email).first()
                if user:
                    if provider != user.created_with:
                        return redirect('/login/{}'.format(user.created_with))
                    user.last_seen = datetime.now()
                    db.session.add(user)
                    db.session.commit()

                # if new user
                else:
                    now = datetime.now()
                    roles = Group()
                    if result.user.email in app.config['ADMIN']:
                        role = roles.default('admin')
                    else:
                        role = roles.default()
                    new_user = User(email=result.user.email,
                                    name=result.user.name,
                                    created_with=provider,
                                    created_at=now,
                                    last_seen=now,
                                    group=role)
                    # check if email address is valid
                    if not new_user.valid_email():
                        msg = 'The address “{}” provided by {} is not a valid '
                        msg += 'email. Please, try another log in provider.'
                        flash({'type': 'error',
                               'text': msg.format(new_user.email,
                                                  provider_name)})
                        next_page = 'site.login_options'

                    # save user to db
                    else:
                        db.session.add(new_user)
                        db.session.commit()
                        new_query = User.query.filter_by(email=new_user.email)
                        user = new_query.first()

                # login user
                if user and user.valid_email():
                    login_user(user)
                    flash({'type': 'success',
                           'text': 'Welcome, {}'.format(result.user.name)})
                # remember me
                remember_me = session.get('remember_me', False)
                if remember_me:
                    session_provider = session.get('provider', False)
                    if provider == session_provider:
                        session['remember_me'] = False
                        session['provider'] = None
                        user.remember_me_token = user.get_token()
                        db.session.add(user)
                        db.session.commit()
                        redir_resp.set_cookie('remember_me', user.get_hash())

        return redir_resp

    return oauth_response


@site_blueprint.route('/logout')
def logout():
    if g.user.is_authenticated():
        g.user.remember_me_token = ''
        db.session.add(g.user)
        db.session.commit()
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
    return {'continents': Continent.query.order_by(Continent.title).all(),
            'countries': Country.query.order_by(Country.title).all(),
            'months': app.config['MONTHS'],
            'years': Year.query.order_by(Year.year).all()}
