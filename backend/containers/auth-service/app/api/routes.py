import logging
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import (
    HTTPBasicCredentials,
    HTTPAuthorizationCredentials,
    HTTPBasic,
    HTTPBearer,
)

from app.core.auth import create_jwt_token, verify_jwt_token
from app.db.database import validate_user_credentials
from app.models.schemas import TokenResponse, TokenValidationResponse

# Security schemes
basic_auth = HTTPBasic()
bearer_auth = HTTPBearer()

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/login", response_model=TokenResponse)
async def login(
    credentials: HTTPBasicCredentials = Depends(basic_auth),
) -> TokenResponse:
    """
    User authentication endpoint
    """
    if not credentials.username or not credentials.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username and password are required",
        )

    is_valid = await validate_user_credentials(
        credentials.username, credentials.password
    )

    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )

    access_token = create_jwt_token(username=credentials.username)
    logger.info(f"User {credentials.username} authenticated successfully")

    return TokenResponse(
        access_token=access_token, token_type="bearer", expires_in=86400
    )


@router.post("/validate", response_model=TokenValidationResponse)
async def validate_token(
    token: HTTPAuthorizationCredentials = Depends(bearer_auth),
) -> TokenValidationResponse:
    """
    Token validation endpoint for other microservices
    """
    payload = verify_jwt_token(token.credentials)
    return TokenValidationResponse(
        username=payload["username"], exp=payload["exp"], iat=payload["iat"]
    )


@router.get("/")
async def root() -> dict:
    """API information endpoint"""
    return {
        "service": "Azure Auth Microservice",
        "version": "1.0.0",
        "database": "SQLite (local development)",
        "status": "running",
    }
