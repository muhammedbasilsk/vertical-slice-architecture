"""Order Pydantic schemas for request/response validation."""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class OrderBase(BaseModel):
    """Base order schema."""

    user_id: int = Field(..., gt=0, description="ID of the user who placed the order")
    product_name: str = Field(..., min_length=1, max_length=200, description="Name of the product")
    quantity: int = Field(..., gt=0, description="Quantity of products ordered")
    total_price: float = Field(..., gt=0, description="Total price of the order")
    status: str = Field(default="pending", description="Order status (pending, processing, completed, cancelled)")


class OrderCreate(OrderBase):
    """Schema for creating an order."""

    pass


class OrderUpdate(BaseModel):
    """Schema for updating an order."""

    product_name: Optional[str] = Field(None, min_length=1, max_length=200, description="Name of the product")
    quantity: Optional[int] = Field(None, gt=0, description="Quantity of products ordered")
    total_price: Optional[float] = Field(None, gt=0, description="Total price of the order")
    status: Optional[str] = Field(None, description="Order status (pending, processing, completed, cancelled)")


class OrderResponse(OrderBase):
    """Schema for order response."""

    id: int = Field(..., description="Order ID")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    class Config:
        from_attributes = True


class OrderListResponse(BaseModel):
    """Schema for order list response."""

    orders: list[OrderResponse] = Field(..., description="List of orders")
    total: int = Field(..., description="Total number of orders")
