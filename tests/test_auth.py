import pytest
from app import create_app, db
from app.models import User

@pytest.fixture
def app():
    app = create_app()
    with app.app_context():
        db.create_all()
        user = User(username="testuser", email="test@example.com")
        user.set_password("correctpassword")
        db.session.add(user)
        db.session.commit()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_login_success_username(client):
    response = client.post('/api/auth/login', json={
        "username": "testuser",
        "password": "correctpassword"
    })
    assert response.status_code == 200
    data = response.get_json()
    assert "access_token" in data or "token" in data

def test_login_success_email(client):
    response = client.post('/api/auth/login', json={
        "identifier": "test@example.com",
        "password": "correctpassword"
    })
    if response.status_code != 200:
        response = client.post('/api/auth/login', json={
            "email": "test@example.com",
            "password": "correctpassword"
        })
    assert response.status_code == 200
    data = response.get_json()
    assert "access_token" in data or "token" in data

def test_login_failed_nonexistent_user(client):
    response = client.post('/api/auth/login', json={
        "username": "nonexistent",
        "password": "password"
    })
    assert response.status_code == 401

def test_login_failed_incorrect_password(client):
    response = client.post('/api/auth/login', json={
        "username": "testuser",
        "password": "wrongpassword"
    })
    assert response.status_code == 401

def test_login_missing_fields(client):
    response = client.post('/api/auth/login', json={
        "username": "testuser"
    })
    assert response.status_code == 400
