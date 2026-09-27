import pytest
from src.models import User
from src.extensions import bcrypt

def test_register_success(client):
    response = client.post('/api/register', json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "ValidPass1!"
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data["message"] == "User registered successfully"
    assert data["user"]["username"] == "testuser"
    assert data["user"]["email"] == "test@example.com"

    user = User.query.filter_by(email="test@example.com").first()
    assert user is not None
    assert user.password_hash != "ValidPass1!"
    assert bcrypt.check_password_hash(user.password_hash, "ValidPass1!")

def test_register_invalid_email(client):
    response = client.post('/api/register', json={
        "username": "testuser",
        "email": "invalid-email",
        "password": "ValidPass1!"
    })
    assert response.status_code == 400
    data = response.get_json()
    assert "email" in data["error"].lower()

def test_register_weak_password_length(client):
    response = client.post('/api/register', json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "Short1!"
    })
    assert response.status_code == 400

def test_register_weak_password_uppercase(client):
    response = client.post('/api/register', json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "lowercase1!"
    })
    assert response.status_code == 400

def test_register_weak_password_digit(client):
    response = client.post('/api/register', json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "NoDigitPass!"
    })
    assert response.status_code == 400

def test_register_weak_password_special(client):
    response = client.post('/api/register', json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "NoSpecialPass1"
    })
    assert response.status_code == 400

def test_register_duplicate_email(client):
    client.post('/api/register', json={
        "username": "user1",
        "email": "duplicate@example.com",
        "password": "ValidPass1!"
    })
    response = client.post('/api/register', json={
        "username": "user2",
        "email": "duplicate@example.com",
        "password": "ValidPass2!"
    })
    assert response.status_code == 400
    data = response.get_json()
    assert "already registered" in data["error"].lower()

def test_register_duplicate_username(client):
    client.post('/api/register', json={
        "username": "sameuser",
        "email": "email1@example.com",
        "password": "ValidPass1!"
    })
    response = client.post('/api/register', json={
        "username": "sameuser",
        "email": "email2@example.com",
        "password": "ValidPass2!"
    })
    assert response.status_code == 400
    data = response.get_json()
    assert "already taken" in data["error"].lower()
