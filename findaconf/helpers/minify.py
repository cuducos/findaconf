# coding: utf-8

from htmlmin.minify import html_minify
from flask import render_template


def render_minified(template_name_or_list, **context):
    rendered_template = render_template(template_name_or_list, **context)
    return html_minify(rendered_template)
