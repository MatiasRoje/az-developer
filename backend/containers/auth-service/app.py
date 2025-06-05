"""
FastAPI Auth Service for Azure Certification Demo
AZ-204 Focus: API Development, Authentication, Microservices Patterns
Database: SQLite (local) → CosmosDB (Azure)
"""

from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
import os
import jwt
import aiosqlite
import sqlite3
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials, HTTPBearer
from pydantic import BaseModel, EmailStr
import logging
from contextlib import asynccontextmanager

# curl http://localhost:8000/
# Configure logging (AZ-204: Application Insights integration patterns)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database file path
DB_FILE = "auth_service.db"

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    AZ-204 Pattern: Application lifecycle management
    Initialize database on startup, cleanup on shutdown
    """
    # Startup - Create database and tables
    await init_database()
    logger.info("Database initialized")
    
    yield
    
    # Shutdown - cleanup if needed
    logger.info("Application shutdown")

app = FastAPI(
    title="Azure Auth Microservice",
    description="Authentication service for Azure certification demo - SQLite Edition",
    version="1.0.0",
    lifespan=lifespan
)

# Security schemes
basic_auth = HTTPBasic()
bearer_auth = HTTPBearer()

# Pydantic models for type safety (AZ-204: API input validation)
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
    email: str
    password: str  # In production: hash with bcrypt
    created_at: Optional[str] = None

def get_jwt_secret() -> str:
    """
    AZ-204 Exam Note: Store JWT secrets in Azure Key Vault
    Use Key Vault references in App Service configuration
    """
    secret = os.environ.get("JWT_SECRET", "your-super-secret-jwt-key-change-in-production")
    if not secret:
        raise ValueError("JWT_SECRET environment variable is required")
    return secret

def create_jwt_token(username: str, secret: str) -> str:
    """
    Create JWT token with proper expiration and claims
    AZ-204 Exam Focus: Token lifecycle management and security best practices
    """
    now = datetime.now(tz=timezone.utc)
    payload = {
        "username": username,
        "exp": now + timedelta(days=1),
        "iat": now,
        "iss": "azure-auth-service",  # Issuer claim for token validation
        "aud": "azure-microservices"   # Audience claim
    }
    
    return jwt.encode(payload, secret, algorithm="HS256")

def verify_jwt_token(token: str, secret: str) -> Dict[str, Any]:
    """
    Verify and decode JWT token
    AZ-204 Exam Note: Common exam scenario for API Gateway authentication
    """
    try:
        payload = jwt.decode(
            token, 
            secret, 
            algorithms=["HS256"],
            options={"verify_exp": True, "verify_iat": True}
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

async def init_database():
    """
    Initialize SQLite database and create tables
    AZ-204 Note: In production, use Azure Database Migration Service
    """
    async with aiosqlite.connect(DB_FILE) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Insert sample users (for demo only)
        await db.execute("""
            INSERT OR IGNORE INTO users (email, password) 
            VALUES 
                ('demo@azure.com', 'Testing123')
        """)
        
        await db.commit()

async def get_user_by_email(email: str) -> Optional[UserRecord]:
    """
    Retrieve user from SQLite database
    AZ-204 Security Pattern: Always use parameterized queries to prevent SQL injection
    """
    try:
        async with aiosqlite.connect(DB_FILE) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute(
                "SELECT id, email, password, created_at FROM users WHERE email = ?", 
                (email,)
            ) as cursor:
                row = await cursor.fetchone()
                
                if row:
                    return UserRecord(
                        id=row['id'],
                        email=row['email'],
                        password=row['password'],
                        created_at=row['created_at']
                    )
                return None
                
    except Exception as e:
        logger.error(f"Database query error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database operation failed"
        )

async def validate_user_credentials(username: str, password: str) -> bool:
    """
    Validate user credentials against database
    AZ-204 Security Pattern: Structured authentication flow
    """
    try:
        user = await get_user_by_email(username)
        
        if user and user.password == password:
            # TODO: In production, use bcrypt.checkpw(password.encode('utf-8'), user.password)
            return True
        
        return False
        
    except Exception as e:
        logger.error(f"User validation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Authentication service error"
        )

@app.post("/login", response_model=TokenResponse)
async def login(credentials: HTTPBasicCredentials = Depends(basic_auth)) -> TokenResponse:
    """
    User authentication endpoint
    
    AZ-204 Exam Focus:
    - HTTP Basic Authentication for simple scenarios
    - JWT token generation for stateless authentication
    - Proper error handling and status codes
    - API Gateway integration patterns
    """
    
    if not credentials.username or not credentials.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username and password are required"
        )
    
    # Validate credentials
    is_valid = await validate_user_credentials(credentials.username, credentials.password)
    
    if not is_valid:
        # AZ-204 Security: Don't reveal whether user exists or password is wrong
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"}
        )
    
    # Create JWT token
    jwt_secret = get_jwt_secret()
    access_token = create_jwt_token(
        username=credentials.username,
        secret=jwt_secret
    )
    
    logger.info(f"User {credentials.username} authenticated successfully")
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=86400
    )

@app.post("/validate", response_model=TokenValidationResponse)
async def validate_token(token: str = Depends(bearer_auth)) -> TokenValidationResponse:
    """
    Token validation endpoint for other microservices
    
    AZ-204 Exam Scenario: 
    - API Gateway token validation
    - Microservice-to-microservice authentication
    - Centralized authentication patterns
    """
    
    jwt_secret = get_jwt_secret()
    payload = verify_jwt_token(token.credentials, jwt_secret)
    
    logger.info(f"Token validated for user: {payload.get('username')}")
    
    return TokenValidationResponse(
        username=payload["username"],
        exp=payload["exp"],
        iat=payload["iat"]
    )

@app.get("/health")
async def health_check() -> Dict[str, str]:
    """
    Health check endpoint
    AZ-204 Pattern: Essential for Azure Load Balancer and Application Gateway
    """
    try:
        # Test database connectivity
        async with aiosqlite.connect(DB_FILE) as db:
            await db.execute("SELECT 1")
            return {"status": "healthy", "database": "connected"}
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Service unhealthy"
        )

@app.get("/users")
async def list_users() -> Dict[str, Any]:
    """
    List all users (for development/testing only)
    AZ-204 Note: Remove in production, add proper authorization
    """
    try:
        async with aiosqlite.connect(DB_FILE) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute("SELECT id, email, created_at FROM users") as cursor:
                rows = await cursor.fetchall()
                users = [dict(row) for row in rows]
                return {"users": users, "count": len(users)}
    except Exception as e:
        logger.error(f"Database query error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database operation failed"
        )

@app.get("/")
async def root() -> Dict[str, str]:
    """API information endpoint"""
    return {
        "service": "Azure Auth Microservice",
        "version": "1.0.0",
        "database": "SQLite (local development)",
        "status": "running",
        "endpoints": "/login, /validate, /health, /users"
    }

# AZ-204 Exam Note: FastAPI automatically generates OpenAPI/Swagger documentation
# Access at /docs for interactive API testing - crucial for API Management scenarios

if __name__ == "__main__":
    import uvicorn
    
    # AZ-204 Production Pattern: Use environment-based configuration
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", "8000"))
    
    uvicorn.run(
        "app:app",
        host=host,
        port=port,
        reload=os.environ.get("ENVIRONMENT", "development") == "development"
    )
