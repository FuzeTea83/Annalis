from pydantic import BaseModel, EmailStr

from schemas.base import CamelModel


class UserBase(CamelModel):
    email: EmailStr

class UserLogin(UserBase):
    password: str

class UserCreate(UserLogin):
    first_name: str
    last_name: str

class UserUpdate(CamelModel):
    email: EmailStr | None = None
    password: str | None = None
    is_active: bool | None = None

class UserResponse(UserBase):
    first_name: str
    last_name: str
    initials: str
    admin: bool

class AuthResponse(CamelModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse