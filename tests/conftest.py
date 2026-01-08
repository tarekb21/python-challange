import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db import db


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture(autouse=True)
def clear_db():
    """Clear the database before each test."""
    db.clear()
    yield
    db.clear()
