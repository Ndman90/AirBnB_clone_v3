#!/usr/bin/python3
"""AirBnB Clone API config file"""

from api.v1.views import app_views
from flask import Flask, make_response, jsonify
from models import storage
from os import getenv
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(app_views)
app.url_map.strict_slashes = False
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown_app(exception):
    """
    disconnects and ends the db session
    at the end a request
    """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """
    Handle non existing pages

    Args:
    error: [description]

    Returns:
    JSON: json object
    """

    e = {
        "error": "Not Found"
    }
    return make_response(jsonify({'error': "Not found"}), 404)


@app.errorhandler(400)
def error_400(error):
    '''Handles the 400 HTTP error code.'''
    msg = 'Bad request'
    if isinstance(error, Exception) and hasattr(error, 'description'):
        msg = error.description
    return jsonify(error=msg), 400


if __name__ == '__main__':
    host = getenv("HBNB_API_HOST", "0.0.0.0")
    port = getenv("HBNB_API_PORT", "5000")
    app.run(host=host, port=port, threaded=True)
