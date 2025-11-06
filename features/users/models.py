"""User Pydantic schemas for request/response validation."""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    """Base user schema."""

    email: EmailStr = Field(..., description="User email address")
    username: str = Field(..., min_length=3, max_length=50, description="Unique username")
    full_name: str = Field(..., min_length=1, max_length=100, description="User full name")


class UserCreate(UserBase):
    """Schema for creating a user."""

    pass


class UserUpdate(BaseModel):
    """Schema for updating a user."""

    email: Optional[EmailStr] = Field(None, description="User email address")
    username: Optional[str] = Field(None, min_length=3, max_length=50, description="Unique username")
    full_name: Optional[str] = Field(None, min_length=1, max_length=100, description="User full name")


class UserResponse(UserBase):
    """Schema for user response."""

    id: int = Field(..., description="User ID")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    class Config:
        from_attributes = True


class UserListResponse(BaseModel):
    """Schema for user list response."""

    users: list[UserResponse] = Field(..., description="List of users")
    total: int = Field(..., description="Total number of users")
