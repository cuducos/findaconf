# coding: utf-8

from cairosvg import svg2png
from colour import Color
from flask import abort, Blueprint, send_from_directory, render_template, Response
from findaconf import app
from random import choice, randrange
from unipath import Path


files_blueprint = Blueprint('file_routes', __name__, static_folder='')


@files_blueprint.route('/poster.png', methods=['GET'])
def poster():

    # randon backgorund color
    rcolor = lambda: randrange(97, 160) / 255.0
    bg = Color(rgb=(rcolor(), rcolor(), rcolor()))

    # get foreground
    fg = Color(bg.hex)
    variation = randrange(15, 60)
    fg.hue = choice([variation, variation * -1])

    # random alpha
    alpha = randrange(4, 7) / 10.0

    # create image
    svg = render_template('poster.svg', background=bg.hex, foreground=fg.hex, transparency=alpha)
    return Response(svg2png(bytestring=svg), mimetype='image/png')


@files_blueprint.route('/favicon.ico')
def favicon():
    return send_from_directory(app.config['SITE_STATIC'].child('imgs'), 'favicon.ico')


@files_blueprint.route('/robots.txt')
def robots():
    return send_from_directory(app.config['SITE_STATIC'], 'robots.txt')


@files_blueprint.route('/static/css/foundation-icons.<extension>')
@files_blueprint.route('/static/webassets-external/foundation-icons.<extension>')
def foundation_icon(extension):
    path = app.config['BASEDIR'].child('findaconf', 'bower', 'foundation-icon-fonts')
    filename = 'foundation-icons.{}'.format(extension)
    if path.child(filename).exists():
        return send_from_directory(path, filename)
    else:
        abort(404)