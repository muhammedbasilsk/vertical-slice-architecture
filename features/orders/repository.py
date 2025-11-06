"""Order data access layer."""
from typing import Optional

from sqlalchemy.orm import Session

from shared.database import OrderModel


class OrderRepository:
    """Repository for order data access."""

    def __init__(self, db: Session):
        """Initialize repository with database session."""
        self.db = db

    def get_by_id(self, order_id: int) -> Optional[OrderModel]:
        """Get order by ID."""
        return self.db.query(OrderModel).filter(OrderModel.id == order_id).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> list[OrderModel]:
        """Get all orders with pagination."""
        return self.db.query(OrderModel).offset(skip).limit(limit).all()

    def get_by_user_id(self, user_id: int, skip: int = 0, limit: int = 100) -> list[OrderModel]:
        """Get orders by user ID."""
        return self.db.query(OrderModel).filter(
            OrderModel.user_id == user_id
        ).offset(skip).limit(limit).all()

    def count(self) -> int:
        """Count total orders."""
        return self.db.query(OrderModel).count()

    def count_by_user(self, user_id: int) -> int:
        """Count orders by user."""
        return self.db.query(OrderModel).filter(OrderModel.user_id == user_id).count()

    def create(self, order_data: dict) -> OrderModel:
        """Create a new order."""
        order = OrderModel(**order_data)
        self.db.add(order)
        self.db.commit()
        self.db.refresh(order)
        return order

    def update(self, order: OrderModel, order_data: dict) -> OrderModel:
        """Update an existing order."""
        for key, value in order_data.items():
            if value is not None:
                setattr(order, key, value)
        self.db.commit()
        self.db.refresh(order)
        return order

    def delete(self, order: OrderModel) -> None:
        """Delete an order."""
        self.db.delete(order)
        self.db.commit()
