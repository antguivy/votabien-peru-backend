import logging
from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, Request
from sqlalchemy.orm import joinedload
from sqlmodel import Session, select

from app.config.security import (
    generate_token,
    get_token_payload,
    hash_password,
    load_user,
    str_decode,
    str_encode,
    verify_password,
)
from app.config.settings import get_settings
from app.models.auth import User, UserToken, VerificationToken
from app.services.email import (
    send_account_activation_confirmation_email,
    send_account_verification_email,
)
from app.utils.string import unique_string

logger = logging.getLogger(__name__)

settings = get_settings()


async def create_user_account(data, session: Session, background_tasks):
    statement = select(User).where(User.email == data.email)
    existing_user = session.exec(statement).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Este correo ya está en uso")

    # if not is_password_strong_enough(data.password):
    #     raise HTTPException(status_code=400, detail="Please provide a strong password.")

    hashed_password = hash_password(data.password)
    user_data = data.model_dump()
    user_data["password"] = hashed_password
    user_data["email_verified"] = None

    user = User(**user_data)
    session.add(user)
    session.commit()
    session.refresh(user)

    verification_token = await create_verification_token(user.email, session)

    await send_account_verification_email(
        user, verification_token.token, background_tasks
    )

    return user


async def logout_user(access_token: str, session: Session):
    """
    Logs out user by invalidating all their tokens.
    """
    token_payload = get_token_payload(
        access_token,
        settings.JWT_SECRET_KEY,
        settings.JWT_ALGORITHM,
        allow_expired=True,
    )

    if not token_payload:
        raise HTTPException(status_code=401, detail="Token inválido.")

    try:
        user_id = str_decode(token_payload.get("sub"))
        token_id = str_decode(token_payload.get("r"))

        # Invalidar el token específico
        user_token = session.exec(
            select(UserToken).where(
                UserToken.id == token_id, UserToken.user_id == user_id
            )
        ).first()

        if user_token:
            user_token.expires_at = datetime.now(timezone.utc)
            session.add(user_token)
            session.commit()

            return {"message": "Sesión cerrada exitosamente."}

        return {"message": "Token ya estaba invalidado."}

    except Exception as e:
        logger.error("Error during logout: %s", e)
        raise HTTPException(status_code=500, detail="Error al cerrar sesión.")


async def create_verification_token(email: str, session: Session):
    """
    Creates a unique verification token for the email.
    """
    # Delete old tokens
    old_tokens = session.exec(
        select(VerificationToken).where(VerificationToken.email == email)
    ).all()
    for token in old_tokens:
        session.delete(token)

    token_string = unique_string(64)

    # Token expire in 24 hours
    expires_at = datetime.now(timezone.utc) + timedelta(hours=24)

    verification_token = VerificationToken(
        email=email, token=token_string, expires_at=expires_at
    )

    session.add(verification_token)
    session.commit()
    session.refresh(verification_token)

    return verification_token


async def activate_user_account(data, session: Session, background_tasks):
    """
    Active user account using the verification token.
    """
    logger.info("Intentando activar cuenta para email: %s", data.email)

    statement = select(User).where(User.email == data.email)
    user = session.exec(statement).first()
    if not user:
        logger.warning("Intento de verificación con email inexistente: %s", data.email)
        raise HTTPException(status_code=400, detail="Enlace de verificación inválido.")

    if user.email_verified:
        raise HTTPException(status_code=400, detail="Esta cuenta ya está verificada.")

    token_statement = select(VerificationToken).where(
        VerificationToken.email == data.email, VerificationToken.token == data.token
    )
    verification_token = session.exec(token_statement).first()

    if not verification_token:
        logger.warning("Token de verificación inválido para: %s", data.email)
        raise HTTPException(status_code=400, detail="Token de verificación inválido.")

    if verification_token.expires_at < datetime.now(timezone.utc):
        session.delete(verification_token)
        session.commit()
        logger.warning("Token expirado para: %s", data.email)
        raise HTTPException(
            status_code=400, detail="El token de verificación ha expirado."
        )

    try:
        user.email_verified = datetime.now(timezone.utc)
        user.updated_at = datetime.now(timezone.utc)

        session.add(user)
        session.delete(verification_token)
        session.commit()
        session.refresh(user)

        await send_account_activation_confirmation_email(user, background_tasks)

        return {"message": "Cuenta varificada exitosamente. Ya puedes iniciar sesión."}

    except Exception:
        session.rollback()
        logger.error(
            "Error al activar cuenta y crear datos por defecto para: %s", user.email
        )
        raise HTTPException(
            status_code=500,
            detail="Error interno del servidor al activar la cuenta. Intenta nuevamente.",
        )


async def get_login_token(data, session: Session, request: Request):
    """
    User autentication and token access generation
    """
    user = await load_user(data.username, session)

    if not user:
        raise HTTPException(
            status_code=404, detail="El correo electrónico no está registrado."
        )

    if not verify_password(data.password, user.password):
        raise HTTPException(status_code=400, detail="Correo o contraseña incorrectos.")

    if not user.email_verified:
        raise HTTPException(
            status_code=403,
            detail="Tu cuenta no está verificada. Revisa tu correo para verificarla.",
        )

    tokens = _generate_tokens(user, session, request)

    return {**tokens, "user": user}


