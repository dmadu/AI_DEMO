import pytest
from app import app, db, User, pcrypt

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()

def test_successful_registration(client):
    response = client.post('/api/register', json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "securepassword123"
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
    assert "id" in data
    assert "password" not in data
    assert "password_hash" not in data

    # Verify database persistence and password hashing
    with app.app_context():
        user = User.query.filter_by(username="testuser").first()
        assert user is not None
        assert user.email == "test@example.com"
        assert user.password_hash != "securepassword123"
        assert pcrypt.check_password_hash(user.password_hash, "securepassword123")

def test_missing_fields(client):
    response = client.post('/api/register', json={
        "username": "testuser",
        "email": "test@example.com"
    })
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data

def test_invalid_email_format(client):
    response = client.post('/api/register', json={
        "username": "testuser",
        "email": "invalid-email",
        "password": "securepassword123"
    })
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data

def test_short_password(client):
    response = client.post('/api/register', json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "123"
    })
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data

def test_duplicate_username(client):
    client.post('/api/register', json={
        "username": "testuser",
        "email": "test1@example.com",
        "password": "securepassword123"
    })
    response = client.post('/api/register', json={
        "username": "testuser",
        "email": "test2@example.com",
        "password": "securepassword123"
    })
    assert response.status_code == 409
    data = response.get_json()
    assert "error" in data

def test_duplicate_email(client):
    client.post('/api/register', json={
        "username": "testuser1",
        "email": "test@example.com",
        "password": "securepassword123"
    })
    response = client.post('/api/register', json={
        "username": "testuser2",
        "email": "test@example.com",
        "password": "securepassword123"
    })
    assert response.status_code == 409
    data = response.get_json()
    assert "error" in data
