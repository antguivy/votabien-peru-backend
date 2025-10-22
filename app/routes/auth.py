from fastapi import (
    APIRouter,
    BackgroundTasks,
    Cookie,
    Depends,
    HTTPException,
    Request,
    Response,
    status,
)
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session

from app.config.database import get_session
from app.config.security import get_current_user, get_token_user, oauth2_scheme
from app.responses.auth import LoginResponse, UserResponse
from app.schemas.auth import RegisterUserRequest, VerifyUserRequest
from app.services import auth
from app.utils.cookies import _clear_token_cookies, _set_token_cookies

auth_router = APIRouter(
    prefix="/auth", tags=["Auth"], responses={404: {"description": "Not found"}}
)

users_router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(oauth2_scheme), Depends(get_current_user)],
)


# ====== AUTH (público) ======
@auth_router.post(
    "/register", status_code=status.HTTP_201_CREATED, response_model=UserResponse
)
async def register_user(
    data: RegisterUserRequest,
    background_tasks: BackgroundTasks,
    session: Session = Depends(get_session),
):
    return await auth.create_user_account(data, session, background_tasks)


@auth_router.post(
    "/login", status_code=status.HTTP_200_OK, response_model=LoginResponse
)
async def user_login(
    request: Request,
    response: Response,
    data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    """User login endpoint."""
    result = await auth.get_login_token(data, session, request)
    # Setear httpOnly cookies
    _set_token_cookies(response, result)
    return result


@auth_router.post(
    "/refresh", status_code=status.HTTP_200_OK, response_model=LoginResponse
)
async def refresh_token(
    response: Response,
    refresh_token: str = Cookie(None),
    session: Session = Depends(get_session),
):
    """Refresh access token using refresh token cookie."""
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="No refresh token provided"
        )

    result = await auth.get_refresh_token(refresh_token, session)

    # Setear cookies (siempre access_token, opcionalmente refresh_token)
    _set_token_cookies(response, result)

    return result


@auth_router.post("/new-verification", status_code=status.HTTP_200_OK)
async def verify_user_account(
    data: VerifyUserRequest,
    background_tasks: BackgroundTasks,
    session: Session = Depends(get_session),
):
    await auth.activate_user_account(data, session, background_tasks)
    return JSONResponse({"message": "Account is activated successfully."})


@auth_router.post("/verify-token", status_code=status.HTTP_200_OK)
async def verify_token(
    token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)
):
    """Verify if actual token is valid"""
    actual_user = await get_token_user(token, session)
    if actual_user:
        return {"valid": True, "user_id": actual_user.id}
    return {"valid": False}


# ====== USERS (require login) ======
@users_router.get("/me", status_code=status.HTTP_200_OK, response_model=UserResponse)
async def fetch_user(current_user=Depends(get_current_user)):
    """Get user info"""
    return current_user


@users_router.post(
    "/logout", status_code=status.HTTP_200_OK, response_model=UserResponse
)
async def logout_user(
    response: Response,
    access_token: str = Cookie(None),
    current_user=Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """Logout user (invalidate tokens and clear cookies)."""
    if access_token:
        await auth.logout_user(access_token, session)

    # Limpiar cookies
    _clear_token_cookies(response)

    return {"message": "Successfully logged out.", "status": "success"}
