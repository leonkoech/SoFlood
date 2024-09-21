from flask import Blueprint, request, jsonify
import requests
import os

geocode_bp = Blueprint('geocode', __name__)
GEOCODING_API_KEY = os.environ.get('GOOGLE_GEOCODING_API_KEY')

@geocode_bp.route('/geocode', methods=['GET'])
def get_geocode_data():
    address = request.args.get('address')
    response = requests.get(f'https://maps.googleapis.com/maps/api/geocode/json?key={GEOCODING_API_KEY}&address={address}')
    results = response.json()["results"]

    latlng = None
    if results:
        latlng = results[0]["geometry"]["location"]

    return jsonify({ "ok": True, "address": address, "latlng": latlng }), 200

