"""Tests for features/orders/service.py."""
import pytest
from fastapi import HTTPException
from sqlalchemy.orm import Session

from features.orders.models import OrderCreate, OrderUpdate
from features.orders.repository import OrderRepository
from features.orders.service import OrderService
from features.users.repository import UserRepository
from shared.database import OrderModel, UserModel


class TestOrderService:
    """Tests for OrderService."""

    def test_get_order_found(self, test_db_session: Session, sample_order: OrderModel):
        """Test getting an order that exists."""
        order_repository = OrderRepository(test_db_session)
        user_repository = UserRepository(test_db_session)
        service = OrderService(order_repository, user_repository)

        order = service.get_order(sample_order.id)

        assert order.id == sample_order.id
        assert order.product_name == sample_order.product_name
        assert order.user_id == sample_order.user_id

    def test_get_order_not_found(self, test_db_session: Session):
        """Test getting an order that doesn't exist."""
        order_repository = OrderRepository(test_db_session)
        user_repository = UserRepository(test_db_session)
        service = OrderService(order_repository, user_repository)

        with pytest.raises(HTTPException) as exc_info:
            service.get_order(999999)

        assert exc_info.value.status_code == 404
        assert "not found" in str(exc_info.value.detail)

    def test_get_orders(self, test_db_session: Session, multiple_orders):
        """Test getting all orders."""
        order_repository = OrderRepository(test_db_session)
        user_repository = UserRepository(test_db_session)
        service = OrderService(order_repository, user_repository)

        result = service.get_orders()

        assert result.total == 5
        assert len(result.orders) == 5
        assert all(order.product_name for order in result.orders)

    def test_get_orders_with_pagination(self, test_db_session: Session, multiple_orders):
        """Test getting orders with pagination."""
        order_repository = OrderRepository(test_db_session)
        user_repository = UserRepository(test_db_session)
        service = OrderService(order_repository, user_repository)

        result = service.get_orders(skip=1, limit=2)

        assert result.total == 5
        assert len(result.orders) == 2

    def test_get_orders_empty(self, test_db_session: Session):
        """Test getting orders when no orders exist."""
        order_repository = OrderRepository(test_db_session)
        user_repository = UserRepository(test_db_session)
        service = OrderService(order_repository, user_repository)

        result = service.get_orders()

        assert result.total == 0
        assert len(result.orders) == 0

    def test_create_order_success(self, test_db_session: Session, sample_user: UserModel):
        """Test creating an order successfully."""
        order_repository = OrderRepository(test_db_session)
        user_repository = UserRepository(test_db_session)
        service = OrderService(order_repository, user_repository)

        order_data = OrderCreate(
            user_id=sample_user.id,
            product_name="Test Product",
            quantity=2,
            total_price=99.99,
            status="pending"
        )

        order = service.create_order(order_data)

        assert order.id is not None
        assert order.user_id == sample_user.id
        assert order.product_name == "Test Product"
        assert order.quantity == 2
        assert order.total_price == 99.99
        assert order.status == "pending"

    def test_create_order_user_not_found(self, test_db_session: Session):
        """Test creating an order for non-existent user."""
        order_repository = OrderRepository(test_db_session)
        user_repository = UserRepository(test_db_session)
        service = OrderService(order_repository, user_repository)

        order_data = OrderCreate(
            user_id=999999,
            product_name="Test Product",
            quantity=2,
            total_price=99.99,
            status="pending"
        )

        with pytest.raises(HTTPException) as exc_info:
            service.create_order(order_data)

        assert exc_info.value.status_code == 404
        assert "User" in str(exc_info.value.detail)
        assert "not found" in str(exc_info.value.detail)

    def test_create_order_invalid_status(self, test_db_session: Session, sample_user: UserModel):
        """Test creating an order with invalid status."""
        order_repository = OrderRepository(test_db_session)
        user_repository = UserRepository(test_db_session)
        service = OrderService(order_repository, user_repository)

        order_data = OrderCreate(
            user_id=sample_user.id,
            product_name="Test Product",
            quantity=2,
            total_price=99.99,
            status="invalid_status"
        )

        with pytest.raises(HTTPException) as exc_info:
            service.create_order(order_data)

        assert exc_info.value.status_code == 400
        assert "Invalid status" in str(exc_info.value.detail)

    def test_create_order_valid_statuses(self, test_db_session: Session, sample_user: UserModel):
        """Test creating orders with all valid statuses."""
        order_repository = OrderRepository(test_db_session)
        user_repository = UserRepository(test_db_session)
        service = OrderService(order_repository, user_repository)

        valid_statuses = ["pending", "processing", "completed", "cancelled"]

        for status in valid_statuses:
            order_data = OrderCreate(
                user_id=sample_user.id,
                product_name=f"Product {status}",
                quantity=1,
                total_price=10.0,
                status=status
            )

            order = service.create_order(order_data)
            assert order.status == status

    def test_update_order_success(self, test_db_session: Session, sample_order: OrderModel):
        """Test updating an order successfully."""
        order_repository = OrderRepository(test_db_session)
        user_repository = UserRepository(test_db_session)
        service = OrderService(order_repository, user_repository)

        update_data = OrderUpdate(
            status="completed",
            quantity=5
        )

        updated_order = service.update_order(sample_order.id, update_data)

        assert updated_order.id == sample_order.id
        assert updated_order.status == "completed"
        assert updated_order.quantity == 5

    def test_update_order_not_found(self, test_db_session: Session):
        """Test updating an order that doesn't exist."""
        order_repository = OrderRepository(test_db_session)
        user_repository = UserRepository(test_db_session)
        service = OrderService(order_repository, user_repository)

        update_data = OrderUpdate(status="completed")

        with pytest.raises(HTTPException) as exc_info:
            service.update_order(999999, update_data)

        assert exc_info.value.status_code == 404
        assert "not found" in str(exc_info.value.detail)

    def test_update_order_invalid_status(self, test_db_session: Session, sample_order: OrderModel):
        """Test updating an order with invalid status."""
        order_repository = OrderRepository(test_db_session)
        user_repository = UserRepository(test_db_session)
        service = OrderService(order_repository, user_repository)

        update_data = OrderUpdate(status="invalid_status")

        with pytest.raises(HTTPException) as exc_info:
            service.update_order(sample_order.id, update_data)

        assert exc_info.value.status_code == 400
        assert "Invalid status" in str(exc_info.value.detail)

    def test_update_order_valid_statuses(self, test_db_session: Session, sample_order: OrderModel):
        """Test updating order with all valid statuses."""
        order_repository = OrderRepository(test_db_session)
        user_repository = UserRepository(test_db_session)
        service = OrderService(order_repository, user_repository)

        valid_statuses = ["pending", "processing", "completed", "cancelled"]

        for status in valid_statuses:
            update_data = OrderUpdate(status=status)
            updated_order = service.update_order(sample_order.id, update_data)
            assert updated_order.status == status

    def test_delete_order_success(self, test_db_session: Session, sample_order: OrderModel):
        """Test deleting an order successfully."""
        order_repository = OrderRepository(test_db_session)
        user_repository = UserRepository(test_db_session)
        service = OrderService(order_repository, user_repository)
        order_id = sample_order.id

        service.delete_order(order_id)

        # Verify order is deleted
        with pytest.raises(HTTPException):
            service.get_order(order_id)

    def test_delete_order_not_found(self, test_db_session: Session):
        """Test deleting an order that doesn't exist."""
        order_repository = OrderRepository(test_db_session)
        user_repository = UserRepository(test_db_session)
        service = OrderService(order_repository, user_repository)

        with pytest.raises(HTTPException) as exc_info:
            service.delete_order(999999)

        assert exc_info.value.status_code == 404
        assert "not found" in str(exc_info.value.detail)
