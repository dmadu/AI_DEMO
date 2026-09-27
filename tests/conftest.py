import pytest
from src.app import create_app
from src.extensions import db as _db

@pytest.fixture(scope='session')
):
def app():
    app = create_app('testing')
    with app.app_context():
        yield app

@pytest.fixture(scope='function')
):
def db(app):
    _db.create_all()
    yield _db
    _db.session.remove()
    _db.drop_all()

@pytest.fixture(scope='function')
):
def client(app):
    return app.test_client()
