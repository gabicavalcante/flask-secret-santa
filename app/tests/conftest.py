import pytest
from sqlalchemy import event

from app.app import create_app
from app.models import db


@pytest.fixture(scope="session")
def app():
    """ Provides an instance of our Flask app
    and set dynaconf env to test """
    app = create_app(FORCE_ENV_FOR_DYNACONF="testing")
    with app.app_context():
        db.create_all(app=app)
        yield app
        db.drop_all(app=app)
