from src.extensions import db, migrate, bcrypt

def test_extensions_initialized(app):
    assert db is not None
    assert migrate is not None
    assert bcrypt is not None

    # Check that app has extensions bound
    assert 'sqlalchemy' in app.extensions
    assert 'migrate' in app.extensions
    assert 'bcrypt' in app.extensions
