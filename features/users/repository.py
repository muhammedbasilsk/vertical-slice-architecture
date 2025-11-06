"""User data access layer."""
from typing import Optional

from sqlalchemy.orm import Session

from shared.database import UserModel


class UserRepository:
    """Repository for user data access."""

    def __init__(self, db: Session):
        """Initialize repository with database session."""
        self.db = db

    def get_by_id(self, user_id: int) -> Optional[UserModel]:
        """Get user by ID."""
        return self.db.query(UserModel).filter(UserModel.id == user_id).first()

    def get_by_email(self, email: str) -> Optional[UserModel]:
        """Get user by email."""
        return self.db.query(UserModel).filter(UserModel.email == email).first()

    def get_by_username(self, username: str) -> Optional[UserModel]:
        """Get user by username."""
        return self.db.query(UserModel).filter(UserModel.username == username).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> list[UserModel]:
        """Get all users with pagination."""
        return self.db.query(UserModel).offset(skip).limit(limit).all()

    def count(self) -> int:
        """Count total users."""
        return self.db.query(UserModel).count()

    def create(self, user_data: dict) -> UserModel:
        """Create a new user."""
        user = UserModel(**user_data)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update(self, user: UserModel, user_data: dict) -> UserModel:
        """Update an existing user."""
        for key, value in user_data.items():
            if value is not None:
                setattr(user, key, value)
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete(self, user: UserModel) -> None:
        """Delete a user."""
        self.db.delete(user)
        self.db.commit()
