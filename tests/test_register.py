import pytest
from app import create_app, db, bcrypt
from app.models import User

@pytest.fixture
pyt_client():
    app = create_app()
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['TESTING'] = True
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.drop_all()

@pytest.fixture
client(app=None):
    app = create_app()
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['TESTING'] = True
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.drop_all()

def test_successful_registration(client):
    response = client.post('/api/auth/register', json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "ValidPass1!"
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data["message"] == "User registered successfully."
    assert data["user"]["username"] == "testuser"
    assert data["user"]["email"] == "test@example.com"

    # Check database persistence and hashing
    user = User.query.filter_by(email="test@example.com").first()
    assert user is not None
    assert user.username == "testuser"
    assert bcrypt.check_password_hash(user.password_hash, "ValidPass1!")

def test_invalid_email_format(client):
    response = client.post('/api/auth/register', json={
        "username": "testuser2",
        "email": "invalid-email",
        "password": "ValidPass1!"
    })
    assert response.status_code == 400
    data = response.get_json()
    assert "Invalid email format" in data["error"]

def test_password_length_constraint(client):
    response = client.post('/api/auth/register', json={
        "username": "testuser3",
        "email": "test3@example.com",
        "password": "VPass1!"
    })
    assert response.status_code == 400
    data = response.get_json()
    assert "at least 8 characters" in data["error"]

def test_password_uppercase_constraint(client):
    response = client.post('/api/auth/register', json={
        "username": "testuser4",
        "email": "test4@example.com",
        "password": "validpass1!"
    })
    assert response.status_code == 400
    data = response.get_json()
    assert "uppercase letter" in data["error"]

def test_password_digit_constraint(client):
    response = client.post('/api/auth/register', json={
        "username": "testuser5",
        "email": "test5@example.com",
        "password": "ValidPass!"
    })
    assert response.status_code == 400
    data = response.get_json()
    assert "numeric digit" in data["error"]

def test_password_special_char_constraint(client):
    response = client.post('/api/auth/register', json={
        "username": "testuser6",
        "email": "test6@example.com",
        "password": "ValidPass1"
    })
    assert response.status_code == 400
    data = response.get_json()
    assert "special character" in data["error"]

def test_duplicate_email_registration(client):
    client.post('/api/auth/register', json={
        "username": "userone",
        "email": "duplicate@example.com",
        "password": "ValidPass1!"
    })
    response = client.post('/api/auth/register', json={
        "username": "usertwo",
        "email": "duplicate@example.com",
        "password": "ValidPass2!"
    })
    assert response.status_code == 409
    data = response.get_json()
    assert "Email already registered" in data["error"]

def test_duplicate_username_registration(client):
    client.post('/api/auth/register', json={
        "username": "sameuser",
        "email": "user1@example.com",
        "password": "ValidPass1!"
    })
    response = client.post('/api/auth/register', json={
        "username": "sameuser",
        "email": "user2@example.com",
        "password": "ValidPass2!"
    })
    assert response.status_code == 409
    data = response.get_json()
    assert "Username already taken" in data["error"]

def test_missing_fields(client):
    response = client.post('/api/auth/register', json={
        "username": "incomplete"
    })
    assert response.status_code == 400
    data = response.get_json()
    assert "Missing required fields" in data["error"]
