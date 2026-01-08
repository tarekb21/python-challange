from fastapi import APIRouter, Depends, HTTPException
from uuid import uuid4

from app.db import db
from app.models import User, UserCreate, UserUpdate, Role
from app.middleware.tenant import get_tenant_id
from app.middleware.role import require_roles, get_user_role

router = APIRouter(prefix="/users", tags=["users"])


# Create user (admin only)
@router.post("/", dependencies=[Depends(require_roles([Role.ADMIN]))])
def create_user(
    user_data: UserCreate,
    tenant_id: str = Depends(get_tenant_id),
):
    # TODO 1: Validate that name is not empty
    # TODO 2: Create a new User object with a unique id and tenant_id
    # TODO 3: Save the user in the in-memory db for this tenant
    # TODO 4: Return the new user

    return {"success": False, "message": "TODO: Implement this endpoint"}


# List users (any role)
@router.get("/")
def list_users(
    tenant_id: str = Depends(get_tenant_id),
    role: Role = Depends(get_user_role),
):
    # TODO 5: Return all users for this tenant

    return {"success": False, "message": "TODO: Implement this endpoint"}


# Update user (admin/editor only)
@router.put("/{user_id}", dependencies=[Depends(require_roles([Role.ADMIN, Role.EDITOR]))])
def update_user(
    user_id: str,
    user_data: UserUpdate,
    tenant_id: str = Depends(get_tenant_id),
):
    # TODO 6: Find user by id in this tenant
    # TODO 7: Update user fields from request body (only non-None fields)
    # TODO 8: Return updated user or 404 if not found

    return {"success": False, "message": "TODO: Implement this endpoint"}


# Delete user (admin only)
@router.delete("/{user_id}", dependencies=[Depends(require_roles([Role.ADMIN]))])
def delete_user(
    user_id: str,
    tenant_id: str = Depends(get_tenant_id),
):
    # TODO 9: Find user by id in this tenant
    # TODO 10: Remove user from db
    # TODO 11: Return success response or 404 if not found

    return {"success": False, "message": "TODO: Implement this endpoint"}
