from flask import Blueprint, request, jsonify

geocode_bp = Blueprint('geocode', __name__)

@geocode_bp.route('/geocode', methods=['GET'])
def get_geocode_data():
    address = request.args.get('address')
    print(f'address={address}')

    return jsonify({ "ok": True, "address": address }), 200

