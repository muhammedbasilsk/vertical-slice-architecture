"""Tests for features/orders/models.py."""
import pytest
from datetime import datetime
from pydantic import ValidationError

from features.orders.models import OrderBase, OrderCreate, OrderUpdate, OrderResponse, OrderListResponse


class TestOrderBase:
    """Tests for OrderBase model."""

    def test_valid_order_base(self):
        """Test creating a valid OrderBase."""
        order = OrderBase(
            user_id=1,
            product_name="Test Product",
            quantity=2,
            total_price=99.99,
            status="pending"
        )

        assert order.user_id == 1
        assert order.product_name == "Test Product"
        assert order.quantity == 2
        assert order.total_price == 99.99
        assert order.status == "pending"

    def test_order_base_default_status(self):
        """Test OrderBase with default status."""
        order = OrderBase(
            user_id=1,
            product_name="Test Product",
            quantity=2,
            total_price=99.99
        )

        assert order.status == "pending"

    def test_invalid_user_id_zero(self):
        """Test OrderBase with user_id of zero."""
        with pytest.raises(ValidationError) as exc_info:
            OrderBase(
                user_id=0,
                product_name="Test Product",
                quantity=2,
                total_price=99.99
            )

        errors = exc_info.value.errors()
        assert any("user_id" in str(error["loc"]) for error in errors)

    def test_invalid_user_id_negative(self):
        """Test OrderBase with negative user_id."""
        with pytest.raises(ValidationError) as exc_info:
            OrderBase(
                user_id=-1,
                product_name="Test Product",
                quantity=2,
                total_price=99.99
            )

        errors = exc_info.value.errors()
        assert any("user_id" in str(error["loc"]) for error in errors)

    def test_empty_product_name(self):
        """Test OrderBase with empty product name."""
        with pytest.raises(ValidationError) as exc_info:
            OrderBase(
                user_id=1,
                product_name="",
                quantity=2,
                total_price=99.99
            )

        errors = exc_info.value.errors()
        assert any("product_name" in str(error["loc"]) for error in errors)

    def test_long_product_name(self):
        """Test OrderBase with product name too long."""
        with pytest.raises(ValidationError) as exc_info:
            OrderBase(
                user_id=1,
                product_name="a" * 201,  # More than 200 characters
                quantity=2,
                total_price=99.99
            )

        errors = exc_info.value.errors()
        assert any("product_name" in str(error["loc"]) for error in errors)

    def test_zero_quantity(self):
        """Test OrderBase with zero quantity."""
        with pytest.raises(ValidationError) as exc_info:
            OrderBase(
                user_id=1,
                product_name="Test Product",
                quantity=0,
                total_price=99.99
            )

        errors = exc_info.value.errors()
        assert any("quantity" in str(error["loc"]) for error in errors)

    def test_negative_quantity(self):
        """Test OrderBase with negative quantity."""
        with pytest.raises(ValidationError) as exc_info:
            OrderBase(
                user_id=1,
                product_name="Test Product",
                quantity=-1,
                total_price=99.99
            )

        errors = exc_info.value.errors()
        assert any("quantity" in str(error["loc"]) for error in errors)

    def test_zero_price(self):
        """Test OrderBase with zero price."""
        with pytest.raises(ValidationError) as exc_info:
            OrderBase(
                user_id=1,
                product_name="Test Product",
                quantity=2,
                total_price=0.0
            )

        errors = exc_info.value.errors()
        assert any("total_price" in str(error["loc"]) for error in errors)

    def test_negative_price(self):
        """Test OrderBase with negative price."""
        with pytest.raises(ValidationError) as exc_info:
            OrderBase(
                user_id=1,
                product_name="Test Product",
                quantity=2,
                total_price=-99.99
            )

        errors = exc_info.value.errors()
        assert any("total_price" in str(error["loc"]) for error in errors)

    def test_missing_fields(self):
        """Test OrderBase with missing required fields."""
        with pytest.raises(ValidationError) as exc_info:
            OrderBase(user_id=1)

        errors = exc_info.value.errors()
        assert len(errors) >= 3  # Missing product_name, quantity, total_price


