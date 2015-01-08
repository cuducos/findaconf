# coding: utf-8

import requests
import sys
from flask import abort, Blueprint, jsonify, request
from findaconf import app
from findaconf.models import Conference, Keyword
from hashlib import sha512

reload(sys)
sys.setdefaultencoding('utf-8')

autocomplete_blueprint = Blueprint('autocomplete', __name__)


@autocomplete_blueprint.route('/keywords', methods=['GET'])
def ajax_keywords():

    # basic vars
    query = '%{}%'.format(request.args.get('query'))
    limit = int(request.args.get('limit'))

    # query keywords
    keywords = Keyword.query.filter(Keyword.title.ilike(query))\
                            .order_by(Keyword.title)[0:limit]

    # query conference title
    conferences = Conference.query.filter(Conference.title.ilike(query))\
                                  .order_by(Conference.title)[0:limit]

    # return
    results = [k.title for k in keywords] + [c.title for c in conferences]
    sorted_results = sorted(results)
    return jsonify(results=[{'label': r} for r in sorted_results[0:limit]])


@autocomplete_blueprint.route('/places', methods=['GET'])
def ajax_google_places():

    # check if the query term was sent
    query = request.args.get('query')
    if not query:
        abort(404)

    # get places from Google Places API
    api_url_vars = {
        'input': query,
        'language': 'en',
        'key': app.config['GOOGLE_PUBLIC_API']
    }
    api_url = 'https://maps.googleapis.com/maps/api/place/autocomplete/json'
    if app.config['GOOGLE_PLACES_PROXY']:
        api_url = app.config['GOOGLE_PLACES_PROXY']
        api_url_vars['token'] = sha512(app.config['SECRET_KEY']).hexdigest()
    api_request = requests.get(api_url, params=api_url_vars)

    # check results
    if api_request.status_code != 200:
        abort(404)
    api_data = api_request.json()

    # parse results
    places = [place['description'] for place in api_data['predictions']]
    return jsonify(results=[{'label': p} for p in places])
