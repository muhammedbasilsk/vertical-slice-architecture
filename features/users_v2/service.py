"""User V2 business logic layer."""
from fastapi import HTTPException, status

from features.users_v2.models import UserCreate, UserUpdate, UserResponse, UserListResponse
from features.users_v2.repository import UserRepositoryV2


class UserServiceV2:
    """Service for user V2 business logic."""

    def __init__(self, repository: UserRepositoryV2):
        """Initialize service with repository."""
        self.repository = repository

    def get_user(self, user_id: int) -> UserResponse:
        """Get a user by ID."""
        user = self.repository.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {user_id} not found"
            )
        return UserResponse.model_validate(user)

    def get_users(self, skip: int = 0, limit: int = 100) -> UserListResponse:
        """Get all users with pagination."""
        users = self.repository.get_all(skip=skip, limit=limit)
        total = self.repository.count()
        return UserListResponse(
            users=[UserResponse.model_validate(user) for user in users],
            total=total
        )

    def create_user(self, user_data: UserCreate) -> UserResponse:
        """Create a new user."""
        # Check if username already exists
        if self.repository.get_by_username(user_data.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )

        user = self.repository.create(user_data.model_dump())
        return UserResponse.model_validate(user)

    def update_user(self, user_id: int, user_data: UserUpdate) -> UserResponse:
        """Update an existing user."""
        user = self.repository.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {user_id} not found"
            )

        # Check if username is being updated and if it's already taken
        if user_data.username and user_data.username != user.username:
            existing_user = self.repository.get_by_username(user_data.username)
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Username already taken"
                )

        updated_user = self.repository.update(user, user_data.model_dump(exclude_unset=True))
        return UserResponse.model_validate(updated_user)

    def delete_user(self, user_id: int) -> None:
        """Delete a user."""
        user = self.repository.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {user_id} not found"
            )
        self.repository.delete(user)
