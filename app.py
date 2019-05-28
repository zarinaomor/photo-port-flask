from flask import Flask
from flask_cors import CORS
import models

import config

app = Flask(__name__)
app.secret_key = config.SECRET_KEY

# app.register_blueprint(photos_api, url_prefix='/api/v1')

@app.before_request
def before_request():
    """Connect to the database before each request"""
    g.db = models.DATABASE
    g.db.connect()

@app.after_request
def after_request(response):
    """Close the database connection after each request"""
    g.db.close()
    return response

@app.route('/')
def index():
    return jsonify({"data" : "i'm data"})

@app.route('/users')
def asdasd():
    return jsonify({"asdasd" : "i'm data"})

if __name__ == '__main__':
    models.initialize()
    app.run(debug=config.DEBUG, port=config.PORT)