class TestOrderCreate:
    """Tests for OrderCreate model."""

    def test_valid_order_create(self):
        """Test creating a valid OrderCreate."""
        order = OrderCreate(
            user_id=1,
            product_name="Test Product",
            quantity=2,
            total_price=99.99,
            status="pending"
        )

        assert order.user_id == 1
        assert order.product_name == "Test Product"
        assert order.quantity == 2
        assert order.total_price == 99.99
        assert order.status == "pending"

    def test_inherits_from_order_base(self):
        """Test that OrderCreate inherits from OrderBase."""
        assert issubclass(OrderCreate, OrderBase)


class TestOrderUpdate:
    """Tests for OrderUpdate model."""

    def test_valid_order_update_all_fields(self):
        """Test creating an OrderUpdate with all fields."""
        order = OrderUpdate(
            product_name="Updated Product",
            quantity=5,
            total_price=250.0,
            status="completed"
        )

        assert order.product_name == "Updated Product"
        assert order.quantity == 5
        assert order.total_price == 250.0
        assert order.status == "completed"

    def test_order_update_partial_fields(self):
        """Test creating an OrderUpdate with partial fields."""
        order = OrderUpdate(status="completed")

        assert order.status == "completed"
        assert order.product_name is None
        assert order.quantity is None
        assert order.total_price is None

    def test_order_update_empty(self):
        """Test creating an empty OrderUpdate."""
        order = OrderUpdate()

        assert order.product_name is None
        assert order.quantity is None
        assert order.total_price is None
        assert order.status is None

    def test_order_update_validation_empty_product_name(self):
        """Test that OrderUpdate validates empty product name."""
        with pytest.raises(ValidationError):
            OrderUpdate(product_name="")

    def test_order_update_validation_zero_quantity(self):
        """Test that OrderUpdate validates zero quantity."""
        with pytest.raises(ValidationError):
            OrderUpdate(quantity=0)

    def test_order_update_validation_zero_price(self):
        """Test that OrderUpdate validates zero price."""
        with pytest.raises(ValidationError):
            OrderUpdate(total_price=0.0)


class TestOrderResponse:
    """Tests for OrderResponse model."""

    def test_valid_order_response(self):
        """Test creating a valid OrderResponse."""
        order = OrderResponse(
            id=1,
            user_id=1,
            product_name="Test Product",
            quantity=2,
            total_price=99.99,
            status="pending",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        assert order.id == 1
        assert order.user_id == 1
        assert order.product_name == "Test Product"
        assert order.quantity == 2
        assert order.total_price == 99.99
        assert order.status == "pending"
        assert isinstance(order.created_at, datetime)
        assert isinstance(order.updated_at, datetime)

    def test_inherits_from_order_base(self):
        """Test that OrderResponse inherits from OrderBase."""
        assert issubclass(OrderResponse, OrderBase)

    def test_missing_required_fields(self):
        """Test OrderResponse with missing required fields."""
        with pytest.raises(ValidationError) as exc_info:
            OrderResponse(
                user_id=1,
                product_name="Test Product",
                quantity=2,
                total_price=99.99,
                status="pending"
            )

        errors = exc_info.value.errors()
        # Should be missing id, created_at, updated_at
        assert len(errors) >= 3


class TestOrderListResponse:
    """Tests for OrderListResponse model."""

    def test_valid_order_list_response(self):
        """Test creating a valid OrderListResponse."""
        orders = [
            OrderResponse(
                id=1,
                user_id=1,
                product_name="Product 1",
                quantity=1,
                total_price=10.0,
                status="pending",
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            ),
            OrderResponse(
                id=2,
                user_id=1,
                product_name="Product 2",
                quantity=2,
                total_price=20.0,
                status="completed",
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
        ]

        response = OrderListResponse(orders=orders, total=2)

        assert len(response.orders) == 2
        assert response.total == 2
        assert all(isinstance(order, OrderResponse) for order in response.orders)

    def test_empty_order_list_response(self):
        """Test creating an empty OrderListResponse."""
        response = OrderListResponse(orders=[], total=0)

        assert len(response.orders) == 0
        assert response.total == 0

    def test_missing_required_fields(self):
        """Test OrderListResponse with missing required fields."""
        with pytest.raises(ValidationError):
            OrderListResponse(orders=[])  # Missing total
