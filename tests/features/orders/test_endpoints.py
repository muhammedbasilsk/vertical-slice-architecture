"""Tests for features/orders/endpoints.py."""
import pytest
from fastapi.testclient import TestClient

from shared.database import OrderModel, UserModel


class TestOrderEndpoints:
    """Tests for order API endpoints."""

    def test_list_orders(self, client: TestClient, multiple_orders):
        """Test listing all orders."""
        response = client.get("/api/v1/orders")

        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 5
        assert len(data["orders"]) == 5

    def test_list_orders_with_pagination(self, client: TestClient, multiple_orders):
        """Test listing orders with pagination."""
        response = client.get("/api/v1/orders?skip=1&limit=2")

        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 5
        assert len(data["orders"]) == 2

    def test_list_orders_empty(self, client: TestClient):
        """Test listing orders when no orders exist."""
        response = client.get("/api/v1/orders")

        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 0
        assert len(data["orders"]) == 0

    def test_get_order(self, client: TestClient, sample_order: OrderModel):
        """Test getting a specific order."""
        response = client.get(f"/api/v1/orders/{sample_order.id}")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == sample_order.id
        assert data["user_id"] == sample_order.user_id
        assert data["product_name"] == sample_order.product_name
        assert data["quantity"] == sample_order.quantity
        assert data["total_price"] == sample_order.total_price
        assert data["status"] == sample_order.status

    def test_get_order_not_found(self, client: TestClient):
        """Test getting an order that doesn't exist."""
        response = client.get("/api/v1/orders/999999")

        assert response.status_code == 404
        assert "not found" in response.json()["detail"]

    def test_create_order(self, client: TestClient, sample_user: UserModel):
        """Test creating a new order."""
        order_data = {
            "user_id": sample_user.id,
            "product_name": "New Product",
            "quantity": 3,
            "total_price": 149.99,
            "status": "pending"
        }

        response = client.post("/api/v1/orders", json=order_data)

        assert response.status_code == 201
        data = response.json()
        assert data["user_id"] == sample_user.id
        assert data["product_name"] == "New Product"
        assert data["quantity"] == 3
        assert data["total_price"] == 149.99
        assert data["status"] == "pending"
        assert "id" in data
        assert "created_at" in data
        assert "updated_at" in data

    def test_create_order_user_not_found(self, client: TestClient):
        """Test creating an order for non-existent user."""
        order_data = {
            "user_id": 999999,
            "product_name": "Product",
            "quantity": 1,
            "total_price": 10.0,
            "status": "pending"
        }

        response = client.post("/api/v1/orders", json=order_data)

        assert response.status_code == 404
        assert "User" in response.json()["detail"]

    def test_create_order_invalid_status(self, client: TestClient, sample_user: UserModel):
        """Test creating an order with invalid status."""
        order_data = {
            "user_id": sample_user.id,
            "product_name": "Product",
            "quantity": 1,
            "total_price": 10.0,
            "status": "invalid_status"
        }

        response = client.post("/api/v1/orders", json=order_data)

        assert response.status_code == 400
        assert "Invalid status" in response.json()["detail"]

    def test_create_order_negative_quantity(self, client: TestClient, sample_user: UserModel):
        """Test creating an order with negative quantity."""
        order_data = {
            "user_id": sample_user.id,
            "product_name": "Product",
            "quantity": -1,
            "total_price": 10.0,
            "status": "pending"
        }

        response = client.post("/api/v1/orders", json=order_data)

        assert response.status_code == 422  # Validation error

    def test_create_order_negative_price(self, client: TestClient, sample_user: UserModel):
        """Test creating an order with negative price."""
        order_data = {
            "user_id": sample_user.id,
            "product_name": "Product",
            "quantity": 1,
            "total_price": -10.0,
            "status": "pending"
        }

        response = client.post("/api/v1/orders", json=order_data)

        assert response.status_code == 422  # Validation error

    def test_create_order_zero_user_id(self, client: TestClient):
        """Test creating an order with zero user_id."""
        order_data = {
            "user_id": 0,
            "product_name": "Product",
            "quantity": 1,
            "total_price": 10.0,
            "status": "pending"
        }

        response = client.post("/api/v1/orders", json=order_data)

        assert response.status_code == 422  # Validation error

    def test_create_order_missing_fields(self, client: TestClient):
        """Test creating an order with missing required fields."""
        order_data = {
            "user_id": 1
            # Missing product_name, quantity, total_price
        }

        response = client.post("/api/v1/orders", json=order_data)

        assert response.status_code == 422  # Validation error

    def test_create_order_default_status(self, client: TestClient, sample_user: UserModel):
        """Test creating an order with default status."""
        order_data = {
            "user_id": sample_user.id,
            "product_name": "Product",
            "quantity": 1,
            "total_price": 10.0
            # No status specified, should default to "pending"
        }

        response = client.post("/api/v1/orders", json=order_data)

        assert response.status_code == 201
        data = response.json()
        assert data["status"] == "pending"

    def test_update_order(self, client: TestClient, sample_order: OrderModel):
        """Test updating an order."""
        update_data = {
            "status": "completed",
            "quantity": 10
        }

        response = client.put(f"/api/v1/orders/{sample_order.id}", json=update_data)

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == sample_order.id
        assert data["status"] == "completed"
        assert data["quantity"] == 10

    def test_update_order_all_fields(self, client: TestClient, sample_order: OrderModel):
        """Test updating all fields of an order."""
        update_data = {
            "product_name": "Updated Product",
            "quantity": 5,
            "total_price": 250.0,
            "status": "processing"
        }

        response = client.put(f"/api/v1/orders/{sample_order.id}", json=update_data)

        assert response.status_code == 200
        data = response.json()
        assert data["product_name"] == "Updated Product"
        assert data["quantity"] == 5
        assert data["total_price"] == 250.0
        assert data["status"] == "processing"

    def test_update_order_not_found(self, client: TestClient):
        """Test updating an order that doesn't exist."""
        update_data = {
            "status": "completed"
        }

        response = client.put("/api/v1/orders/999999", json=update_data)

        assert response.status_code == 404
        assert "not found" in response.json()["detail"]

    def test_update_order_invalid_status(self, client: TestClient, sample_order: OrderModel):
        """Test updating an order with invalid status."""
        update_data = {
            "status": "invalid_status"
        }

        response = client.put(f"/api/v1/orders/{sample_order.id}", json=update_data)

        assert response.status_code == 400
        assert "Invalid status" in response.json()["detail"]

    def test_delete_order(self, client: TestClient, sample_order: OrderModel):
        """Test deleting an order."""
        response = client.delete(f"/api/v1/orders/{sample_order.id}")

        assert response.status_code == 204

        # Verify order is deleted
        get_response = client.get(f"/api/v1/orders/{sample_order.id}")
        assert get_response.status_code == 404

    def test_delete_order_not_found(self, client: TestClient):
        """Test deleting an order that doesn't exist."""
        response = client.delete("/api/v1/orders/999999")

        assert response.status_code == 404
        assert "not found" in response.json()["detail"]
