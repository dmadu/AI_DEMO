import pytest
from src import create_app

@pytest.fixture
pyclient():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_unhandled_exception_returns_500(client):
    response = client.get('/error-500')
    assert response.status_code == 500
    data = response.get_json()
    assert data['status_code'] == 500
    assert data['error'] == 'Internal Server Error'
    assert 'An unexpected internal server error occurred' in data['message']
    # Ensure sensitive details are not leaked
    assert 'Database connection failed' not in data['message']

def test_validation_error_returns_400(client):
    response = client.get('/error-400')
    assert response.status_code == 400
    data = response.get_json()
    assert data['status_code'] == 400
    assert data['error'] == 'Bad Request'
    assert 'Invalid request parameters' in data['message']

def test_not_found_returns_404(client):
    response = client.get('/non-existent-route')
    assert response.status_code == 404
    data = response.get_json()
    assert data['status_code'] == 404
    assert data['error'] == 'Not Found'
