"""Order business logic layer."""
from fastapi import HTTPException, status

from features.orders.models import OrderCreate, OrderUpdate, OrderResponse, OrderListResponse
from features.orders.repository import OrderRepository
from features.users.repository import UserRepository


class OrderService:
    """Service for order business logic."""

    def __init__(self, order_repository: OrderRepository, user_repository: UserRepository):
        """Initialize service with repositories."""
        self.order_repository = order_repository
        self.user_repository = user_repository

    def get_order(self, order_id: int) -> OrderResponse:
        """Get an order by ID."""
        order = self.order_repository.get_by_id(order_id)
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Order with id {order_id} not found"
            )
        return OrderResponse.model_validate(order)

    def get_orders(self, skip: int = 0, limit: int = 100) -> OrderListResponse:
        """Get all orders with pagination."""
        orders = self.order_repository.get_all(skip=skip, limit=limit)
        total = self.order_repository.count()
        return OrderListResponse(
            orders=[OrderResponse.model_validate(order) for order in orders],
            total=total
        )

    def create_order(self, order_data: OrderCreate) -> OrderResponse:
        """Create a new order."""
        # Verify that the user exists
        user = self.user_repository.get_by_id(order_data.user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {order_data.user_id} not found"
            )

        # Validate status
        valid_statuses = ["pending", "processing", "completed", "cancelled"]
        if order_data.status not in valid_statuses:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
            )

        order = self.order_repository.create(order_data.model_dump())
        return OrderResponse.model_validate(order)

    def update_order(self, order_id: int, order_data: OrderUpdate) -> OrderResponse:
        """Update an existing order."""
        order = self.order_repository.get_by_id(order_id)
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Order with id {order_id} not found"
            )

        # Validate status if provided
        if order_data.status:
            valid_statuses = ["pending", "processing", "completed", "cancelled"]
            if order_data.status not in valid_statuses:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
                )

        updated_order = self.order_repository.update(order, order_data.model_dump(exclude_unset=True))
        return OrderResponse.model_validate(updated_order)

    def delete_order(self, order_id: int) -> None:
        """Delete an order."""
        order = self.order_repository.get_by_id(order_id)
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Order with id {order_id} not found"
            )
        self.order_repository.delete(order)
