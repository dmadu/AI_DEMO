import pytest
from app import create_app, db
from app.models import User

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"
    })

    with app.app_context():
        db.create_all()
        user = User(username="testuser", email="test@example.com")
        user.set_password("securepassword123")
        db.session.add(user)
        db.session.commit()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_login_success_username(client):
    response = client.post('/api/auth/login', json={
        "identifier": "testuser",
        "password": "securepassword123"
    })
    assert response.status_code == 200
    data = response.get_json()
    assert "access_token" in data
    assert data["user"]["username"] == "testuser"

def test_login_success_email(client):
    response = client.post('/api/auth/login', json={
        "identifier": "test@example.com",
        "password": "securepassword123"
    })
    assert response.status_code == 200
    data = response.get_json()
    assert "access_token" in data
    assert data["user"]["email"] == "test@example.com"

def test_login_incorrect_password(client):
    response = client.post('/api/auth/login', json={
        "identifier": "testuser",
        "password": "wrongpassword"
    })
    assert response.status_code == 401
    data = response.get_json()
    assert "error" in data

def test_login_nonexistent_user(client):
    response = client.post('/api/auth/login', json={
        "identifier": "nonexistent@example.com",
        "password": "securepassword123"
    })
    assert response.status_code == 401
    data = response.get_json()
    assert "error" in data

def test_login_missing_fields(client):
    response = client.post('/api/auth/login', json={
        "identifier": "testuser"
    })
    assert response.status_code == 400
