from flask import Flask
from flask.ext.assets import Environment
from flask.ext.compress import Compress
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.script import Manager
from flask.ext.sqlalchemy import SQLAlchemy
from slimish_jinja import SlimishExtension


# add slimish_jinja extension
class SlimishApp(Flask):
    Flask.jinja_options['extensions'].append(SlimishExtension)

# init the app
app = SlimishApp('findaconf', static_folder='assets')
app.config.from_object('config')
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

# enable gzip compression
Compress(app)

# assets
findaconf_path = app.config['BASEDIR'].child('findaconf')
assets = Environment(app)
assets.load_path = [
    findaconf_path.child('blueprints', 'site', 'coffeescript'),
    findaconf_path.child('blueprints', 'site', 'scss'),
    findaconf_path.child('bower')
]
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
    app.logger.info('App {} started successfully.'.format(app.config['TITLE']))

# load & register blueprints
from blueprints.autocomplete.views import autocomplete_blueprint
from blueprints.files.views import files_blueprint
from blueprints.site.views import site_blueprint
app.register_blueprint(autocomplete_blueprint, url_prefix='/autocomplete')
app.register_blueprint(files_blueprint)
app.register_blueprint(site_blueprint)
