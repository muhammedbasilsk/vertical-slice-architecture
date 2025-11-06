"""Tests for features/users/models.py."""
import pytest
from datetime import datetime
from pydantic import ValidationError

from features.users.models import UserBase, UserCreate, UserUpdate, UserResponse, UserListResponse


class TestUserBase:
    """Tests for UserBase model."""

    def test_valid_user_base(self):
        """Test creating a valid UserBase."""
        user = UserBase(
            email="test@example.com",
            username="testuser",
            full_name="Test User"
        )

        assert user.email == "test@example.com"
        assert user.username == "testuser"
        assert user.full_name == "Test User"

    def test_invalid_email(self):
        """Test UserBase with invalid email."""
        with pytest.raises(ValidationError) as exc_info:
            UserBase(
                email="invalid-email",
                username="testuser",
                full_name="Test User"
            )

        errors = exc_info.value.errors()
        assert any("email" in str(error["loc"]) for error in errors)

    def test_short_username(self):
        """Test UserBase with username too short."""
        with pytest.raises(ValidationError) as exc_info:
            UserBase(
                email="test@example.com",
                username="ab",  # Less than 3 characters
                full_name="Test User"
            )

        errors = exc_info.value.errors()
        assert any("username" in str(error["loc"]) for error in errors)

    def test_long_username(self):
        """Test UserBase with username too long."""
        with pytest.raises(ValidationError) as exc_info:
            UserBase(
                email="test@example.com",
                username="a" * 51,  # More than 50 characters
                full_name="Test User"
            )

        errors = exc_info.value.errors()
        assert any("username" in str(error["loc"]) for error in errors)

    def test_empty_full_name(self):
        """Test UserBase with empty full name."""
        with pytest.raises(ValidationError) as exc_info:
            UserBase(
                email="test@example.com",
                username="testuser",
                full_name=""
            )

        errors = exc_info.value.errors()
        assert any("full_name" in str(error["loc"]) for error in errors)

    def test_long_full_name(self):
        """Test UserBase with full name too long."""
        with pytest.raises(ValidationError) as exc_info:
            UserBase(
                email="test@example.com",
                username="testuser",
                full_name="a" * 101  # More than 100 characters
            )

        errors = exc_info.value.errors()
        assert any("full_name" in str(error["loc"]) for error in errors)

    def test_missing_fields(self):
        """Test UserBase with missing required fields."""
        with pytest.raises(ValidationError) as exc_info:
            UserBase(email="test@example.com")

        errors = exc_info.value.errors()
        assert len(errors) >= 2  # Missing username and full_name


class TestUserCreate:
    """Tests for UserCreate model."""

    def test_valid_user_create(self):
        """Test creating a valid UserCreate."""
        user = UserCreate(
            email="test@example.com",
            username="testuser",
            full_name="Test User"
        )

        assert user.email == "test@example.com"
        assert user.username == "testuser"
        assert user.full_name == "Test User"

    def test_inherits_from_user_base(self):
        """Test that UserCreate inherits from UserBase."""
        assert issubclass(UserCreate, UserBase)


class TestUserUpdate:
    """Tests for UserUpdate model."""

    def test_valid_user_update_all_fields(self):
        """Test creating a UserUpdate with all fields."""
        user = UserUpdate(
            email="updated@example.com",
            username="updateduser",
            full_name="Updated User"
        )

        assert user.email == "updated@example.com"
        assert user.username == "updateduser"
        assert user.full_name == "Updated User"

    def test_user_update_partial_fields(self):
        """Test creating a UserUpdate with partial fields."""
        user = UserUpdate(full_name="Updated User")

        assert user.full_name == "Updated User"
        assert user.email is None
        assert user.username is None

    def test_user_update_empty(self):
        """Test creating an empty UserUpdate."""
        user = UserUpdate()

        assert user.email is None
        assert user.username is None
        assert user.full_name is None

    def test_user_update_validation(self):
        """Test that UserUpdate validates fields."""
        with pytest.raises(ValidationError):
            UserUpdate(email="invalid-email")

    def test_user_update_short_username(self):
        """Test UserUpdate with username too short."""
        with pytest.raises(ValidationError) as exc_info:
            UserUpdate(username="ab")

        errors = exc_info.value.errors()
        assert any("username" in str(error["loc"]) for error in errors)


class TestUserResponse:
    """Tests for UserResponse model."""

    def test_valid_user_response(self):
        """Test creating a valid UserResponse."""
        user = UserResponse(
            id=1,
            email="test@example.com",
            username="testuser",
            full_name="Test User",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        assert user.id == 1
        assert user.email == "test@example.com"
        assert user.username == "testuser"
        assert user.full_name == "Test User"
        assert isinstance(user.created_at, datetime)
        assert isinstance(user.updated_at, datetime)

    def test_inherits_from_user_base(self):
        """Test that UserResponse inherits from UserBase."""
        assert issubclass(UserResponse, UserBase)

    def test_missing_required_fields(self):
        """Test UserResponse with missing required fields."""
        with pytest.raises(ValidationError) as exc_info:
            UserResponse(
                email="test@example.com",
                username="testuser",
                full_name="Test User"
            )

        errors = exc_info.value.errors()
        # Should be missing id, created_at, updated_at
        assert len(errors) >= 3


class TestUserListResponse:
    """Tests for UserListResponse model."""

    def test_valid_user_list_response(self):
        """Test creating a valid UserListResponse."""
        users = [
            UserResponse(
                id=1,
                email="user1@example.com",
                username="user1",
                full_name="User 1",
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            ),
            UserResponse(
                id=2,
                email="user2@example.com",
                username="user2",
                full_name="User 2",
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
        ]

        response = UserListResponse(users=users, total=2)

        assert len(response.users) == 2
        assert response.total == 2
        assert all(isinstance(user, UserResponse) for user in response.users)

    def test_empty_user_list_response(self):
        """Test creating an empty UserListResponse."""
        response = UserListResponse(users=[], total=0)

        assert len(response.users) == 0
        assert response.total == 0

    def test_missing_required_fields(self):
        """Test UserListResponse with missing required fields."""
        with pytest.raises(ValidationError):
            UserListResponse(users=[])  # Missing total
