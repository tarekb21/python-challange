import pytest
from fastapi.testclient import TestClient


class TestCreateUser:
    """Tests for POST /users - Create user (admin only)"""

    def test_create_user_as_admin(self, client: TestClient):
        """Admin should be able to create a user."""
        response = client.post(
            "/users",
            json={"name": "John Doe", "email": "john@example.com", "age": 30},
            headers={"x-tenant-id": "tenant-1", "x-user-role": "admin"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "John Doe"
        assert data["email"] == "john@example.com"
        assert data["age"] == 30
        assert "id" in data
        assert data["tenant_id"] == "tenant-1"

    def test_create_user_as_editor_forbidden(self, client: TestClient):
        """Editor should not be able to create a user."""
        response = client.post(
            "/users",
            json={"name": "John Doe"},
            headers={"x-tenant-id": "tenant-1", "x-user-role": "editor"},
        )
        assert response.status_code == 403

    def test_create_user_as_viewer_forbidden(self, client: TestClient):
        """Viewer should not be able to create a user."""
        response = client.post(
            "/users",
            json={"name": "John Doe"},
            headers={"x-tenant-id": "tenant-1", "x-user-role": "viewer"},
        )
        assert response.status_code == 403

    def test_create_user_without_role_header(self, client: TestClient):
        """Request without role header should return 401."""
        response = client.post(
            "/users",
            json={"name": "John Doe"},
            headers={"x-tenant-id": "tenant-1"},
        )
        assert response.status_code == 401

    def test_create_user_empty_name_fails(self, client: TestClient):
        """Creating a user with empty name should fail."""
        response = client.post(
            "/users",
            json={"name": ""},
            headers={"x-tenant-id": "tenant-1", "x-user-role": "admin"},
        )
        assert response.status_code == 400


class TestListUsers:
    """Tests for GET /users - List users (any role)"""

    def test_list_users_empty(self, client: TestClient):
        """Should return empty list when no users exist."""
        response = client.get(
            "/users",
            headers={"x-tenant-id": "tenant-1", "x-user-role": "viewer"},
        )
        assert response.status_code == 200
        assert response.json() == []

    def test_list_users_returns_created_users(self, client: TestClient):
        """Should return all users for the tenant."""
        # Create two users
        client.post(
            "/users",
            json={"name": "User 1"},
            headers={"x-tenant-id": "tenant-1", "x-user-role": "admin"},
        )
        client.post(
            "/users",
            json={"name": "User 2"},
            headers={"x-tenant-id": "tenant-1", "x-user-role": "admin"},
        )

        response = client.get(
            "/users",
            headers={"x-tenant-id": "tenant-1", "x-user-role": "viewer"},
        )
        assert response.status_code == 200
        users = response.json()
        assert len(users) == 2
        names = [u["name"] for u in users]
        assert "User 1" in names
        assert "User 2" in names

    def test_list_users_tenant_isolation(self, client: TestClient):
        """Users from one tenant should not be visible to another."""
        # Create user in tenant-1
        client.post(
            "/users",
            json={"name": "Tenant 1 User"},
            headers={"x-tenant-id": "tenant-1", "x-user-role": "admin"},
        )
        # Create user in tenant-2
        client.post(
            "/users",
            json={"name": "Tenant 2 User"},
            headers={"x-tenant-id": "tenant-2", "x-user-role": "admin"},
        )

        # List users in tenant-1
        response = client.get(
            "/users",
            headers={"x-tenant-id": "tenant-1", "x-user-role": "viewer"},
        )
        users = response.json()
        assert len(users) == 1
        assert users[0]["name"] == "Tenant 1 User"

    def test_list_users_all_roles_allowed(self, client: TestClient):
        """All roles should be able to list users."""
        for role in ["admin", "editor", "viewer"]:
            response = client.get(
                "/users",
                headers={"x-tenant-id": "tenant-1", "x-user-role": role},
            )
            assert response.status_code == 200


class TestUpdateUser:
    """Tests for PUT /users/{id} - Update user (admin/editor only)"""

    def test_update_user_as_admin(self, client: TestClient):
        """Admin should be able to update a user."""
        # Create a user first
        create_response = client.post(
            "/users",
            json={"name": "Original Name", "email": "original@example.com"},
            headers={"x-tenant-id": "tenant-1", "x-user-role": "admin"},
        )
        user_id = create_response.json()["id"]

        # Update the user
        response = client.put(
            f"/users/{user_id}",
            json={"name": "Updated Name"},
            headers={"x-tenant-id": "tenant-1", "x-user-role": "admin"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated Name"
        assert data["email"] == "original@example.com"  # Should remain unchanged

    def test_update_user_as_editor(self, client: TestClient):
        """Editor should be able to update a user."""
        create_response = client.post(
            "/users",
            json={"name": "Original Name"},
            headers={"x-tenant-id": "tenant-1", "x-user-role": "admin"},
        )
        user_id = create_response.json()["id"]

        response = client.put(
            f"/users/{user_id}",
            json={"name": "Editor Updated"},
            headers={"x-tenant-id": "tenant-1", "x-user-role": "editor"},
        )
        assert response.status_code == 200
        assert response.json()["name"] == "Editor Updated"

    def test_update_user_as_viewer_forbidden(self, client: TestClient):
        """Viewer should not be able to update a user."""
        create_response = client.post(
            "/users",
            json={"name": "Original Name"},
            headers={"x-tenant-id": "tenant-1", "x-user-role": "admin"},
        )
        user_id = create_response.json()["id"]

        response = client.put(
            f"/users/{user_id}",
            json={"name": "Updated Name"},
            headers={"x-tenant-id": "tenant-1", "x-user-role": "viewer"},
        )
        assert response.status_code == 403

    def test_update_nonexistent_user_returns_404(self, client: TestClient):
        """Updating a non-existent user should return 404."""
        response = client.put(
            "/users/nonexistent-id",
            json={"name": "Updated Name"},
            headers={"x-tenant-id": "tenant-1", "x-user-role": "admin"},
        )
        assert response.status_code == 404


class TestDeleteUser:
    """Tests for DELETE /users/{id} - Delete user (admin only)"""

    def test_delete_user_as_admin(self, client: TestClient):
        """Admin should be able to delete a user."""
        create_response = client.post(
            "/users",
            json={"name": "To Delete"},
            headers={"x-tenant-id": "tenant-1", "x-user-role": "admin"},
        )
        user_id = create_response.json()["id"]

        response = client.delete(
            f"/users/{user_id}",
            headers={"x-tenant-id": "tenant-1", "x-user-role": "admin"},
        )
        assert response.status_code == 200

        # Verify user is deleted
        list_response = client.get(
            "/users",
            headers={"x-tenant-id": "tenant-1", "x-user-role": "viewer"},
        )
        assert len(list_response.json()) == 0

    def test_delete_user_as_editor_forbidden(self, client: TestClient):
        """Editor should not be able to delete a user."""
        create_response = client.post(
            "/users",
            json={"name": "To Delete"},
            headers={"x-tenant-id": "tenant-1", "x-user-role": "admin"},
        )
        user_id = create_response.json()["id"]

        response = client.delete(
            f"/users/{user_id}",
            headers={"x-tenant-id": "tenant-1", "x-user-role": "editor"},
        )
        assert response.status_code == 403

    def test_delete_user_as_viewer_forbidden(self, client: TestClient):
        """Viewer should not be able to delete a user."""
        create_response = client.post(
            "/users",
            json={"name": "To Delete"},
            headers={"x-tenant-id": "tenant-1", "x-user-role": "admin"},
        )
        user_id = create_response.json()["id"]

        response = client.delete(
            f"/users/{user_id}",
            headers={"x-tenant-id": "tenant-1", "x-user-role": "viewer"},
        )
        assert response.status_code == 403

    def test_delete_nonexistent_user_returns_404(self, client: TestClient):
        """Deleting a non-existent user should return 404."""
        response = client.delete(
            "/users/nonexistent-id",
            headers={"x-tenant-id": "tenant-1", "x-user-role": "admin"},
        )
        assert response.status_code == 404

    def test_delete_user_tenant_isolation(self, client: TestClient):
        """Should not be able to delete a user from another tenant."""
        create_response = client.post(
            "/users",
            json={"name": "Tenant 1 User"},
            headers={"x-tenant-id": "tenant-1", "x-user-role": "admin"},
        )
        user_id = create_response.json()["id"]

        # Try to delete from tenant-2
        response = client.delete(
            f"/users/{user_id}",
            headers={"x-tenant-id": "tenant-2", "x-user-role": "admin"},
        )
        assert response.status_code == 404

        # Verify user still exists in tenant-1
        list_response = client.get(
            "/users",
            headers={"x-tenant-id": "tenant-1", "x-user-role": "viewer"},
        )
        assert len(list_response.json()) == 1
