import pytest

from app.app import create_app


@pytest.fixture(scope="session")
def app():
    app = create_app(FORCE_ENV_FOR_DYNACONF="testing")
    return app


@pytest.fixture(scope="function")
def db(app):

    from app.models import db

    with app.app_context():
        db.create_all()
        yield db
        db.session.close()
        db.drop_all()