async def get_refresh_token(refresh_token, session):
    """
    Refreshes access token using refresh token.
    Implements sliding window and token rotation.
    """
    token_payload = get_token_payload(
        refresh_token,
        settings.JWT_SECRET_KEY,
        settings.JWT_ALGORITHM,
        allow_expired=False,
    )

    if not token_payload:
        raise HTTPException(
            status_code=401, detail="Refresh token inválido o expirado."
        )

    # Extrae los datos del payload
    refresh_key = token_payload.get("t")
    access_key = token_payload.get("a")
    user_id = str_decode(token_payload.get("sub"))
    if not all([refresh_key, access_key, user_id]):
        raise HTTPException(
            status_code=401, detail="Refresh token con estructura inválida."
        )
    now_utc = datetime.now(timezone.utc)

    user_token = session.exec(
        select(UserToken)
        .options(joinedload(UserToken.user))
        .where(
            UserToken.refresh_key == refresh_key,
            UserToken.access_key == access_key,
            UserToken.user_id == user_id,
            UserToken.expires_at > now_utc,
        )
    ).first()

    if not user_token:
        raise HTTPException(
            status_code=401,
            detail="Refresh token inválido o expirado. Por favor inicia sesión nuevamente.",
        )

    # Invalidar el refresh token usado (refresh token rotation)
    user_token.last_used_at = now_utc

    # 5. Determinar si renovar refresh_token (Sliding Window)
    time_remaining = user_token.expires_at - now_utc
    days_remaining = time_remaining.days
    should_renew_refresh = False

    if settings.REFRESH_TOKEN_SLIDING_WINDOW:
        if days_remaining < settings.REFRESH_TOKEN_RENEWAL_THRESHOLD_DAYS:
            should_renew_refresh = True

    # 6. Generar nuevos tokens
    if should_renew_refresh:
        # Generar nuevo refresh_token y access_token (rotation completa)
        new_refresh_key = unique_string(100)
        new_access_key = unique_string(50)

        user_token.refresh_key = new_refresh_key
        user_token.access_key = new_access_key
        user_token.expires_at = now_utc + timedelta(
            minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES
        )

        session.add(user_token)
        session.commit()
        session.refresh(user_token)

        # Generar nuevos tokens JWT
        tokens = _generate_tokens_from_existing_user_token(user_token)

        logger.info(
            "Refresh token renovado para usuario %s... (quedaban %s días, ahora válido por 7 días más)",
            user_id[:8],
            days_remaining,
        )

        return {**tokens, "user": user_token.user}

    else:
        # Solo generar nuevo access_token (reutilizar refresh_token)
        session.add(user_token)
        session.commit()

        tokens = _generate_access_token_only(user_token)

        logger.info(
            "Access token renovado para usuario %s... (refresh_token aún válido por %s días)",
            user_id[:8],
            days_remaining,
        )

        return {**tokens, "user": user_token.user}


def _generate_tokens(user, session: Session, request: Request):
    """
    Generates new access and refresh tokens for a user.
    Returns:
        dict: Contains access_token, refresh_token, and expires_in
    """
    refresh_key = unique_string(100)
    access_key = unique_string(50)
    rt_expires = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    now = datetime.now(timezone.utc)

    ip_address = request.client.host if request.client else None
    user_agent = request.headers.get("user-agent", "Unknown")
    # Crear nuevo UserToken en DB
    user_token = UserToken(
        user_id=user.id,
        access_key=access_key,
        refresh_key=refresh_key,
        ip_address=ip_address,
        user_agent=user_agent,
        expires_at=now + rt_expires,
        last_used_at=now,
    )
    session.add(user_token)
    session.commit()
    session.refresh(user_token)

    # ============ ACCESS TOKEN ============
    at_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    at_payload = {
        "sub": str_encode(str(user.id)),
        "a": access_key,
        "r": str_encode(str(user_token.id)),
    }

    access_token = generate_token(
        at_payload, settings.JWT_SECRET_KEY, settings.JWT_ALGORITHM, at_expires
    )

    # ============ REFRESH TOKEN ============
    rt_payload = {"sub": str_encode(str(user.id)), "t": refresh_key, "a": access_key}

    refresh_token = generate_token(
        rt_payload, settings.JWT_SECRET_KEY, settings.JWT_ALGORITHM, rt_expires
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "expires_in": at_expires.total_seconds(),
    }


def _generate_tokens_from_existing_user_token(user_token: UserToken) -> dict:
    """
    Generates new tokens from existing UserToken (cuando se renueva el refresh).
    """
    at_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    rt_expires = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)

    # Access token
    at_payload = {
        "sub": str_encode(str(user_token.user_id)),
        "a": user_token.access_key,
        "r": str_encode(str(user_token.id)),
    }
    access_token = generate_token(
        at_payload, settings.JWT_SECRET_KEY, settings.JWT_ALGORITHM, at_expires
    )

    # Refresh token
    rt_payload = {
        "sub": str_encode(str(user_token.user_id)),
        "t": user_token.refresh_key,
        "a": user_token.access_key,
    }
    refresh_token = generate_token(
        rt_payload, settings.JWT_SECRET_KEY, settings.JWT_ALGORITHM, rt_expires
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "expires_in": at_expires.total_seconds(),
    }


def _generate_access_token_only(user_token: UserToken) -> dict:
    """
    Generates only new access_token, reusing existing refresh_token.
    Used when refresh_token still has enough time remaining.
    """
    at_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    # Access token
    at_payload = {
        "sub": str_encode(str(user_token.user_id)),
        "a": user_token.access_key,
        "r": str_encode(str(user_token.id)),
    }
    access_token = generate_token(
        at_payload, settings.JWT_SECRET_KEY, settings.JWT_ALGORITHM, at_expires
    )

    # NO generar nuevo refresh_token, el cliente sigue usando el actual
    # Por eso retornamos None en refresh_token
    return {
        "access_token": access_token,
        "refresh_token": None,  # Indica al frontend que NO actualice la cookie
        "expires_in": at_expires.total_seconds(),
    }
