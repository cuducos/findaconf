# coding: utf-8

import sys
from findaconf import app
from findaconf.mockup import Conf
from flask import Blueprint, render_template, request
from htmlmin.minify import html_minify

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
    return html_minify(render_template('home.slim'))


@site_blueprint.route('/find')
def results():

    # parse vars
    url_vars = ['query', 'month', 'year', 'region', 'location']
    req_vars = [request.args.get(v) for v in url_vars]
    query = dict(zip(url_vars, req_vars))

    return html_minify(render_template('results.slim'))
