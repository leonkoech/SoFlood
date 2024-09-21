from flask import Blueprint, request, jsonify
import requests
import os

geocode_bp = Blueprint('geocode', __name__)
GEOCODING_API_KEY = os.environ.get('GOOGLE_GEOCODING_API_KEY')

@geocode_bp.route('/geocode', methods=['GET'])
def get_geocode_data():

    response = {
        "error": None, 
        "data": None
    }
    status_code = 200

    try:
        address = request.args.get('address')
        geocode_data = requests.get(f'https://maps.googleapis.com/maps/api/geocode/json?key={GEOCODING_API_KEY}&address={address}')
        results = geocode_data.json()["results"]
        latlng = None
        if results:
            latlng = results[0]["geometry"]["location"]
            response["data"] = latlng

    except Exception as e:
        response["error"] = e
        status_code = 500


    return jsonify(response), status_code

@geocode_bp.route('/elevation', methods=['GET'])
def get_elevation_data():

    response = {
        "error": None, 
        "data": None
    }
    status_code = 200

    try:
        lat = request.args.get('lat')
        lng = request.args.get('lng')
        elevation = requests.get(f'https://maps.googleapis.com/maps/api/elevation/json?locations={lat}%2C{lng}&key={GEOCODING_API_KEY}')

        results = elevation.json()["results"]

        if results:
            # The elevation of the location in meters.
            elevation = results[0]["elevation"]
            response['data'] = { "elevation_in_meters": elevation }
    
    except Exception as e:
        response["error"] = e
        status_code = 500


    return jsonify(response), status_code

