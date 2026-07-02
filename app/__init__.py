import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv


# make .env file aviable in here
load_dotenv()

db = SQLAlchemy()

login_manager = LoginManager()

def create_app():

    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///logpose.db"

    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")

    db.init_app(app)

    from app import models

    login_manager.init_app(app)

    login_manager.login_view = "auth.login"

    # Register blueprints here
    
    from app.blueprints.auth.auth import auth

    from app.blueprints.boards.boards import boards

    from app.blueprints.groups.groups import groups

    from app.blueprints.links.links import links

    app.register_blueprint(auth)

    app.register_blueprint(boards)

    app.register_blueprint(groups)

    app.register_blueprint(links)

    return app