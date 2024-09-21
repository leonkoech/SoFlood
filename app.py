from flask import Flask, jsonify, render_template
import api  # Importing the file `api.py`
import api_dev_2
from api_dev import geocode_bp

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/results')
def results():
    return render_template('results.html')

# this is an example of a get request
#  go to this link to see: http://127.0.0.1:5000/get_test
@app.route('/get_test',  methods=['GET'])
def get_test():
    try:
        data = {"message": "this is my data"}
        return jsonify(data), 200
    except Exception as e:
        error_message = {"error": str(e)}
        return jsonify(error_message), 500


# Register the Blueprint with the app
app.register_blueprint(geocode_bp)

if __name__ == '__main__':
    app.run(debug=True)
