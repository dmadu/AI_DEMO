import pytest
from app import create_app
from app.extensions import db
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
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_successful_registration(client, app):
    response = client.post('/api/register', json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "ValidPass1!"
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
    assert "password" not in data
    assert "password_hash" not in data

    with app.app_context():
        user = User.query.filter_by(email="test@example.com").first()
        assert user is not None
        assert user.password_hash != "ValidPass1!"

def test_invalid_email_format(client):
    response = client.post('/api/register', json={
        "username": "testuser",
        "email": "invalid-email",
        "password": "ValidPass1!"
    })
    assert response.status_code == 400
    assert "email" in response.get_json()["error"].lower()

def test_password_too_short(client):
    response = client.post('/api/register', json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "Val1!"
    })
    assert response.status_code == 400
    assert "8 characters" in response.get_json()["error"]

def test_password_missing_uppercase(client):
    response = client.post('/api/register', json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "validpass1!"
    })
    assert response.status_code == 400
    assert "uppercase" in response.get_json()["error"]

def test_password_missing_number(client):
    response = client.post('/api/register', json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "ValidPass!"
    })
    assert response.status_code == 400
    assert "numeric digit" in response.get_json()["error"]

def test_password_missing_special_character(client):
    response = client.post('/api/register', json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "ValidPass1"
    })
    assert response.status_code == 400
    assert "special character" in response.get_json()["error"]

def test_duplicate_email_registration(client):
    client.post('/api/register', json={
        "username": "user1",
        "email": "duplicate@example.com",
        "password": "ValidPass1!"
    })
    response = client.post('/api/register', json={
        "username": "user2",
        "email": "duplicate@example.com",
        "password": "ValidPass1!"
    })
    assert response.status_code == 409
    assert "email" in response.get_json()["error"].lower()

def test_duplicate_username_registration(client):
    client.post('/api/register', json={
        "username": "samename",
        "email": "email1@example.com",
        "password": "ValidPass1!"
    })
    response = client.post('/api/register', json={
        "username": "samename",
        "email": "email2@example.com",
        "password": "ValidPass1!"
    })
    assert response.status_code == 409
    assert "username" in response.get_json()["error"].lower()
