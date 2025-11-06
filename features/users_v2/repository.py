"""User V2 data access layer."""
from typing import Optional

from sqlalchemy.orm import Session

from shared.database import UserModelV2


class UserRepositoryV2:
    """Repository for user V2 data access."""

    def __init__(self, db: Session):
        """Initialize repository with database session."""
        self.db = db

    def get_by_id(self, user_id: int) -> Optional[UserModelV2]:
        """Get user by ID."""
        return self.db.query(UserModelV2).filter(UserModelV2.id == user_id).first()

    def get_by_username(self, username: str) -> Optional[UserModelV2]:
        """Get user by username."""
        return self.db.query(UserModelV2).filter(UserModelV2.username == username).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> list[UserModelV2]:
        """Get all users with pagination."""
        return self.db.query(UserModelV2).offset(skip).limit(limit).all()

    def count(self) -> int:
        """Count total users."""
        return self.db.query(UserModelV2).count()

    def create(self, user_data: dict) -> UserModelV2:
        """Create a new user."""
        user = UserModelV2(**user_data)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update(self, user: UserModelV2, user_data: dict) -> UserModelV2:
        """Update an existing user."""
        for key, value in user_data.items():
            if value is not None:
                setattr(user, key, value)
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete(self, user: UserModelV2) -> None:
        """Delete a user."""
        self.db.delete(user)
        self.db.commit()
