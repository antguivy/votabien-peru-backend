from pydantic import BaseModel, EmailStr


class RegisterUserRequest(BaseModel):
    name: str
    email: EmailStr
    password: str


class VerifyUserRequest(BaseModel):
    token: str
    email: EmailStr


class RefreshTokenRequest(BaseModel):
    refresh_token: str
