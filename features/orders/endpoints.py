"""Order API endpoints."""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from shared.database import get_db
from features.orders.models import OrderCreate, OrderUpdate, OrderResponse, OrderListResponse
from features.orders.repository import OrderRepository
from features.orders.service import OrderService
from features.users.repository import UserRepository

router = APIRouter(prefix="/orders", tags=["Orders"])


def get_order_service(db: Session = Depends(get_db)) -> OrderService:
    """Dependency to get order service."""
    order_repository = OrderRepository(db)
    user_repository = UserRepository(db)
    return OrderService(order_repository, user_repository)


@router.get(
    "",
    response_model=OrderListResponse,
    status_code=status.HTTP_200_OK,
    summary="List all orders",
    description="Retrieve a list of all orders with pagination support"
)
def list_orders(
    skip: int = 0,
    limit: int = 100,
    service: OrderService = Depends(get_order_service)
) -> OrderListResponse:
    """
    List all orders with pagination.

    - **skip**: Number of records to skip (default: 0)
    - **limit**: Maximum number of records to return (default: 100)
    """
    return service.get_orders(skip=skip, limit=limit)


@router.get(
    "/{order_id}",
    response_model=OrderResponse,
    status_code=status.HTTP_200_OK,
    summary="Get an order",
    description="Retrieve a specific order by its ID"
)
def get_order(
    order_id: int,
    service: OrderService = Depends(get_order_service)
) -> OrderResponse:
    """
    Get an order by ID.

    - **order_id**: The ID of the order to retrieve
    """
    return service.get_order(order_id)


@router.post(
    "",
    response_model=OrderResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create an order",
    description="Create a new order with the provided information"
)
def create_order(
    order_data: OrderCreate,
    service: OrderService = Depends(get_order_service)
) -> OrderResponse:
    """
    Create a new order.

    - **user_id**: ID of the user placing the order
    - **product_name**: Name of the product
    - **quantity**: Quantity of products
    - **total_price**: Total price of the order
    - **status**: Order status (default: pending)
    """
    return service.create_order(order_data)


@router.put(
    "/{order_id}",
    response_model=OrderResponse,
    status_code=status.HTTP_200_OK,
    summary="Update an order",
    description="Update an existing order's information"
)
def update_order(
    order_id: int,
    order_data: OrderUpdate,
    service: OrderService = Depends(get_order_service)
) -> OrderResponse:
    """
    Update an existing order.

    - **order_id**: The ID of the order to update
    - **product_name**: Name of the product (optional)
    - **quantity**: Quantity of products (optional)
    - **total_price**: Total price of the order (optional)
    - **status**: Order status (optional)
    """
    return service.update_order(order_id, order_data)


@router.delete(
    "/{order_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an order",
    description="Delete an order by its ID"
)
def delete_order(
    order_id: int,
    service: OrderService = Depends(get_order_service)
) -> None:
    """
    Delete an order.

    - **order_id**: The ID of the order to delete
    """
    service.delete_order(order_id)
