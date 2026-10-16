from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import get_db
from schemas import UserCreate, AuthResponse, UserLogin
from services.user_service import UserService


router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED, responses={
    201: {"description": "User registered successfully"},
    409: {"description": "User already exists"},
})
def register(user_data: UserCreate, db: Annotated[Session, Depends(get_db)]):
    service = UserService(db)

    try:
        new_user = service.create_user(user_data)
        return service.build_auth_response(new_user)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
@router.post("/login", response_model=AuthResponse, status_code=status.HTTP_200_OK, responses={
    200: {"description": "User logged in successfully"},
    401: {"description": "Invalid credentials"},
})
def login(user_data: UserLogin, db: Annotated[Session, Depends(get_db)]):
    service = UserService(db)

    try:
        user = service.authenticate(user_data.email, user_data.password)
        return service.build_auth_response(user)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


