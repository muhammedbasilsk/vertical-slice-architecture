"""Tests for main.py."""
import pytest
from fastapi.testclient import TestClient


class TestMainApplication:
    """Tests for main FastAPI application."""

    def test_app_creation(self):
        """Test that the FastAPI app is created correctly."""
        from main import app

        assert app is not None
        assert app.title == "Vertical Slice Architecture API"
        assert app.version == "1.0.0"

    def test_root_endpoint(self, client: TestClient):
        """Test the root endpoint."""
        response = client.get("/")

        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "Welcome to Vertical Slice Architecture API" in data["message"]
        assert data["docs"] == "/api/docs"
        assert data["version"] == "1.0.0"

    def test_health_check_endpoint(self, client: TestClient):
        """Test the health check endpoint."""
        response = client.get("/health")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["database"] == "connected"

    def test_docs_endpoint(self, client: TestClient):
        """Test that the API docs are accessible."""
        response = client.get("/api/docs")

        assert response.status_code == 200

    def test_openapi_endpoint(self, client: TestClient):
        """Test that the OpenAPI schema is accessible."""
        response = client.get("/api/openapi.json")

        assert response.status_code == 200
        data = response.json()
        assert "openapi" in data
        assert "info" in data
        assert data["info"]["title"] == "Vertical Slice Architecture API"

    def test_users_router_registered(self, client: TestClient):
        """Test that the users router is registered."""
        response = client.get("/api/v1/users")

        # Should return 200 (even if empty list)
        assert response.status_code == 200

    def test_orders_router_registered(self, client: TestClient):
        """Test that the orders router is registered."""
        response = client.get("/api/v1/orders")

        # Should return 200 (even if empty list)
        assert response.status_code == 200

    def test_cors_middleware(self, client: TestClient):
        """Test that CORS middleware is configured."""
        response = client.options(
            "/",
            headers={
                "Origin": "http://example.com",
                "Access-Control-Request-Method": "GET"
            }
        )

        # CORS headers should be present
        assert "access-control-allow-origin" in response.headers

    def test_404_for_non_existent_endpoint(self, client: TestClient):
        """Test that non-existent endpoints return 404."""
        response = client.get("/non-existent-endpoint")

        assert response.status_code == 404
