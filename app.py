from flask import Flask, jsonify, render_template
import api  # Importing the file `api.py`
import api_dev
import api_dev_2

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

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


if __name__ == '__main__':
    app.run(debug=True)