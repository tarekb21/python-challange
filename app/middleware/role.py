from fastapi import Header, HTTPException
from app.models import Role


def get_user_role(x_user_role: str = Header(None, alias="x-user-role")) -> Role:
    """
    Dependency that extracts user role from request headers.
    """
    if not x_user_role:
        raise HTTPException(status_code=401, detail="User role required in x-user-role header")

    try:
        return Role(x_user_role.lower())
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid role: {x_user_role}")


def require_roles(allowed_roles: list[Role]):
    """
    Returns a dependency that checks if the user has one of the allowed roles.

    Usage:
        @router.post("/", dependencies=[Depends(require_roles([Role.ADMIN]))])
        def create_something():
            ...
    """
    def role_checker(x_user_role: str = Header(None, alias="x-user-role")) -> Role:
        if not x_user_role:
            raise HTTPException(status_code=401, detail="User role required in x-user-role header")

        try:
            role = Role(x_user_role.lower())
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid role: {x_user_role}")

        if role not in allowed_roles:
            raise HTTPException(status_code=403, detail="Forbidden")

        return role

    return role_checker
