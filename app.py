from flask import Flask, g, jsonify,render_template
from flask_login import LoginManager, current_user
login_manager = LoginManager()
from flask_cors import CORS
import models
from resources.users import users_api
from resources.photos import photos_api
import config


app = Flask(__name__)
app.secret_key = config.SECRET_KEY

login_manager.init_app(app)


@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id==userid)
    except models.DoesNotExist:
        return None

CORS(photos_api, origins=["http://localhost:3000"], support_credentials=True)
CORS(users_api, origins=["http://localhost:3000"], support_credentials=True)


app.register_blueprint(photos_api, url_prefix='/photos')
app.register_blueprint(users_api, url_prefix='/users')



@app.before_request
def before_request():
    """Connect to the database before each request"""
    g.db = models.DATABASE
    g.db.connect()
    g.user = current_user

@app.after_request
def after_request(response):
    """Close the database connection after each request"""
    g.db.close()
    return response

@app.route('/')
def index():
    return render_template('index.html')
 


if __name__ == '__main__':
    models.initialize()
    app.run(debug=config.DEBUG, port=config.PORT)