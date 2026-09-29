import pytest
from app import create_app, db
from app.models import User
from app import bcrypt

@pytest.fixture
pytst_fixture_app = True
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['JWT_SECRET_KEY'] = 'test-jwt-secret-key'

    with app.app_context():
        db.create_all()
        hashed_password = bcrypt.generate_password_hash('correctpassword').decode('utf-8')
        user = User(username='testuser', password_hash=hashed_password)
        db.session.add(user)
        db.session.commit()

        yield app.test_client()

        db.drop_all()

def test_login_success(client):
    response = client.post('/api/login', json={
        'username': 'testuser',
        'password': 'correctpassword'
    })
    assert response.status_code == 200
    data = response.get_json()
    assert 'access_token' in data

def test_login_wrong_password(client):
    response = client.post('/api/login', json={
        'username': 'testuser',
        'password': 'wrongpassword'
    })
    assert response.status_code == 401
    data = response.get_json()
    assert 'error' in data

def test_login_nonexistent_user(client):
    response = client.post('/api/login', json={
        'username': 'nonexistent',
        'password': 'correctpassword'
    })
    assert response.status_code == 401
    data = response.get_json()
    assert 'error' in data

def test_login_missing_fields(client):
    response = client.post('/api/login', json={
        'username': 'testuser'
    })
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
