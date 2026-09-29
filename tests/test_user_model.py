import pytest
from sqlalchemy.exc import IntegrityError
from src.models.user import User

def test_user_creation(db_session):
    user = User(
        username="testuser",
        email="test@example.com",
        hashed_password="hashed_secret"
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    assert user.id is not None
    assert user.username == "testuser"
    assert user.email == "test@example.com"
    assert user.hashed_password == "hashed_secret"
    assert user.created_at is not None
    assert user.updated_at is not None

def test_unique_username_constraint(db_session):
    user1 = User(
        username="duplicate",
        email="user1@example.com",
        hashed_password="hash1"
    )
    db_session.add(user1)
    db_session.commit()

    user2 = User(
        username="duplicate",
        email="user2@example.com",
        hashed_password="hash2"
    )
    db_session.add(user2)
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()

def test_unique_email_constraint(db_session):
    user1 = User(
        username="user1",
        email="duplicate@example.com",
        hashed_password="hash1"
    )
    db_session.add(user1)
    db_session.commit()

    user2 = User(
        username="user2",
        email="duplicate@example.com",
        hashed_password="hash2"
    )
    db_session.add(user2)
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()
