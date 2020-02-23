import pytest

from app.app import create_app


@pytest.fixture
def app():
    app = create_app(FORCE_ENV_FOR_DYNACONF="testing")
    return app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def db(app):
    from app.models import db

    with app.app_context():
        db.create_all()
        yield db
        db.drop_all()
        db.session.commit()
