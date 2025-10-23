import base64
import logging
from datetime import datetime, timedelta, timezone

import jwt
from argon2 import PasswordHasher
from argon2.exceptions import (
    HashingError,
    InvalidHash,
    VerificationError,
    VerifyMismatchError,
)
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import Session

from app.config.database import get_session
from app.config.settings import get_settings
from app.models.auth import User, UserToken

logger = logging.getLogger(__name__)
settings = get_settings()

ESPECIAL_CHARACTERS = ["@", "#", "$", "%", "=", ":", "?", ".", "/", "|", "~", ">"]
ph = PasswordHasher(
    time_cost=3, memory_cost=65536, parallelism=4, hash_len=32, salt_len=16
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def hash_password(password: str) -> str | None:
    """Hashes a password using Argon2."""
    try:
        return ph.hash(password)
    except HashingError as e:
        logger.error("Error hashing password: %s", e)
        raise


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a password against its hash using Argon2."""
    try:
        ph.verify(hashed_password, plain_password)
        return True
    except VerifyMismatchError:
        return False
    except (InvalidHash, VerificationError) as e:
        logger.error("Error verifying password: %s", e)
        return False


def is_password_strong_enough(password: str) -> bool:
    """Checks if the password meets strength requirements."""
    if len(password) < 8:
        return False
    if not any(char.isupper() for char in password):
        return False
    if not any(char.islower() for char in password):
        return False
    if not any(char.isdigit() for char in password):
        return False
    if not any(char in ESPECIAL_CHARACTERS for char in password):
        return False
    return True


def str_encode(string: str) -> str:
    """Encodes a string to bytes and then to a base85 string."""
    return base64.b85encode(string.encode("ascii")).decode("ascii")


def str_decode(string: str) -> str:
    """Decodes a base85 string back to the original string."""
    return base64.b85decode(string.encode("ascii")).decode("ascii")


def get_token_payload(
    token: str, secret: str, algo: str, allow_expired: bool = False
) -> str | None:
    """Decodes a JWT token and returns its payload."""
    try:
        if allow_expired:
            # Decodificar sin verificar expiración
            payload = jwt.decode(
                token, secret, algorithms=[algo], options={"verify_exp": False}
            )
        else:
            # Decodificar normalmente (verifica expiración)
            payload = jwt.decode(token, secret, algorithms=[algo])

        return payload

    except jwt.ExpiredSignatureError:
        return None

    except jwt.InvalidTokenError as e:
        logger.error("Invalid token: %s", e)
        return None


def generate_token(
    payload: dict, secret: str, algo: str, expiry: timedelta
) -> str | None:
    """Generates a JWT token with the given payload and expiration."""
    now = datetime.now(timezone.utc)
    expire = now + expiry

    token_payload = {
        **payload,  # Copia
        "iat": int(now.timestamp()),
        "exp": int(expire.timestamp()),
    }

    return jwt.encode(token_payload, secret, algorithm=algo)


async def get_token_user(token: str, db) -> User | None:
    """Gets user info from the token payload."""
    payload = get_token_payload(
        token, settings.JWT_SECRET_KEY, settings.JWT_ALGORITHM, allow_expired=False
    )

    if not payload:
        return None

    user_token_id = str_decode(payload.get("r"))
    user_id = str_decode(payload.get("sub"))
    access_key = payload.get("a")

    if not all([user_token_id, user_id, access_key]):
        return None

    user_token = (
        db.query(UserToken)
        .filter(
            UserToken.access_key == access_key,
            UserToken.id == user_token_id,
            UserToken.user_id == user_id,
            UserToken.expires_at > datetime.now(timezone.utc),
        )
        .first()
    )

    if user_token:
        return user_token.user

    return None


async def load_user(email: str, db):
    """Loads user from the database by email."""
    try:
        user = db.query(User).filter(User.email == email).first()
    except SQLAlchemyError as e:
        logger.error("Database error while loading user by email %s: %s", email, e)
        return None

    if not user:
        logger.info("User not found, Email: %s", email)
        return None

    return user


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_session)
):
    """Dependency to get the current user from the token."""
    user = await get_token_user(token, db)
    if user:
        if not user.id:
            return None
        return user
    raise HTTPException(status_code=401, detail="Not authorised.")
