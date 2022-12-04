import os
from flask import Flask
from dotenv import load_dotenv, find_dotenv
from flask_cors import CORS

load_dotenv(find_dotenv())

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config['SECRET_KEY'] =os.environ.get("SECRET_KEY")
  
    from .auth import auth

    app.register_blueprint(auth, url_prefix="/auth")

    return app
