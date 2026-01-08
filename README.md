# Python Developer Challenge - User Management API

A multi-tenant user management API with Role-Based Access Control (RBAC).

## Getting Started (CodeSandbox)

The server starts automatically. Use the terminal to run tests:

```bash
pytest tests/ -v
```

## Local Setup

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Your Task

Implement the TODO items in `app/routes/users.py`. There are 11 TODOs to complete.

### Endpoints

| Method | Endpoint      | Required Role  | Description       |
|--------|---------------|----------------|-------------------|
| POST   | /users        | admin          | Create a user     |
| GET    | /users        | any            | List all users    |
| PUT    | /users/{id}   | admin, editor  | Update a user     |
| DELETE | /users/{id}   | admin          | Delete a user     |

### Headers

All requests require:
- `x-tenant-id`: The tenant identifier
- `x-user-role`: The user's role (`admin`, `editor`, or `viewer`)

### Example Requests

```bash
# Create a user (as admin)
curl -X POST http://localhost:8000/users \
  -H "Content-Type: application/json" \
  -H "x-tenant-id: tenant-1" \
  -H "x-user-role: admin" \
  -d '{"name": "John Doe", "email": "john@example.com", "age": 30}'

# List users
curl http://localhost:8000/users \
  -H "x-tenant-id: tenant-1" \
  -H "x-user-role: viewer"

# Update a user (as editor)
curl -X PUT http://localhost:8000/users/{user_id} \
  -H "Content-Type: application/json" \
  -H "x-tenant-id: tenant-1" \
  -H "x-user-role: editor" \
  -d '{"name": "Jane Doe"}'

# Delete a user (as admin)
curl -X DELETE http://localhost:8000/users/{user_id} \
  -H "x-tenant-id: tenant-1" \
  -H "x-user-role: admin"
```

## Run Tests

```bash
pytest tests/ -v
```

## Hints

- Use `uuid4()` to generate unique IDs
- The database is a simple dict: `db[tenant_id]` returns a list of users
- Check if a tenant exists in the db before accessing it
- Use Pydantic's `model_dump(exclude_unset=True)` for partial updates
