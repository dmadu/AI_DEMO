import pytest
from src import create_app
from src.extensions import db as _db

@pytest.fixture(scope='session')
):
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        yield app

@pytest.fixture(scope='function')
    with app.app_context():
        _db.create_all()
        yield _db
        _db.session.remove()
        _db.drop_all()

@pytest.fixture(scope='function')
    return app.test_client()
