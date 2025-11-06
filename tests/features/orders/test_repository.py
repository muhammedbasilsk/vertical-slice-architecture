"""Tests for features/orders/repository.py."""
import pytest
from sqlalchemy.orm import Session

from features.orders.repository import OrderRepository
from shared.database import OrderModel, UserModel


class TestOrderRepository:
    """Tests for OrderRepository."""

    def test_get_by_id_found(self, test_db_session: Session, sample_order: OrderModel):
        """Test getting order by ID when order exists."""
        repository = OrderRepository(test_db_session)
        order = repository.get_by_id(sample_order.id)

        assert order is not None
        assert order.id == sample_order.id
        assert order.product_name == sample_order.product_name

    def test_get_by_id_not_found(self, test_db_session: Session):
        """Test getting order by ID when order doesn't exist."""
        repository = OrderRepository(test_db_session)
        order = repository.get_by_id(999999)

        assert order is None

    def test_get_all(self, test_db_session: Session, multiple_orders):
        """Test getting all orders."""
        repository = OrderRepository(test_db_session)
        orders = repository.get_all()

        assert len(orders) == 5
        assert all(isinstance(order, OrderModel) for order in orders)

    def test_get_all_with_pagination(self, test_db_session: Session, multiple_orders):
        """Test getting all orders with pagination."""
        repository = OrderRepository(test_db_session)

        # Get first 2 orders
        orders_page1 = repository.get_all(skip=0, limit=2)
        assert len(orders_page1) == 2

        # Get next 2 orders
        orders_page2 = repository.get_all(skip=2, limit=2)
        assert len(orders_page2) == 2

        # Ensure different orders
        assert orders_page1[0].id != orders_page2[0].id

    def test_get_by_user_id(self, test_db_session: Session, sample_user: UserModel, multiple_orders):
        """Test getting orders by user ID."""
        repository = OrderRepository(test_db_session)
        orders = repository.get_by_user_id(sample_user.id)

        assert len(orders) == 5
        assert all(order.user_id == sample_user.id for order in orders)

    def test_get_by_user_id_with_pagination(self, test_db_session: Session, sample_user: UserModel, multiple_orders):
        """Test getting orders by user ID with pagination."""
        repository = OrderRepository(test_db_session)

        orders_page1 = repository.get_by_user_id(sample_user.id, skip=0, limit=2)
        assert len(orders_page1) == 2

        orders_page2 = repository.get_by_user_id(sample_user.id, skip=2, limit=2)
        assert len(orders_page2) == 2

    def test_get_by_user_id_not_found(self, test_db_session: Session):
        """Test getting orders for non-existent user."""
        repository = OrderRepository(test_db_session)
        orders = repository.get_by_user_id(999999)

        assert len(orders) == 0

    def test_count(self, test_db_session: Session, multiple_orders):
        """Test counting orders."""
        repository = OrderRepository(test_db_session)
        count = repository.count()

        assert count == 5

    def test_count_empty(self, test_db_session: Session):
        """Test counting orders when no orders exist."""
        repository = OrderRepository(test_db_session)
        count = repository.count()

        assert count == 0

    def test_count_by_user(self, test_db_session: Session, sample_user: UserModel, multiple_orders):
        """Test counting orders by user."""
        repository = OrderRepository(test_db_session)
        count = repository.count_by_user(sample_user.id)

        assert count == 5

    def test_count_by_user_empty(self, test_db_session: Session):
        """Test counting orders for user with no orders."""
        repository = OrderRepository(test_db_session)
        count = repository.count_by_user(999999)

        assert count == 0

    def test_create(self, test_db_session: Session, sample_user: UserModel):
        """Test creating an order."""
        repository = OrderRepository(test_db_session)
        order_data = {
            "user_id": sample_user.id,
            "product_name": "Test Product",
            "quantity": 2,
            "total_price": 99.99,
            "status": "pending"
        }

        order = repository.create(order_data)

        assert order.id is not None
        assert order.user_id == sample_user.id
        assert order.product_name == "Test Product"
        assert order.quantity == 2
        assert order.total_price == 99.99
        assert order.status == "pending"
        assert order.created_at is not None
        assert order.updated_at is not None

    def test_update(self, test_db_session: Session, sample_order: OrderModel):
        """Test updating an order."""
        repository = OrderRepository(test_db_session)
        update_data = {
            "status": "completed",
            "quantity": 5
        }

        updated_order = repository.update(sample_order, update_data)

        assert updated_order.id == sample_order.id
        assert updated_order.status == "completed"
        assert updated_order.quantity == 5
        assert updated_order.product_name == sample_order.product_name  # Unchanged

    def test_update_with_none_values(self, test_db_session: Session, sample_order: OrderModel):
        """Test updating an order with None values (should skip None values)."""
        repository = OrderRepository(test_db_session)
        original_status = sample_order.status

        update_data = {
            "quantity": 10,
            "status": None
        }

        updated_order = repository.update(sample_order, update_data)

        assert updated_order.quantity == 10
        assert updated_order.status == original_status  # Should remain unchanged

    def test_delete(self, test_db_session: Session, sample_order: OrderModel):
        """Test deleting an order."""
        repository = OrderRepository(test_db_session)
        order_id = sample_order.id

        repository.delete(sample_order)

        # Verify order is deleted
        deleted_order = repository.get_by_id(order_id)
        assert deleted_order is None
