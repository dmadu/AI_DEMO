import pytest
from app import create_app, db
from app.models import User

@pytest.fixture
py_client():
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'JWT_SECRET_KEY': 'test-jwt-secret'
    })
    
    with app.app_context():
        db.create_all()
        user = User(username='testuser', email='test@example.com')
        user.set_password('securepassword')
        db.session.add(user)
        db.session.commit()
        
        yield app.test_client()
        
        db.drop_all()

def test_login_success_with_username(py_client):
    response = py_client.post('/api/auth/login', json={
        'username': 'testuser',
        'password': 'securepassword'
    })
    assert response.status_code == 200
    data = response.get_json()
    assert 'access_token' in data

def test_login_success_with_email(py_client):
    response = py_client.post('/api/auth/login', json={
        'email': 'test@example.com',
        'password': 'securepassword'
    })
    assert response.status_code == 200
    data = response.get_json()
    assert 'access_token' in data

def test_login_invalid_password(py_client):
    response = py_client.post('/api/auth/login', json={
        'username': 'testuser',
        'password': 'wrongpassword'
    })
    assert response.status_code == 401
    data = response.get_json()
    assert 'error' in data

def test_login_nonexistent_user(py_client):
    response = py_client.post('/api/auth/login', json={
        'username': 'nonexistent',
        'password': 'securepassword'
    })
    assert response.status_code == 401
    data = response.get_json()
    assert 'error' in data
