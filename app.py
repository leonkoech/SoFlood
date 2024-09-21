from flask import Flask, jsonify, render_template, request
import api  # Importing the file `api.py`
from  api_dev_2 import make_prediction
from api_dev import geocode_bp

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

# this is an example of a get request
#  go to this link to see: http://127.0.0.1:5000/get_test
@app.route('/make_flood_prediction',  methods=['GET'])
def get_test():
    lat = request.args.get('lat')
    long = request.args.get('long')
    zip = request.args.get('zip')
    try:
        results = make_prediction(zip, lat,long)
        data = {"data": results}
        return jsonify(data), 200
    except Exception as e:
        error_message = {"error": str(e)}
        return jsonify(error_message), 500


# Register the Blueprint with the app
app.register_blueprint(geocode_bp)

if __name__ == '__main__':
    app.run(debug=True)
