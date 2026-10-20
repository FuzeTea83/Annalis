import secrets
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
import bcrypt

from app import settings

BCRYPT_MAX_BYTES = 72  # Limite technique de bcrypt
RESET_TOKEN_EXPIRE_MINUTES = 15

def _prepare(password: str) -> bytes:
    """Prépare le mot de passe pour le hachage en s'assurant qu'il ne dépasse pas la limite de bcrypt et qu'il est correctement encodé en UTF-8."""
    encoded = password.encode("utf-8")
    if len(encoded) <= BCRYPT_MAX_BYTES:
        return encoded

    truncated = encoded[:BCRYPT_MAX_BYTES]
    while truncated:
        try:
            truncated.decode("utf-8")
            break
        except UnicodeDecodeError:
            truncated = truncated[:-1]
    return truncated


def hash_password(password: str) -> str:
    """Hache le mot de passe en utilisant bcrypt avec un sel aléatoire et un coût de 12.
     Retourne le mot de passe haché sous forme de chaîne UTF-8."""
    return bcrypt.hashpw(_prepare(password), bcrypt.gensalt(rounds=12)).decode()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return bcrypt.checkpw(_prepare(plain_password), hashed_password.encode("utf-8"))
    except ValueError:
        return False

ALGORITHM = "HS256"

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Crée un token JWT avec les données fournies et une date d'expiration."""
    to_encode = data.copy()
    now = datetime.now(timezone.utc)
    expire = now + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"iat": now, "exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> dict | None:
    """Décode le token JWT et retourne le payload si valide, sinon None."""
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None


def generate_reset_token() -> str:
    """Token aléatoire cryptographiquement sûr pour forgot-password."""
    return secrets.token_urlsafe(32)

def create_reset_token(user_id: str) -> str:
    """Crée un token unique pour réinitialiser le mot de passe."""
    expire = datetime.now(timezone.utc) + timedelta(minutes=RESET_TOKEN_EXPIRE_MINUTES)

    salt = secrets.token_urlsafe(32)
    payload = {
        "sub": user_id,
        "exp": expire,
        "salt": salt,
        "type": "reset"
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=ALGORITHM)

def verify_reset_token(token: str) -> str | None:
    """Vérifie le token et retourne l'user_id si valide."""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "reset":
            return None
        user_id = payload.get("sub")
        if not user_id:
            return None
        return user_id
    except JWTError:
        return None