from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr, validate_email, TypeAdapter
from sqlalchemy.orm import Session

from core.dependencies import get_current_user
from database import get_db
from models import User
from schemas import UserCreate, AuthResponse, UserLogin, UserResponse
from schemas.user import ForgotPasswordRequest, ResetPasswordRequest
from services.user_service import UserService


router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, db: Annotated[Session, Depends(get_db)]):
    service = UserService(db)
    new_user = service.create_user(user_data)
    return service.build_auth_response(new_user)

@router.post("/login", response_model=AuthResponse, status_code=status.HTTP_200_OK)
def login(user_data: UserLogin, db: Annotated[Session, Depends(get_db)]):
    service = UserService(db)
    user = service.authenticate(user_data)
    return service.build_auth_response(user)

@router.get("/me", response_model=UserResponse, status_code=status.HTTP_200_OK)
def me(current_user: Annotated[User, Depends(get_current_user)], db: Annotated[Session, Depends(get_db)]):
    service = UserService(db)
    return service.build_user_response(current_user)

@router.post("/logout")
def logout():
    pass

@router.post("forgot-password")
def forgot_password(req: ForgotPasswordRequest, db: Annotated[Session, Depends(get_db)]):
    service = UserService(db)
    return service.forgot_password(req)

@router.post("/auth/reset-password")
def reset_password(req: ResetPasswordRequest, db: Annotated[Session, Depends(get_db)]):
    service = UserService(db)
    return service.reset_password(req)
