import unittest
from app import app, db, User

class LoginTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = app.test_client()
        with app.app_context():
            db.create_all()
            user = User(username='testuser')
            user.set_password('correctpassword')
            db.session.add(user)
            db.session.commit()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_login_page_loads(self):
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'username', response.data)
        self.assertIn(b'password', response.data)
        self.assertIn(b'Register here', response.data)

    def test_login_success(self):
        response = self.client.post('/login', json={
            'username': 'testuser',
            'password': 'correctpassword'
        })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('access_token', data)

    def test_login_invalid_credentials(self):
        response = self.client.post('/login', json={
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 401)
        data = response.get_json()
        self.assertIn('error', data)

if __name__ == '__main__':
    unittest.main()
