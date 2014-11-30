from flask import Flask
from flask.ext.assets import Environment
from flask.ext.compress import Compress
from flask.ext.script import Manager, Server
from slimish_jinja import SlimishExtension


# add slimish_jinja extension
class SlimishApp(Flask):
    Flask.jinja_options['extensions'].append(SlimishExtension)

# init the app
app = SlimishApp('findaconf')
app.config.from_object('config')
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

# init manager
manager = Manager(app)

# enable gzip compression
Compress(app)

# assets
assets = Environment(app)
assets.load_path = [
    app.config['BASEDIR'].child('findaconf', 'coffeescript'),
    app.config['BASEDIR'].child('findaconf', 'scss'),
    app.config['BASEDIR'].child('bower_components')
]
assets.from_yaml(app.config['BASEDIR'].child('findaconf', 'assets.yaml'))

# manage errors
if not app.config['DEBUG']:
    import logging
    from logging.handlers import RotatingFileHandler
    filepath = app.config['BASEDIR'].child('errors.log')
    handler = RotatingFileHandler(filepath, 'a', 1 * 1024 * 1024, 10)
    formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    handler.setFormatter(formatter)
    handler.setLevel(logging.INFO)
    app.logger.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.logger.info('App {} started successfully.'.format(app.config['MINI_TITLE']))

# load & register blueprints
from blueprints.autocomplete import autocomplete_blueprint
from blueprints.file_routes import file_routes_blueprint
from blueprints.site import site_blueprint
app.register_blueprint(autocomplete_blueprint, url_prefix='/autocomplete')
app.register_blueprint(file_routes_blueprint)
app.register_blueprint(site_blueprint)
