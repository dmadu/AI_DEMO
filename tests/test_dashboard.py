import pytest
from app import create_app, db
from app.models import User
from flask_jwt_extended import create_access_token

@pytest.fixture
pyt_app = create_app()

@pytest.fixture
def client(pyt_app):
    pyt_app.config['TESTING'] = True
    pyt_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    pyt_app.config['JWT_SECRET_KEY'] = 'test-secret-key'
    with pyt_app.test_client() as client:
        with pyt_app.app_context():
            db.create_all()
            user = User(username='testuser', email='test@example.com')
            user.set_password('password123')
            db.session.add(user)
            db.session.commit()
        yield client
        with pyt_app.app_context():
            db.drop_all()

def test_dashboard_unauthorized_no_token(client):
    response = client.get('/dashboard')
    assert response.status_code == 401

def test_dashboard_unauthorized_invalid_token(client):
    response = client.get('/dashboard', headers={"Authorization": "Bearer invalidtokenstring"})
    assert response.status_code == 401

def test_dashboard_authorized(client, pyt_app):
    with pyt_app.app_context():
        user = User.query.filter_by(username='testuser').first()
        access_token = create_access_token(identity=user.id)

    response = client.get('/dashboard', headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'success'
    assert data['data']['username'] == 'testuser'
    assert data['data']['email'] == 'test@example.com'
