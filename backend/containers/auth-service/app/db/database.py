import logging
import asyncpg
from fastapi import HTTPException, status
from typing import Optional

from app.core.config import settings
from app.models.schemas import UserRecord

logger = logging.getLogger(__name__)


async def init_database():
    """
    Initialize PostgreSQL database and create tables
    This runs when the auth-service starts up
    """
    try:
        conn = await asyncpg.connect(settings.DATABASE_URL)
        
        # Create users table
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(255) NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            )
        """)

        # Insert demo user
        await conn.execute("""
            INSERT INTO users (username, email, password) 
            VALUES ($1, $2, $3)
            ON CONFLICT (email) DO NOTHING
        """, 'Azure Developer', 'demo@azure.com', 'Testing123')

        await conn.close()
        logger.info("PostgreSQL database initialized successfully")

    except Exception as e:
        logger.error(f"PostgreSQL initialization error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database initialization failed",
        )


async def get_user_by_email(email: str) -> Optional[UserRecord]:
    """
    Retrieve user from PostgreSQL database
    """
    try:
        conn = await asyncpg.connect(settings.DATABASE_URL)
        
        row = await conn.fetchrow(
            "SELECT id, username, email, password, created_at FROM users WHERE email = $1",
            email
        )
        
        await conn.close()

        if row:
            return UserRecord(
                id=row["id"],
                username=row["username"],
                email=row["email"],
                password=row["password"],
                created_at=row["created_at"],
            )
        return None

    except Exception as e:
        logger.error(f"PostgreSQL query error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database operation failed",
        )


async def validate_user_credentials(
    username: str, password: str
) -> dict[str, bool | UserRecord | None]:
    """
    Validate user credentials against database
    """
    try:
        user = await get_user_by_email(username)

        if user and user.password == password:
            # TODO: In production, use bcrypt.checkpw
            return {"is_valid": True, "user": user}

        return {"is_valid": False, "user": None}

    except Exception as e:
        logger.error(f"User validation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Authentication service error",
        )
