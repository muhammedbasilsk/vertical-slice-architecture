"""User API endpoints."""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from shared.database import get_db
from features.users.models import UserCreate, UserUpdate, UserResponse, UserListResponse
from features.users.repository import UserRepository
from features.users.service import UserService

router = APIRouter(prefix="/users", tags=["Users"])


def get_user_service(db: Session = Depends(get_db)) -> UserService:
    """Dependency to get user service."""
    repository = UserRepository(db)
    return UserService(repository)


@router.get(
    "",
    response_model=UserListResponse,
    status_code=status.HTTP_200_OK,
    summary="List all users",
    description="Retrieve a list of all users with pagination support"
)
def list_users(
    skip: int = 0,
    limit: int = 100,
    service: UserService = Depends(get_user_service)
) -> UserListResponse:
    """
    List all users with pagination.

    - **skip**: Number of records to skip (default: 0)
    - **limit**: Maximum number of records to return (default: 100)
    """
    return service.get_users(skip=skip, limit=limit)


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Get a user",
    description="Retrieve a specific user by their ID"
)
def get_user(
    user_id: int,
    service: UserService = Depends(get_user_service)
) -> UserResponse:
    """
    Get a user by ID.

    - **user_id**: The ID of the user to retrieve
    """
    return service.get_user(user_id)


@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a user",
    description="Create a new user with the provided information"
)
def create_user(
    user_data: UserCreate,
    service: UserService = Depends(get_user_service)
) -> UserResponse:
    """
    Create a new user.

    - **email**: User's email address (must be unique)
    - **username**: User's username (must be unique)
    - **full_name**: User's full name
    """
    return service.create_user(user_data)


@router.put(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Update a user",
    description="Update an existing user's information"
)
def update_user(
    user_id: int,
    user_data: UserUpdate,
    service: UserService = Depends(get_user_service)
) -> UserResponse:
    """
    Update an existing user.

    - **user_id**: The ID of the user to update
    - **email**: User's email address (optional)
    - **username**: User's username (optional)
    - **full_name**: User's full name (optional)
    """
    return service.update_user(user_id, user_data)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a user",
    description="Delete a user by their ID"
)
def delete_user(
    user_id: int,
    service: UserService = Depends(get_user_service)
) -> None:
    """
    Delete a user.

    - **user_id**: The ID of the user to delete
    """
    service.delete_user(user_id)
