# coding: utf-8

from flask import Flask
from flask.ext.assets import Environment
from flask.ext.compress import Compress
from flask.ext.login import LoginManager
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.script import Manager
from flask.ext.sqlalchemy import SQLAlchemy
from slimish_jinja import SlimishExtension

# init the app
app = Flask('findaconf', static_folder='assets')
app.config.from_object('config')

# set jinja and json outputs
app.jinja_options['extensions'].append(SlimishExtension)
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

# init db
db = SQLAlchemy(app)
from findaconf import models

# init manager
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

# init the login manager
lm = LoginManager()
lm.init_app(app)
lm.login_view = '/login'
lm.login_message = {'type': 'info', 'text': lm.login_message}

# enable gzip compression
Compress(app)

# assets
site_path = app.config['BASEDIR'].child('findaconf', 'blueprints', 'site')
bower_path = app.config['BASEDIR'].child('findaconf', 'bower')
assets = Environment(app)
assets.config['PYSCSS_LOAD_PATHS'] = [bower_path.child('foundation', 'scss')]
assets.load_path = [site_path, bower_path]
assets.from_yaml(app.config['BASEDIR'].child('findaconf', 'assets.yaml'))

# manage errors
if not app.config['DEBUG']:
    import logging
    from logging.handlers import RotatingFileHandler
    filepath = app.config['BASEDIR'].child('errors.log')
    handler = RotatingFileHandler(filepath, 'a', 1 * 1024 * 1024, 10)
    row = '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    formatter = logging.Formatter(row)
    handler.setFormatter(formatter)
    handler.setLevel(logging.INFO)
    app.logger.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.logger.info('{} started successfully.'.format(app.config['TITLE']))

# load & register blueprints
from blueprints.autocomplete.views import autocomplete_blueprint
from blueprints.files.views import files_blueprint
from blueprints.site.views import site_blueprint
app.register_blueprint(autocomplete_blueprint, url_prefix='/autocomplete')
app.register_blueprint(files_blueprint)
app.register_blueprint(site_blueprint)
