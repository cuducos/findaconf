# coding: utf-8

from cairosvg import svg2png
from colour import Color
from flask import (abort, Blueprint, send_from_directory, render_template,
                   Response)
from findaconf import app
from random import choice, randrange


files = Blueprint('file_routes', __name__, static_folder='')


@files.route('/poster.png', methods=['GET'])
def poster():

    # randon backgorund color
    rand_rgb = tuple([(randrange(97, 160) / 255.0) for i in range(3)])
    bg = Color(rgb=rand_rgb)

    # get foreground
    fg = Color(bg.hex)
    variation = randrange(15, 60)
    fg.hue = choice([variation, variation * -1])

    # random alpha
    alpha = randrange(4, 7) / 10.0

    # create image
    svg = render_template('poster.svg', bg=bg.hex, fg=fg.hex, alpha=alpha)
    return Response(svg2png(bytestring=svg), mimetype='image/png')


@files.route('/favicon.ico')
def favicon():
    imgs_path = app.config['SITE_STATIC'].child('favicons')
    return send_from_directory(imgs_path, 'favicon.ico')


@files.route('/robots.txt')
def robots():
    return send_from_directory(app.config['SITE_STATIC'], 'robots.txt')


@files.route('/assets/foundation-icons.<extension>')
@files.route('/assets/webassets-external/foundation-icons.<extension>')
def foundation_icon(extension):
    bower_path = app.config['BASEDIR'].child('findaconf', 'bower')
    directory = 'foundation-icon-fonts'
    file_name = 'foundation-icons.{}'.format(extension)
    if bower_path.child(directory, file_name).exists():
        return send_from_directory(bower_path.child(directory), file_name)
    else:
        abort(404)
