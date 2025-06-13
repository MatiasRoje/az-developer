from datetime import datetime, timedelta, timezone
from typing import Dict, Any
import jwt
from fastapi import HTTPException, status
import logging

from app.core.config import settings

logger = logging.getLogger(__name__)


def create_jwt_token(username: str) -> str:
    """
    Create JWT token with proper expiration and claims
    """
    now = datetime.now(tz=timezone.utc)
    payload = {
        "username": username,
        "exp": now + timedelta(days=1),
        "iat": now,
        "iss": "azure-auth-service",
        "aud": "azure-microservices",
    }

    return jwt.encode(payload, settings.get_jwt_secret(), algorithm="HS256")


def verify_jwt_token(token: str) -> Dict[str, Any]:
    """
    Verify and decode JWT token
    """
    try:
        payload = jwt.decode(
            token,
            settings.get_jwt_secret(),
            algorithms=["HS256"],
            options={
                "verify_exp": True,
                "verify_iat": True,
                "verify_aud": True,
            },
            audience="azure-microservices",
            issuer="azure-auth-service",
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired"
        )
    except jwt.InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid token: {str(e)}"
        )
