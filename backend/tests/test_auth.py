import pytest
from backend.app import create_app, db, bcrypt
from backend.app.models.user import User

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"
    })

    with app.app_context():
        db.create_all()
        hashed_password = bcrypt.generate_password_hash("secret123").decode('utf-8')
        user = User(username="testuser", email="test@example.com", password_hash=hashed_password)
        db.session.add(user)
        db.session.commit()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_successful_login(client):
    response = client.post("/api/login", json={
        "username": "testuser",
        "password": "secret123"
    })
    assert response.status_code == 200
    data = response.get_json()
    assert "access_token" in data

def test_failed_login_invalid_password(client):
    response = client.post("/api/login", json={
        "username": "testuser",
        "password": "wrongpassword"
    })
    assert response.status_code == 401
    data = response.get_json()
    assert data == {"error": "Invalid credentials"}

def test_failed_login_nonexistent_user(client):
    response = client.post("/api/login", json={
        "username": "nonexistent",
        "password": "secret123"
    })
    assert response.status_code == 401
    data = response.get_json()
    assert data == {"error": "Invalid credentials"}
