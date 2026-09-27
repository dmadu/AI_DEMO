def test_config_is_testing(app):
    assert app.config['TESTING'] is True

def test_health_check(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert response.get_json() == {'status': 'healthy'}
