from datetime import timedelta

from sqlalchemy.orm import Session
from models import User
from schemas import UserResponse, UserCreate, AuthResponse
from core.security import hash_password, verify_password, create_access_token


def compute_initials(first_name: str, last_name: str) -> str:
    """Calcule les initiales, ex: 'Jean Dupont' -> 'JD'."""
    parts = [p for p in (first_name, last_name) if p and p.strip()]
    return "".join(p[0].upper() for p in parts) or "?"

class UserService:
    def __init__(self, db: Session):
        self.db = db

    def get_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(User.email == email).first()

    def get_by_id(self, user_id: int) -> User | None:
        return self.db.get(User, user_id)


    def create_user(self, register: UserCreate) -> User:
        if self.get_by_email(register.email):
            raise ValueError("Email already exists")

        user = User(
            email=register.email,
            hashed_password=hash_password(register.password),
            first_name=register.first_name,
            last_name=register.last_name,
            admin=False,
            is_active=True,
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def authenticate(self, email: str, password: str) -> User:
        user = self.get_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            raise ValueError("Invalid credentials")
        return user

    def build_auth_response(self, user: User) -> AuthResponse:
        access_token_expires = timedelta(minutes=60)
        access_token = create_access_token(data={"sub": str(user.id_account)}, expires_delta=access_token_expires)

        initials = compute_initials(user.first_name, user.last_name)

        return AuthResponse(
            access_token=access_token,
            token_type="bearer",
            user=UserResponse(
                email=user.email,
                first_name=user.first_name,
                last_name=user.last_name,
                initials=initials,
                admin=user.admin,
            ),
        )