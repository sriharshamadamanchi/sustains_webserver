from flask import Flask
from flask_cors import CORS
from flask_pymongo import PyMongo

from src.blog.api import blog_api

mongo = PyMongo()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

def create_app():
    app.register_blueprint(blog_api)

    app.config['DEBUG'] = True
    app.config[
        'MONGO_URI'] = "mongodb+srv://sriharshamadamanchi:Harsha1642@database.l2gng.mongodb.net/Blog?retryWrites=true&w=majority"

    mongo.init_app(app)

    return app
