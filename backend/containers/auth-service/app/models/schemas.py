from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserCredentials(BaseModel):
    username: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int = 86400  # 24 hours


class TokenValidationResponse(BaseModel):
    username: str
    id: int
    email: str
    exp: int
    iat: int


class UserRecord(BaseModel):
    """User data model for PostgreSQL"""

    id: Optional[int] = None
    username: str
    email: str
    password: str  # In production: hash with bcrypt
    created_at: Optional[datetime] = None  # Changed from str to datetime
