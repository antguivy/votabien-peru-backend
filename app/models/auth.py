from datetime import datetime, timezone
from typing import List, Optional

from cuid2 import Cuid
from sqlmodel import Column, DateTime, Field, Relationship, SQLModel


def cuid_factory():
    """Generate cuid id"""
    return Cuid().generate()


def utc_now():
    """Generate utc now"""
    return datetime.now(timezone.utc)


class UserToken(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="user.id")
    access_key: Optional[str] = Field(default=None, index=True, max_length=250)
    refresh_key: Optional[str] = Field(default=None, index=True, max_length=250)
    ip_address: Optional[str] = Field(default=None, max_length=45)  # IPv6 compatible
    user_agent: Optional[str] = Field(default=None, max_length=255)
    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), nullable=False),
        default_factory=utc_now,
    )
    last_used_at: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True), nullable=True), default=None
    )
    expires_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), nullable=False)
    )

    user: "User" = Relationship(back_populates="tokens")


class User(SQLModel, table=True):
    id: str = Field(default_factory=cuid_factory, primary_key=True)
    name: Optional[str] = Field(default=None, max_length=150)
    email: str = Field(default=None, unique=True)
    email_verified: Optional[datetime] = None
    image: Optional[str] = None
    password: Optional[str] = None
    is_admin: bool = Field(default=False)
    tokens: List["UserToken"] = Relationship(back_populates="user")
    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), nullable=False),
        default_factory=utc_now,
    )
    updated_at: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True), nullable=True)
    )


class VerificationToken(SQLModel, table=True):
    id: str = Field(default_factory=cuid_factory, primary_key=True)
    email: str = Field(nullable=False, max_length=255)
    token: str = Field(nullable=False, unique=True, max_length=255)

    expires_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), nullable=False)
    )
    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), nullable=False),
        default_factory=utc_now,
    )
