import logging
import aiosqlite
from fastapi import HTTPException, status
from typing import Optional

from app.core.config import settings
from app.models.schemas import UserRecord

logger = logging.getLogger(__name__)


async def init_database():
    """
    Initialize SQLite database for local development and create tables
    """
    async with aiosqlite.connect(settings.DB_FILE) as db:
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        )

        # Insert sample user for demo purposes
        await db.execute(
            """
            INSERT OR IGNORE INTO users (username, email, password)
            VALUES
                ('Azure Developer', 'demo@azure.com', 'Testing123')
        """
        )

        await db.commit()


async def get_user_by_email(email: str) -> Optional[UserRecord]:
    """
    Retrieve user from SQLite database
    """
    try:
        async with aiosqlite.connect(settings.DB_FILE) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute(
                "SELECT id, username, email, password, created_at FROM "
                "users WHERE email = ?",
                (email,),
            ) as cursor:
                row = await cursor.fetchone()

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
        logger.error(f"Database query error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database operation failed",
        )


async def validate_user_credentials(username: str, password: str) -> bool:
    """
    Validate user credentials against database
    """
    try:
        user = await get_user_by_email(username)

        if user and user.password == password:
            # TODO: In production, use bcrypt.checkpw (password.encode('utf-8'), user.password)
            return True

        return False

    except Exception as e:
        logger.error(f"User validation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Authentication service error",
        )
