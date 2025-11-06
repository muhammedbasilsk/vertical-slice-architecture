"""User V2 API endpoints."""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from shared.database import get_db
from features.users_v2.models import UserCreate, UserUpdate, UserResponse, UserListResponse
from features.users_v2.repository import UserRepositoryV2
from features.users_v2.service import UserServiceV2

router = APIRouter(prefix="/users", tags=["Users V2"])


def get_user_service(db: Session = Depends(get_db)) -> UserServiceV2:
    """Dependency to get user V2 service."""
    repository = UserRepositoryV2(db)
    return UserServiceV2(repository)


@router.get(
    "",
    response_model=UserListResponse,
    status_code=status.HTTP_200_OK,
    summary="List all users (V2)",
    description="Retrieve a list of all users with pagination support"
)
def list_users(
    skip: int = 0,
    limit: int = 100,
    service: UserServiceV2 = Depends(get_user_service)
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
    summary="Get a user (V2)",
    description="Retrieve a specific user by their ID"
)
def get_user(
    user_id: int,
    service: UserServiceV2 = Depends(get_user_service)
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
    summary="Create a user (V2)",
    description="Create a new user with the provided information"
)
def create_user(
    user_data: UserCreate,
    service: UserServiceV2 = Depends(get_user_service)
) -> UserResponse:
    """
    Create a new user.

    - **username**: User's username (must be unique)
    - **name**: User's name
    - **role**: User's role (default: user)
    """
    return service.create_user(user_data)


@router.patch(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Update a user (V2)",
    description="Partially update an existing user's information"
)
def update_user(
    user_id: int,
    user_data: UserUpdate,
    service: UserServiceV2 = Depends(get_user_service)
) -> UserResponse:
    """
    Update an existing user (partial update).

    - **user_id**: The ID of the user to update
    - **username**: User's username (optional)
    - **name**: User's name (optional)
    - **role**: User's role (optional)
    """
    return service.update_user(user_id, user_data)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a user (V2)",
    description="Delete a user by their ID"
)
def delete_user(
    user_id: int,
    service: UserServiceV2 = Depends(get_user_service)
) -> None:
    """
    Delete a user.

    - **user_id**: The ID of the user to delete
    """
    service.delete_user(user_id)
