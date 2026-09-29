import pytest
from sqlalchemy.exc import IntegrityError
from app.models.user import User

def test_user_model_creation(db_session):
    user = User(
        email="test@example.com",
        username="testuser",
        password_hash="hashed_secret"
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    assert user.id is not None
    assert user.email == "test@example.com"
    assert user.username == "testuser"
    assert user.password_hash == "hashed_secret"
    assert user.created_at is not None
    assert user.updated_at is not None

def test_user_email_unique_constraint(db_session):
    user1 = User(
        email="unique@example.com",
        username="user1",
        password_hash="hashed_secret"
    )
    db_session.add(user1)
    db_session.commit()

    user2 = User(
        email="unique@example.com",
        username="user2",
        password_hash="hashed_secret"
    )
    db_session.add(user2)
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()

def test_user_username_unique_constraint(db_session):
    user1 = User(
        email="email1@example.com",
        username="sameusername",
        password_hash="hashed_secret"
    )
    db_session.add(user1)
    db_session.commit()

    user2 = User(
        email="email2@example.com",
        username="sameusername",
        password_hash="hashed_secret"
    )
    db_session.add(user2)
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()

def test_user_nullable_constraints(db_session):
    # Missing email
    user_no_email = User(
        username="noemail",
        password_hash="hashed_secret"
    )
    db_session.add(user_no_email)
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()

    # Missing username
    user_no_username = User(
        email="nousername@example.com",
        password_hash="hashed_secret"
    )
    db_session.add(user_no_username)
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()

    # Missing password_hash
    user_no_password = User(
        email="nopassword@example.com",
        username="nopassword"
    )
    db_session.add(user_no_password)
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()
