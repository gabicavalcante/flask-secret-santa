from flask import Flask
from flask_migrate import Migrate
from dynaconf import FlaskDynaconf


def create_app():
    app = Flask(__name__)

    # initialize the FlaskDynaconf extension in our app
    FlaskDynaconf(app)

    from app.models import db, Draw

    db.init_app(app)
    Migrate(app, db)

    from app.admin import admin
    admin.init_app(app) 

    from app.routes import bot

    app.register_blueprint(bot)

    return app