"""Tests for features/users/repository.py."""
import pytest
from sqlalchemy.orm import Session

from features.users.repository import UserRepository
from shared.database import UserModel


class TestUserRepository:
    """Tests for UserRepository."""

    def test_get_by_id_found(self, test_db_session: Session, sample_user: UserModel):
        """Test getting user by ID when user exists."""
        repository = UserRepository(test_db_session)
        user = repository.get_by_id(sample_user.id)

        assert user is not None
        assert user.id == sample_user.id
        assert user.email == sample_user.email

    def test_get_by_id_not_found(self, test_db_session: Session):
        """Test getting user by ID when user doesn't exist."""
        repository = UserRepository(test_db_session)
        user = repository.get_by_id(999999)

        assert user is None

    def test_get_by_email_found(self, test_db_session: Session, sample_user: UserModel):
        """Test getting user by email when user exists."""
        repository = UserRepository(test_db_session)
        user = repository.get_by_email(sample_user.email)

        assert user is not None
        assert user.id == sample_user.id
        assert user.email == sample_user.email

    def test_get_by_email_not_found(self, test_db_session: Session):
        """Test getting user by email when user doesn't exist."""
        repository = UserRepository(test_db_session)
        user = repository.get_by_email("nonexistent@example.com")

        assert user is None

    def test_get_by_username_found(self, test_db_session: Session, sample_user: UserModel):
        """Test getting user by username when user exists."""
        repository = UserRepository(test_db_session)
        user = repository.get_by_username(sample_user.username)

        assert user is not None
        assert user.id == sample_user.id
        assert user.username == sample_user.username

    def test_get_by_username_not_found(self, test_db_session: Session):
        """Test getting user by username when user doesn't exist."""
        repository = UserRepository(test_db_session)
        user = repository.get_by_username("nonexistent")

        assert user is None

    def test_get_all(self, test_db_session: Session, multiple_users):
        """Test getting all users."""
        repository = UserRepository(test_db_session)
        users = repository.get_all()

        assert len(users) == 5
        assert all(isinstance(user, UserModel) for user in users)

    def test_get_all_with_pagination(self, test_db_session: Session, multiple_users):
        """Test getting all users with pagination."""
        repository = UserRepository(test_db_session)

        # Get first 2 users
        users_page1 = repository.get_all(skip=0, limit=2)
        assert len(users_page1) == 2

        # Get next 2 users
        users_page2 = repository.get_all(skip=2, limit=2)
        assert len(users_page2) == 2

        # Ensure different users
        assert users_page1[0].id != users_page2[0].id

    def test_count(self, test_db_session: Session, multiple_users):
        """Test counting users."""
        repository = UserRepository(test_db_session)
        count = repository.count()

        assert count == 5

    def test_count_empty(self, test_db_session: Session):
        """Test counting users when no users exist."""
        repository = UserRepository(test_db_session)
        count = repository.count()

        assert count == 0

    def test_create(self, test_db_session: Session):
        """Test creating a user."""
        repository = UserRepository(test_db_session)
        user_data = {
            "email": "new@example.com",
            "username": "newuser",
            "full_name": "New User"
        }

        user = repository.create(user_data)

        assert user.id is not None
        assert user.email == "new@example.com"
        assert user.username == "newuser"
        assert user.full_name == "New User"
        assert user.created_at is not None
        assert user.updated_at is not None

    def test_update(self, test_db_session: Session, sample_user: UserModel):
        """Test updating a user."""
        repository = UserRepository(test_db_session)
        update_data = {
            "full_name": "Updated Name",
            "email": "updated@example.com"
        }

        updated_user = repository.update(sample_user, update_data)

        assert updated_user.id == sample_user.id
        assert updated_user.full_name == "Updated Name"
        assert updated_user.email == "updated@example.com"
        assert updated_user.username == sample_user.username  # Unchanged

    def test_update_with_none_values(self, test_db_session: Session, sample_user: UserModel):
        """Test updating a user with None values (should skip None values)."""
        repository = UserRepository(test_db_session)
        original_email = sample_user.email

        update_data = {
            "full_name": "Updated Name",
            "email": None
        }

        updated_user = repository.update(sample_user, update_data)

        assert updated_user.full_name == "Updated Name"
        assert updated_user.email == original_email  # Should remain unchanged

    def test_delete(self, test_db_session: Session, sample_user: UserModel):
        """Test deleting a user."""
        repository = UserRepository(test_db_session)
        user_id = sample_user.id

        repository.delete(sample_user)

        # Verify user is deleted
        deleted_user = repository.get_by_id(user_id)
        assert deleted_user is None
