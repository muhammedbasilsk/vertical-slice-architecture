"""User V2 Pydantic schemas for request/response validation."""
from datetime import datetime
from typing import Optional
from enum import Enum

from pydantic import BaseModel, Field


class UserRole(str, Enum):
    """User role enum."""

    USER = "user"
    ADMIN = "admin"
    MODERATOR = "moderator"


class UserBase(BaseModel):
    """Base user schema for V2."""

    username: str = Field(..., min_length=3, max_length=50, description="Unique username")
    name: str = Field(..., min_length=1, max_length=100, description="User name")


class UserCreate(UserBase):
    """Schema for creating a user in V2."""

    role: UserRole = Field(default=UserRole.USER, description="User role")


class UserUpdate(BaseModel):
    """Schema for updating a user in V2."""

    username: Optional[str] = Field(None, min_length=3, max_length=50, description="Unique username")
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="User name")
    role: Optional[UserRole] = Field(None, description="User role")


class UserResponse(UserBase):
    """Schema for user response in V2."""

    id: int = Field(..., description="User ID")
    role: UserRole = Field(..., description="User role")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    class Config:
        from_attributes = True


class UserListResponse(BaseModel):
    """Schema for user list response in V2."""

    users: list[UserResponse] = Field(..., description="List of users")
    total: int = Field(..., description="Total number of users")
