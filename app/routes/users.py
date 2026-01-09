from fastapi import APIRouter, Depends, HTTPException
from uuid import uuid4

from app.db import db
from app.models import User, UserCreate, UserUpdate, Response, Role
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
    if not user_data.name:
        raise HTTPException(status_code=400, detail="Name cannot be empty")
    
    # TODO 2: Create a new User object with a unique id and tenant_id
    new_user: User = User(
        id=str(uuid4()),
        tenant_id=tenant_id,
        name=user_data.name,
        email=user_data.email,
        age=user_data.age,
    )
    # TODO 3: Save the user in the in-memory db for this tenant
    if tenant_id not in db:
        db[tenant_id] = []
    db[tenant_id].append(new_user)

    # TODO 4: Return the new user
    return Response(
        success=True,
        message="User created successfully",
        data=new_user
    )

# List users (any role)
@router.get("/")
def list_users(
    tenant_id: str = Depends(get_tenant_id),
    role: Role = Depends(get_user_role), # you defined role but in the task it says
    # we should list users for any role
):
    # TODO 5: Return all users for this tenant
    users = db.get(tenant_id, [])
    return Response(
        success=True,
        message="Users retrieved successfully",
        data=users
    )


# Update user (admin/editor only)
@router.put("/{user_id}", dependencies=[Depends(require_roles([Role.ADMIN, Role.EDITOR]))])
def update_user(
    user_id: str,
    user_data: UserUpdate,
    tenant_id: str = Depends(get_tenant_id),
):
    # TODO 6: Find user by id in this tenant
    users = db.get(tenant_id, [])
    user = next((u for u in users if u.id == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    
    # TODO 7: Update user fields from request body (only non-None fields)
    updated_user = user.model_copy(update=user_data.model_dump(exclude_unset=True))
    users[users.index(user)] = updated_user

    # TODO 8: Return updated user or 404 if not found
    return Response(
        success=True,
        message="User updated successfully",
        data=updated_user
    )

# Delete user (admin only)
@router.delete("/{user_id}", dependencies=[Depends(require_roles([Role.ADMIN]))])
def delete_user(
    user_id: str,
    tenant_id: str = Depends(get_tenant_id),
):
    # TODO 9: Find user by id in this tenant
    users = db.get(tenant_id, [])
    user = next((u for u in users if u.id == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # TODO 10: Remove user from db
    users.remove(user)

    # TODO 11: Return success response or 404 if not found
    return Response(
        success=True,
        message="User deleted successfully",
        data=None
    )
