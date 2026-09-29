import pytest
from app import create_app, db
from app.models import User
from flask_jwt_extended import create_access_token

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
        if hasattr(user, 'set_password'):
            user.set_password("password123")
        else:
            user.password = "password123"
        db.session.add(user)
        db.session.commit()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_dashboard_success(client, app):
    with app.app_context():
        user = User.query.filter_by(email="test@example.com").first()
        access_token = create_access_token(identity=user.id if hasattr(user, 'id') else user.email)

    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = client.get("/api/dashboard", headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    assert "Welcome" in data.get("message", "")
    assert "user" in data

def test_dashboard_missing_token(client):
    response = client.get("/api/dashboard")
    assert response.status_code == 401

def test_dashboard_invalid_token(client):
    headers = {
        "Authorization": "Bearer invalid_token_string"
    }
    response = client.get("/api/dashboard", headers=headers)
    assert response.status_code == 401
