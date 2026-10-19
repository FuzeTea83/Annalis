import uuid
from datetime import timedelta

from sqlalchemy.orm import Session

from core.exeptions import InvalidEmailDomainError, InvalidCredentialsError, EmailAlreadyExistsError, InvalidTokenError, \
    UserNotFoundError
from models import User
from schemas import UserResponse, UserCreate, AuthResponse, UserLogin
from core.security import hash_password, verify_password, create_access_token, create_reset_token, verify_reset_token
from schemas.user import ForgotPasswordRequest, ForgotPasswordResponse, ResetPasswordRequest, ResetPasswordResponse

allowed_domains = ["@etu.univ-amu.fr"]

def compute_initials(first_name: str, last_name: str) -> str:
    parts = [p for p in (first_name, last_name) if p and p.strip()]
    return "".join(p[0].upper() for p in parts) or "?"

def verify_email_domain(email: str) -> bool:
    return any(email.endswith(domain) for domain in allowed_domains)


class UserService:
    def __init__(self, db: Session):
        self.db = db

    def get_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(User.email == email).first()

    def get_by_id(self, user_id: str) -> User | None:
        return self.db.get(User, user_id)


    def create_user(self, register: UserCreate) -> User:
        if not verify_email_domain(register.email):
            raise InvalidEmailDomainError(allowed_domains)

        if self.get_by_email(register.email):
            raise EmailAlreadyExistsError

        user = User(
            id_account=str(uuid.uuid4()),
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

    def authenticate(self, login: UserLogin) -> User:
        if not verify_email_domain(login.email):
            raise InvalidEmailDomainError(allowed_domains)

        user = self.get_by_email(login.email)

        if not user or not verify_password(login.password, user.hashed_password):
            raise InvalidCredentialsError
        return user

    def build_user_response(self, user: User) -> UserResponse:
        initials = compute_initials(user.first_name, user.last_name)
        return UserResponse(
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            initials=initials,
            admin=user.admin,
        )

    def build_auth_response(self, user: User) -> AuthResponse:
        access_token_expires = timedelta(minutes=60)
        access_token = create_access_token(data={"sub": str(user.id_account)}, expires_delta=access_token_expires)

        return AuthResponse(
            token=access_token,
            token_type="bearer",
            user=self.build_user_response(user)
        )

    def send_reset_email(self, email: str, link: str):
        print(f"📧 [DEV MODE] Email de reset envoyé à {email} avec le lien : {link}")
        # En prod : email.send(link)

    def forgot_password(self, req: ForgotPasswordRequest):
        user = self.get_by_email(req.email)

        if user:
            token = create_reset_token(user.id_account)
            reset_link = f"http://localhost:5173/reset-password?token={token}"
            self.send_reset_email(req.email, reset_link)

        return ForgotPasswordResponse(message="Si l'adresse email est valide, un email de réinitialisation a été envoyé.")

    def reset_password(self, req: ResetPasswordRequest):
        user_id = verify_reset_token(req.token)
        if user_id is None:
            raise InvalidTokenError

        hashed_password = hash_password(req.new_password)

        self.update_user_password(user_id, hashed_password)

        return ResetPasswordResponse(message="Mot de passe réinitialisé avec succès.")

    def update_user_password(self, user_id: str, hashed_password: str):
        user = self.get_by_id(user_id)
        if not user:
            raise UserNotFoundError

        user.hashed_password = hashed_password
        self.db.commit()
        self.db.refresh(user)