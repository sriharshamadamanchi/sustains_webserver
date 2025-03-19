from flask import Flask
from flask_cors import CORS
from flask_mail import Mail
from flask_pymongo import PyMongo

from src.auth.api import auth_api
from src.blog.api import blog_api

mongo = PyMongo()
mail = Mail()


def create_app():
    app = Flask(__name__)

    CORS(app)

    app.register_blueprint(blog_api)
    app.register_blueprint(auth_api)

    app.config['DEBUG'] = True
    app.config[
        'MONGO_URI'] = "mongodb+srv://sriharshamadamanchi:Harsha1642@database.l2gng.mongodb.net/Blog?retryWrites=true&w=majority"

    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
    app.config['MAIL_USERNAME'] = 'harshahari1642@gmail.com'
    app.config['MAIL_PASSWORD'] = 'pcgs xujm fpht jnrv'
    app.config['MAIL_DEFAULT_SENDER'] = 'harshahari1642@gmail.com'

    mongo.init_app(app)
    mail.init_app(app)

    return app
