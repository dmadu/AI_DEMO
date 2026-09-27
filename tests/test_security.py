from src.extensions import bcrypt

def test_password_hashing(app):
    password = "secure_password_123"
    hashed = bcrypt.generate_password_hash(password).decode('utf-8')

    assert hashed != password
    assert bcrypt.check_password_hash(hashed, password) is True
    assert bcrypt.check_password_hash(hashed, "wrong_password") is False
