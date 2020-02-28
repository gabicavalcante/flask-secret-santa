from flask import Flask
from flask_migrate import Migrate
from dynaconf import FlaskDynaconf


def create_app(**config):
    app = Flask(__name__)

    # initialize the FlaskDynaconf extension in our app
    FlaskDynaconf(app, **config)

    # initialize the database and the Migrate extension
    from app.models import db

    db.init_app(app)
    Migrate(app, db)

    # register the blueprint
    from app.routes import bot

    app.register_blueprint(bot)

    return app
