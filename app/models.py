from enum import Enum
from typing import Optional
from pydantic import BaseModel


class Role(str, Enum):
    ADMIN = "admin"
    EDITOR = "editor"
    VIEWER = "viewer"


class User(BaseModel):
    id: str
    name: str
    email: Optional[str] = None
    age: Optional[int] = None
    tenant_id: str


class UserCreate(BaseModel):
    name: str
    email: Optional[str] = None
    age: Optional[int] = None


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    age: Optional[int] = None
