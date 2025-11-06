"""Tests for features/users/endpoints.py."""
import pytest
from fastapi.testclient import TestClient

from shared.database import UserModel


class TestUserEndpoints:
    """Tests for user API endpoints."""

    def test_list_users(self, client: TestClient, multiple_users):
        """Test listing all users."""
        response = client.get("/api/v1/users")

        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 5
        assert len(data["users"]) == 5

    def test_list_users_with_pagination(self, client: TestClient, multiple_users):
        """Test listing users with pagination."""
        response = client.get("/api/v1/users?skip=1&limit=2")

        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 5
        assert len(data["users"]) == 2

    def test_list_users_empty(self, client: TestClient):
        """Test listing users when no users exist."""
        response = client.get("/api/v1/users")

        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 0
        assert len(data["users"]) == 0

    def test_get_user(self, client: TestClient, sample_user: UserModel):
        """Test getting a specific user."""
        response = client.get(f"/api/v1/users/{sample_user.id}")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == sample_user.id
        assert data["email"] == sample_user.email
        assert data["username"] == sample_user.username
        assert data["full_name"] == sample_user.full_name

    def test_get_user_not_found(self, client: TestClient):
        """Test getting a user that doesn't exist."""
        response = client.get("/api/v1/users/999999")

        assert response.status_code == 404
        assert "not found" in response.json()["detail"]

    def test_create_user(self, client: TestClient):
        """Test creating a new user."""
        user_data = {
            "email": "new@example.com",
            "username": "newuser",
            "full_name": "New User"
        }

        response = client.post("/api/v1/users", json=user_data)

        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "new@example.com"
        assert data["username"] == "newuser"
        assert data["full_name"] == "New User"
        assert "id" in data
        assert "created_at" in data
        assert "updated_at" in data

    def test_create_user_duplicate_email(self, client: TestClient, sample_user: UserModel):
        """Test creating a user with duplicate email."""
        user_data = {
            "email": sample_user.email,
            "username": "differentuser",
            "full_name": "Different User"
        }

        response = client.post("/api/v1/users", json=user_data)

        assert response.status_code == 400
        assert "Email already registered" in response.json()["detail"]

    def test_create_user_duplicate_username(self, client: TestClient, sample_user: UserModel):
        """Test creating a user with duplicate username."""
        user_data = {
            "email": "different@example.com",
            "username": sample_user.username,
            "full_name": "Different User"
        }

        response = client.post("/api/v1/users", json=user_data)

        assert response.status_code == 400
        assert "Username already taken" in response.json()["detail"]

    def test_create_user_invalid_email(self, client: TestClient):
        """Test creating a user with invalid email."""
        user_data = {
            "email": "invalid-email",
            "username": "newuser",
            "full_name": "New User"
        }

        response = client.post("/api/v1/users", json=user_data)

        assert response.status_code == 422  # Validation error

    def test_create_user_short_username(self, client: TestClient):
        """Test creating a user with username too short."""
        user_data = {
            "email": "new@example.com",
            "username": "ab",  # Less than 3 characters
            "full_name": "New User"
        }

        response = client.post("/api/v1/users", json=user_data)

        assert response.status_code == 422  # Validation error

    def test_create_user_missing_fields(self, client: TestClient):
        """Test creating a user with missing required fields."""
        user_data = {
            "email": "new@example.com"
            # Missing username and full_name
        }

        response = client.post("/api/v1/users", json=user_data)

        assert response.status_code == 422  # Validation error

    def test_update_user(self, client: TestClient, sample_user: UserModel):
        """Test updating a user."""
        update_data = {
            "full_name": "Updated Name"
        }

        response = client.put(f"/api/v1/users/{sample_user.id}", json=update_data)

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == sample_user.id
        assert data["full_name"] == "Updated Name"
        assert data["email"] == sample_user.email

    def test_update_user_all_fields(self, client: TestClient, sample_user: UserModel):
        """Test updating all fields of a user."""
        update_data = {
            "email": "updated@example.com",
            "username": "updateduser",
            "full_name": "Updated Name"
        }

        response = client.put(f"/api/v1/users/{sample_user.id}", json=update_data)

        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "updated@example.com"
        assert data["username"] == "updateduser"
        assert data["full_name"] == "Updated Name"

    def test_update_user_not_found(self, client: TestClient):
        """Test updating a user that doesn't exist."""
        update_data = {
            "full_name": "Updated Name"
        }

        response = client.put("/api/v1/users/999999", json=update_data)

        assert response.status_code == 404
        assert "not found" in response.json()["detail"]

    def test_update_user_duplicate_email(self, client: TestClient, multiple_users):
        """Test updating a user with an email that already exists."""
        user1 = multiple_users[0]
        user2 = multiple_users[1]

        update_data = {
            "email": user2.email
        }

        response = client.put(f"/api/v1/users/{user1.id}", json=update_data)

        assert response.status_code == 400
        assert "Email already registered" in response.json()["detail"]

    def test_update_user_duplicate_username(self, client: TestClient, multiple_users):
        """Test updating a user with a username that already exists."""
        user1 = multiple_users[0]
        user2 = multiple_users[1]

        update_data = {
            "username": user2.username
        }

        response = client.put(f"/api/v1/users/{user1.id}", json=update_data)

        assert response.status_code == 400
        assert "Username already taken" in response.json()["detail"]

    def test_delete_user(self, client: TestClient, sample_user: UserModel):
        """Test deleting a user."""
        response = client.delete(f"/api/v1/users/{sample_user.id}")

        assert response.status_code == 204

        # Verify user is deleted
        get_response = client.get(f"/api/v1/users/{sample_user.id}")
        assert get_response.status_code == 404

    def test_delete_user_not_found(self, client: TestClient):
        """Test deleting a user that doesn't exist."""
        response = client.delete("/api/v1/users/999999")

        assert response.status_code == 404
        assert "not found" in response.json()["detail"]
