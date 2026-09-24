import hashlib
import secrets

from pwdlib import PasswordHash
from datetime import datetime, timedelta, timezone
from app.core.config import settings

password_hasher = PasswordHash.recommended()

def hash_password(password: str) -> str:
    return password_hasher.hash(password)

def verify_password(
    plain_password: str,
    password_hash: str,
) -> bool:
    return password_hasher.verify(
        plain_password,
        password_hash,
    )

def generate_session_token() -> str:
    return secrets.token_urlsafe(32)

def hash_session_token(token: str) -> str:
    return hashlib.sha256(
        token.encode("utf-8")
    ).hexdigest()

def get_session_expiry() -> datetime:
    return datetime.now(timezone.utc) + timedelta(
        days=settings.session_expire_days
    )