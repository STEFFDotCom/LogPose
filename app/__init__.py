from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from app.blueprints.auth.auth import auth

db = SQLAlchemy()

login_manager = LoginManager()

def create_app():

    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///logpose.db"

    db.init_app(app)

    from app import models

    login_manager.init_app(app)

    # Register blueprints here

    app.register_blueprint(auth)

    return app