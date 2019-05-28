from flask import Flask, g, jsonify,render_template
from flask_login import LoginManager
login_manager = LoginManager()
from flask_cors import CORS
import models
from resources.photos import photos_api
from resources.users import users_api
import config

app = Flask(__name__)
app.secret_key = config.SECRET_KEY

login_manager.init_app(app)


# @login_manager.user_loader
# def load_user(userid)
#     try:
#         return models.User.get 

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
    return render_template('index.html')

@app.route('/users')
def asdasd():
    return jsonify({"asdasd" : "i'm data"})

if __name__ == '__main__':
    models.initialize()
    app.run(debug=config.DEBUG, port=config.PORT)