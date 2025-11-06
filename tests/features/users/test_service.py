"""Tests for features/users/service.py."""
import pytest
from fastapi import HTTPException
from sqlalchemy.orm import Session

from features.users.models import UserCreate, UserUpdate
from features.users.repository import UserRepository
from features.users.service import UserService
from shared.database import UserModel


class TestUserService:
    """Tests for UserService."""

    def test_get_user_found(self, test_db_session: Session, sample_user: UserModel):
        """Test getting a user that exists."""
        repository = UserRepository(test_db_session)
        service = UserService(repository)

        user = service.get_user(sample_user.id)

        assert user.id == sample_user.id
        assert user.email == sample_user.email
        assert user.username == sample_user.username
        assert user.full_name == sample_user.full_name

    def test_get_user_not_found(self, test_db_session: Session):
        """Test getting a user that doesn't exist."""
        repository = UserRepository(test_db_session)
        service = UserService(repository)

        with pytest.raises(HTTPException) as exc_info:
            service.get_user(999999)

        assert exc_info.value.status_code == 404
        assert "not found" in str(exc_info.value.detail)

    def test_get_users(self, test_db_session: Session, multiple_users):
        """Test getting all users."""
        repository = UserRepository(test_db_session)
        service = UserService(repository)

        result = service.get_users()

        assert result.total == 5
        assert len(result.users) == 5
        assert all(user.email for user in result.users)

    def test_get_users_with_pagination(self, test_db_session: Session, multiple_users):
        """Test getting users with pagination."""
        repository = UserRepository(test_db_session)
        service = UserService(repository)

        result = service.get_users(skip=1, limit=2)

        assert result.total == 5
        assert len(result.users) == 2

    def test_get_users_empty(self, test_db_session: Session):
        """Test getting users when no users exist."""
        repository = UserRepository(test_db_session)
        service = UserService(repository)

        result = service.get_users()

        assert result.total == 0
        assert len(result.users) == 0

    def test_create_user_success(self, test_db_session: Session):
        """Test creating a user successfully."""
        repository = UserRepository(test_db_session)
        service = UserService(repository)

        user_data = UserCreate(
            email="new@example.com",
            username="newuser",
            full_name="New User"
        )

        user = service.create_user(user_data)

        assert user.id is not None
        assert user.email == "new@example.com"
        assert user.username == "newuser"
        assert user.full_name == "New User"

    def test_create_user_duplicate_email(self, test_db_session: Session, sample_user: UserModel):
        """Test creating a user with duplicate email."""
        repository = UserRepository(test_db_session)
        service = UserService(repository)

        user_data = UserCreate(
            email=sample_user.email,
            username="differentuser",
            full_name="Different User"
        )

        with pytest.raises(HTTPException) as exc_info:
            service.create_user(user_data)

        assert exc_info.value.status_code == 400
        assert "Email already registered" in str(exc_info.value.detail)

    def test_create_user_duplicate_username(self, test_db_session: Session, sample_user: UserModel):
        """Test creating a user with duplicate username."""
        repository = UserRepository(test_db_session)
        service = UserService(repository)

        user_data = UserCreate(
            email="different@example.com",
            username=sample_user.username,
            full_name="Different User"
        )

        with pytest.raises(HTTPException) as exc_info:
            service.create_user(user_data)

        assert exc_info.value.status_code == 400
        assert "Username already taken" in str(exc_info.value.detail)

    def test_update_user_success(self, test_db_session: Session, sample_user: UserModel):
        """Test updating a user successfully."""
        repository = UserRepository(test_db_session)
        service = UserService(repository)

        update_data = UserUpdate(
            full_name="Updated Name"
        )

        updated_user = service.update_user(sample_user.id, update_data)

        assert updated_user.id == sample_user.id
        assert updated_user.full_name == "Updated Name"
        assert updated_user.email == sample_user.email

    def test_update_user_not_found(self, test_db_session: Session):
        """Test updating a user that doesn't exist."""
        repository = UserRepository(test_db_session)
        service = UserService(repository)

        update_data = UserUpdate(full_name="Updated Name")

        with pytest.raises(HTTPException) as exc_info:
            service.update_user(999999, update_data)

        assert exc_info.value.status_code == 404
        assert "not found" in str(exc_info.value.detail)

    def test_update_user_duplicate_email(self, test_db_session: Session, multiple_users):
        """Test updating a user with an email that already exists."""
        repository = UserRepository(test_db_session)
        service = UserService(repository)

        user1 = multiple_users[0]
        user2 = multiple_users[1]

        update_data = UserUpdate(email=user2.email)

        with pytest.raises(HTTPException) as exc_info:
            service.update_user(user1.id, update_data)

        assert exc_info.value.status_code == 400
        assert "Email already registered" in str(exc_info.value.detail)

    def test_update_user_duplicate_username(self, test_db_session: Session, multiple_users):
        """Test updating a user with a username that already exists."""
        repository = UserRepository(test_db_session)
        service = UserService(repository)

        user1 = multiple_users[0]
        user2 = multiple_users[1]

        update_data = UserUpdate(username=user2.username)

        with pytest.raises(HTTPException) as exc_info:
            service.update_user(user1.id, update_data)

        assert exc_info.value.status_code == 400
        assert "Username already taken" in str(exc_info.value.detail)

    def test_update_user_same_email(self, test_db_session: Session, sample_user: UserModel):
        """Test updating a user with their own email (should succeed)."""
        repository = UserRepository(test_db_session)
        service = UserService(repository)

        update_data = UserUpdate(
            email=sample_user.email,
            full_name="Updated Name"
        )

        updated_user = service.update_user(sample_user.id, update_data)

        assert updated_user.email == sample_user.email
        assert updated_user.full_name == "Updated Name"

    def test_update_user_same_username(self, test_db_session: Session, sample_user: UserModel):
        """Test updating a user with their own username (should succeed)."""
        repository = UserRepository(test_db_session)
        service = UserService(repository)

        update_data = UserUpdate(
            username=sample_user.username,
            full_name="Updated Name"
        )

        updated_user = service.update_user(sample_user.id, update_data)

        assert updated_user.username == sample_user.username
        assert updated_user.full_name == "Updated Name"

    def test_delete_user_success(self, test_db_session: Session, sample_user: UserModel):
        """Test deleting a user successfully."""
        repository = UserRepository(test_db_session)
        service = UserService(repository)
        user_id = sample_user.id

        service.delete_user(user_id)

        # Verify user is deleted
        with pytest.raises(HTTPException):
            service.get_user(user_id)

    def test_delete_user_not_found(self, test_db_session: Session):
        """Test deleting a user that doesn't exist."""
        repository = UserRepository(test_db_session)
        service = UserService(repository)

        with pytest.raises(HTTPException) as exc_info:
            service.delete_user(999999)

        assert exc_info.value.status_code == 404
        assert "not found" in str(exc_info.value.detail)
