from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from core.exeptions import InvalidTokenError, UserNotFoundError
from database import get_db
from core.security import decode_access_token
from models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = decode_access_token(token)
    if not payload:
        raise InvalidTokenError

    user_id = payload.get("sub")
    if not user_id:
        raise InvalidTokenError

    user = db.query(User).filter(User.id_account == user_id).first()
    if not user:
        raise UserNotFoundError
    return user