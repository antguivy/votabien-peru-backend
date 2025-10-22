from fastapi import Response

from app.config.settings import get_settings

settings = get_settings()


def _set_token_cookies(response: Response, result: dict) -> None:
    """Set access and refresh cookies securely."""
    is_prod = settings.ENVIRONMENT == "production"

    response.set_cookie(
        key="access_token",
        value=result["access_token"],
        httponly=True,
        secure=is_prod,
        samesite="lax",
        max_age=int(result["expires_in"]),
        path="/",
    )

    if result.get("refresh_token"):
        refresh_max_age = 7 * 24 * 60 * 60
        response.set_cookie(
            key="refresh_token",
            value=result["refresh_token"],
            httponly=True,
            secure=is_prod,
            samesite="lax",
            max_age=refresh_max_age,
            path="/",
        )


def _clear_token_cookies(response: Response) -> None:
    """Remove auth cookies (for logout)."""
    response.delete_cookie("access_token", path="/", httponly=True)
    response.delete_cookie("refresh_token", path="/", httponly=True)
