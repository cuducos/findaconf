# coding: utf-8

import json
import requests
import sys
from flask import abort, Blueprint, request, Response
from findaconf import app
from hashlib import sha512

reload(sys)
sys.setdefaultencoding('utf-8')

autocomplete_blueprint = Blueprint('autocomplete', __name__)


@autocomplete_blueprint.route('/keywords', methods=['GET'])
def ajax_keywords():

    # basic vars
    query = request.args.get('query')
    limit = int(request.args.get('limit'))
    keywords = list()

    # load keywords
    if query:
        filename = app.config['BASEDIR'].child('contrib', 'keywords.txt')
        with open(filename) as filehandler:
            for line in filehandler:
                if query.lower() in line.lower():
                    keywords.append(line.strip())

    # return
    keywords = keywords[:limit]
    return Response(
        response=json.dumps([{'value': k, 'label': k} for k in keywords]),
        status=200,
        mimetype='application/json')


@autocomplete_blueprint.route('/googleplaces', methods=['GET'])
def ajax_googleplaces():

    # check if the query term was sent
    query = request.args.get('query')
    if not query:
        abort(404)

    # get places from Google Places API
    api_url_vars = {
        'input': query,
        'language': 'en',
        'key': app.config['GOOGLE_PLACES_API']
    }
    api_url = 'https://maps.googleapis.com/maps/api/place/autocomplete/json'
    if app.config['GOOGLE_PLACES_API_PROXY']:
        api_url = app.config['GOOGLE_PLACES_API_PROXY']
        api_url_vars['token'] = sha512(app.config['SECRET_KEY']).hexdigest()
    api_request = requests.get(api_url, params=api_url_vars)

    # check results
    if api_request.status_code != 200:
        abort(404)
    api_data = api_request.json()

    # parse results
    places = [place['description'] for place in api_data['predictions']]
    return Response(
        response=json.dumps([{'value': p, 'label': p} for p in places]),
        status=200,
        mimetype='application/json')