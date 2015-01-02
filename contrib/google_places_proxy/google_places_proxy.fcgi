# coding: utf-8

from decouple import config
from flask import Flask, request, jsonify
from flup.server.fcgi import WSGIServer
from hashlib import sha512
from requests import get

app = Flask(__name__)


@app.route('/')
def google_places_proxy():

    # var to store errors
    errors = list()

    # check the secret key
    secret_server = sha512(config('SECRET_KEY', default=None))
    if secret_server.hexdigest() != request.args.get('token'):
        errors.append('Invalid `token`.')

    # check if the request has the input var
    query = request.args.get('input')
    if not query:
        errors.append('No `input` variable found.')

    # check if the request has API key var
    api_key = request.args.get('key')
    if not api_key:
        errors.append('No API `key` variable found.')

    # break if error
    if errors:
        return jsonify({'proxy_error': errors})

    # get places from Google Places API
    lang = request.args.get('lang') if request.args.get('lang') else 'en'
    api_vars = {
        'input': query,
        'language': lang,
        'key': api_key
    }
    api_url = 'https://maps.googleapis.com/maps/api/place/autocomplete/json'
    api_request = get(api_url, params=api_vars)

    # if HTTP error
    if api_request.status_code != 200:
        msg = '{} HTTP status code.'.format(api_request.status_code)
        return jsonify({'error': msg})

    # if HTTP success
    api_data = api_request.json()
    return jsonify(api_data)

WSGIServer(app).run()
