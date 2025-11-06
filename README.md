# FastAPI Vertical Slice Architecture

A FastAPI application demonstrating **Vertical Slice Architecture** with RESTful CRUD operations for User and Order entities.

## Architecture Overview

### What is Vertical Slice Architecture?

Vertical Slice Architecture organizes code by **features** rather than technical layers. Each feature (or "slice") contains all the code needed for that feature, including:

- API endpoints (routes)
- Business logic (services)
- Data access (repositories)
- Data models (schemas)

### Benefits

- **Feature cohesion**: All code for a feature is in one place
- **Easy to understand**: Follow a feature from API to database in one directory
- **Maintainability**: Changes to a feature are isolated
- **Team scalability**: Different teams can work on different slices
- **Testability**: Each slice can be tested independently

### Project Structure

```
vertical-slice-architecture/
├── main.py                          # FastAPI application entry point
├── config.py                        # Application configuration
├── requirements.txt                 # Python dependencies
├── shared/                          # Shared utilities
│   ├── __init__.py
│   └── database.py                  # Database models and connection
├── features/                        # Vertical slices
│   ├── users/                       # User feature slice
│   │   ├── __init__.py
│   │   ├── models.py                # Pydantic schemas
│   │   ├── endpoints.py             # API routes
│   │   ├── service.py               # Business logic
│   │   └── repository.py            # Data access
│   └── orders/                      # Order feature slice
│       ├── __init__.py
│       ├── models.py                # Pydantic schemas
│       ├── endpoints.py             # API routes
│       ├── service.py               # Business logic
│       └── repository.py            # Data access
```

## Features

### Entities

1. **User**
   - id (auto-generated)
   - email (unique)
   - username (unique)
   - full_name
   - created_at
   - updated_at

2. **Order**
   - id (auto-generated)
   - user_id (foreign key to User)
   - product_name
   - quantity
   - total_price
   - status (pending, processing, completed, cancelled)
   - created_at
   - updated_at

### RESTful API Endpoints

#### Users

- `GET /api/v1/users` - List all users (with pagination)
- `GET /api/v1/users/{id}` - Get a specific user
- `POST /api/v1/users` - Create a new user
- `PUT /api/v1/users/{id}` - Update a user
- `DELETE /api/v1/users/{id}` - Delete a user

#### Orders

- `GET /api/v1/orders` - List all orders (with pagination)
- `GET /api/v1/orders/{id}` - Get a specific order
- `POST /api/v1/orders` - Create a new order
- `PUT /api/v1/orders/{id}` - Update an order
- `DELETE /api/v1/orders/{id}` - Delete an order

## Getting Started

### Prerequisites

- Python 3.10+
- pip

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd vertical-slice-architecture
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python main.py
```

Or using uvicorn directly:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

### API Documentation

Once the application is running, you can access:

- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc
- **OpenAPI Schema**: http://localhost:8000/api/openapi.json

## Usage Examples

### Using cURL

#### Create a User

```bash
curl -X POST "http://localhost:8000/api/v1/users" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john.doe@example.com",
    "username": "johndoe",
    "full_name": "John Doe"
  }'
```

#### Get All Users

```bash
curl -X GET "http://localhost:8000/api/v1/users"
```

#### Get a Specific User

```bash
curl -X GET "http://localhost:8000/api/v1/users/1"
```

#### Update a User

```bash
curl -X PUT "http://localhost:8000/api/v1/users/1" \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "John Smith"
  }'
```

#### Delete a User

```bash
curl -X DELETE "http://localhost:8000/api/v1/users/1"
```

#### Create an Order

```bash
curl -X POST "http://localhost:8000/api/v1/orders" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "product_name": "Laptop",
    "quantity": 2,
    "total_price": 2499.99,
    "status": "pending"
  }'
```

#### Get All Orders

```bash
curl -X GET "http://localhost:8000/api/v1/orders"
```

#### Update an Order

```bash
curl -X PUT "http://localhost:8000/api/v1/orders/1" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "completed"
  }'
```

### Using Python Requests

```python
import requests

BASE_URL = "http://localhost:8000/api/v1"

# Create a user
user_data = {
    "email": "jane.doe@example.com",
    "username": "janedoe",
    "full_name": "Jane Doe"
}
response = requests.post(f"{BASE_URL}/users", json=user_data)
user = response.json()
print(f"Created user: {user}")

# Create an order
order_data = {
    "user_id": user["id"],
    "product_name": "Smartphone",
    "quantity": 1,
    "total_price": 999.99,
    "status": "pending"
}
response = requests.post(f"{BASE_URL}/orders", json=order_data)
order = response.json()
print(f"Created order: {order}")

# Get all users
response = requests.get(f"{BASE_URL}/users")
users = response.json()
print(f"All users: {users}")

# Update order status
response = requests.put(
    f"{BASE_URL}/orders/{order['id']}",
    json={"status": "completed"}
)
updated_order = response.json()
print(f"Updated order: {updated_order}")
```

## Architecture Layers in Each Slice

### 1. Models (Pydantic Schemas)
- **Purpose**: Data validation and serialization
- **Files**: `models.py`
- **Contains**: Request/response schemas

### 2. Endpoints (API Routes)
- **Purpose**: Handle HTTP requests and responses
- **Files**: `endpoints.py`
- **Contains**: FastAPI route handlers

### 3. Service (Business Logic)
- **Purpose**: Implement business rules and validation
- **Files**: `service.py`
- **Contains**: Business logic, validation, error handling

### 4. Repository (Data Access)
- **Purpose**: Database operations
- **Files**: `repository.py`
- **Contains**: CRUD operations, queries

## RESTful Standards Compliance

This API follows RESTful best practices:

1. **Resource-based URLs**: `/users`, `/orders`
2. **HTTP Methods**:
   - GET (retrieve)
   - POST (create)
   - PUT (update)
   - DELETE (delete)
3. **Status Codes**:
   - 200 OK (successful GET, PUT)
   - 201 Created (successful POST)
   - 204 No Content (successful DELETE)
   - 400 Bad Request (validation errors)
   - 404 Not Found (resource not found)
4. **JSON responses**: All responses in JSON format
5. **Pagination support**: List endpoints support `skip` and `limit` parameters
6. **Proper error messages**: Clear, descriptive error messages

## Database

The application uses SQLite by default for simplicity. The database is automatically created when you run the application.

To use a different database, update the `DATABASE_URL` in `.env` file:

```bash
# PostgreSQL
DATABASE_URL=postgresql://user:password@localhost/dbname

# MySQL
DATABASE_URL=mysql://user:password@localhost/dbname
```

## Testing

You can test the API using:

1. **Swagger UI**: Interactive API documentation at http://localhost:8000/api/docs
2. **cURL**: Command-line tool (examples above)
3. **Postman**: Import the OpenAPI schema from http://localhost:8000/api/openapi.json
4. **Python requests**: Use the Python examples above

## License

MIT License
