"""Pytest configuration and fixtures."""
import os
import sys
from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

# Add the project root to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from shared.database import Base, get_db, UserModel, OrderModel
from main import app


# Test database URL (in-memory SQLite)
TEST_DATABASE_URL = "sqlite:///:memory:"


@pytest.fixture(scope="function")
def test_engine():
    """Create a test database engine with StaticPool for in-memory SQLite."""
    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool  # Use StaticPool to maintain a single connection
    )
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)
    engine.dispose()


@pytest.fixture(scope="function")
def test_db_session(test_engine) -> Generator[Session, None, None]:
    """Create a test database session."""
    TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    session = TestSessionLocal()
    try:
        yield session
    finally:
        session.rollback()
        session.close()


@pytest.fixture(scope="function")
def client(test_engine) -> Generator[TestClient, None, None]:
    """Create a test client with database session override."""
    TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

    def override_get_db():
        session = TestSessionLocal()
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def sample_user_data():
    """Sample user data for testing."""
    return {
        "email": "test@example.com",
        "username": "testuser",
        "full_name": "Test User"
    }


@pytest.fixture
def sample_user(test_db_session: Session, sample_user_data) -> UserModel:
    """Create a sample user in the database."""
    user = UserModel(**sample_user_data)
    test_db_session.add(user)
    test_db_session.commit()
    test_db_session.refresh(user)
    return user


@pytest.fixture
def sample_order_data(sample_user):
    """Sample order data for testing."""
    return {
        "user_id": sample_user.id,
        "product_name": "Test Product",
        "quantity": 2,
        "total_price": 99.99,
        "status": "pending"
    }


@pytest.fixture
def sample_order(test_db_session: Session, sample_user, sample_order_data) -> OrderModel:
    """Create a sample order in the database."""
    order = OrderModel(**sample_order_data)
    test_db_session.add(order)
    test_db_session.commit()
    test_db_session.refresh(order)
    return order


@pytest.fixture
def multiple_users(test_db_session: Session):
    """Create multiple users for testing pagination."""
    users = []
    for i in range(5):
        user = UserModel(
            email=f"user{i}@example.com",
            username=f"user{i}",
            full_name=f"User {i}"
        )
        test_db_session.add(user)
        users.append(user)
    test_db_session.commit()
    for user in users:
        test_db_session.refresh(user)
    return users


@pytest.fixture
def multiple_orders(test_db_session: Session, sample_user):
    """Create multiple orders for testing pagination."""
    orders = []
    for i in range(5):
        order = OrderModel(
            user_id=sample_user.id,
            product_name=f"Product {i}",
            quantity=i + 1,
            total_price=(i + 1) * 10.0,
            status="pending"
        )
        test_db_session.add(order)
        orders.append(order)
    test_db_session.commit()
    for order in orders:
        test_db_session.refresh(order)
    return orders
