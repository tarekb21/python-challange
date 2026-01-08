from fastapi import Header, HTTPException


def get_tenant_id(x_tenant_id: str = Header(...)) -> str:
    """
    Dependency that extracts tenant ID from request headers.
    """
    if not x_tenant_id:
        raise HTTPException(status_code=400, detail="Tenant ID required in x-tenant-id header")
    return x_tenant_id
