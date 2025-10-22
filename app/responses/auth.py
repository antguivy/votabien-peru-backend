from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr

from app.responses.base import BaseResponse


class UserResponse(BaseResponse):
    id: str
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    email_verified: Optional[datetime] = None
    image: Optional[str] = None
    created_at: datetime


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: Optional[str] = None
    expires_in: float
    token_type: str = "Bearer"
    user: UserResponse
