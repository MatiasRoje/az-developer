from pydantic import BaseModel, EmailStr
from typing import Optional


class UserCredentials(BaseModel):
    username: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int = 86400  # 24 hours


class TokenValidationResponse(BaseModel):
    username: str
    exp: int
    iat: int


class UserRecord(BaseModel):
    """User data model matching SQLite schema"""

    id: Optional[int] = None
    username: str
    email: str
    password: str  # In production: hash with bcrypt
    created_at: Optional[str] = None
