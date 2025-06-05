"""
FastAPI Gateway Service for Azure Certification Demo
AZ-204 Focus: API Gateway patterns, Service Discovery, Load Balancing
Routes: Auth Service integration with future microservices support
"""

from datetime import datetime
from typing import Optional, Dict, Any
import os
import httpx
from fastapi import FastAPI, Request, HTTPException, status, Depends
from fastapi.security import HTTPBearer
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import logging
import uvicorn

# Configure logging (AZ-204: Application Insights integration patterns)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Azure Gateway Microservice",
    description="API Gateway for Azure certification demo - Routes to Auth and future services",
    version="1.0.0"
)

# Security schemes
bearer_auth = HTTPBearer(auto_error=False)

# Service configuration (AZ-204: Service Discovery patterns)
class ServiceConfig(BaseModel):
    """Configuration for downstream services"""
    auth_service_url: str
    timeout: int = 30

def get_service_config() -> ServiceConfig:
    """
    AZ-204 Exam Note: In production, use Azure Service Discovery
    - Azure Container Apps: Built-in service discovery
    - AKS: Kubernetes service discovery
    - API Management: Backend service configuration
    """
    return ServiceConfig(
        auth_service_url=os.environ.get("AUTH_SERVICE_URL", "http://localhost:8000"),
        timeout=int(os.environ.get("SERVICE_TIMEOUT", "30"))
    )

# Request/Response models for type safety
class LoginRequest(BaseModel):
    """Login request forwarding model"""
    pass  # Will forward raw basic auth

class TokenValidationRequest(BaseModel):
    """Token validation request model"""
    pass  # Will forward authorization header

class HealthResponse(BaseModel):
    """Gateway health response"""
    status: str
    timestamp: str
    services: Dict[str, str]

async def forward_to_auth_service(
    method: str,
    path: str,
    request: Request,
    config: ServiceConfig
) -> Dict[str, Any]:
    """
    Forward requests to auth service with proper error handling
    AZ-204 Pattern: Microservice communication with circuit breaker concepts
    """
    
    # Prepare headers for forwarding
    headers = dict(request.headers)
    
    # Remove host header to avoid conflicts
    headers.pop('host', None)
    
    # Construct target URL
    target_url = f"{config.auth_service_url}{path}"
    
    try:
        async with httpx.AsyncClient(timeout=config.timeout) as client:
            
            if method == "GET":
                response = await client.get(target_url, headers=headers)
            elif method == "POST":
                # Get request body for POST requests
                body = await request.body()
                response = await client.post(
                    target_url, 
                    headers=headers, 
                    content=body
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                    detail=f"Method {method} not supported"
                )
            
            # Log the forwarding
            logger.info(f"Forwarded {method} {path} to auth-service: {response.status_code}")
            
            # Return response data
            return {
                "status_code": response.status_code,
                "content": response.json() if response.headers.get("content-type", "").startswith("application/json") else response.text,
                "headers": dict(response.headers)
            }
            
    except httpx.TimeoutException:
        logger.error(f"Timeout forwarding to auth-service: {target_url}")
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail="Auth service timeout"
        )
    except httpx.RequestError as e:
        logger.error(f"Request error forwarding to auth-service: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Auth service unavailable"
        )
    except Exception as e:
        logger.error(f"Unexpected error forwarding to auth-service: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Gateway internal error"
        )

@app.post("/login")
async def login_proxy(request: Request):
    """
    Login endpoint - forwards to auth service
    
    AZ-204 Exam Focus:
    - API Gateway routing patterns
    - Authentication flow through gateway
    - Service-to-service communication
    - Load balancing and failover concepts
    """
    
    config = get_service_config()
    result = await forward_to_auth_service("POST", "/login", request, config)
    
    # Return response with original status code
    return JSONResponse(
        content=result["content"],
        status_code=result["status_code"]
    )

@app.post("/validate")
async def validate_proxy(request: Request):
    """
    Token validation endpoint - forwards to auth service
    
    AZ-204 Exam Scenario:
    - Centralized token validation through gateway
    - Microservice authentication patterns
    - API Gateway security policies
    """
    
    config = get_service_config()
    result = await forward_to_auth_service("POST", "/validate", request, config)
    
    return JSONResponse(
        content=result["content"],
        status_code=result["status_code"]
    )

@app.get("/auth/health")
async def auth_health_proxy(request: Request):
    """
    Auth service health check through gateway
    AZ-204 Pattern: Health monitoring through API Gateway
    """
    
    config = get_service_config()
    result = await forward_to_auth_service("GET", "/health", request, config)
    
    return JSONResponse(
        content=result["content"],
        status_code=result["status_code"]
    )

@app.get("/auth/users")
async def users_proxy(request: Request):
    """
    Users endpoint proxy (development only)
    AZ-204 Note: In production, add proper authorization middleware
    """
    
    config = get_service_config()
    result = await forward_to_auth_service("GET", "/users", request, config)
    
    return JSONResponse(
        content=result["content"],
        status_code=result["status_code"]
    )

@app.get("/health", response_model=HealthResponse)
async def gateway_health() -> HealthResponse:
    """
    Gateway health check endpoint
    AZ-204 Pattern: Multi-service health aggregation
    """
    
    config = get_service_config()
    services_status = {}
    
    # Check auth service health
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            response = await client.get(f"{config.auth_service_url}/health")
            services_status["auth-service"] = "healthy" if response.status_code == 200 else "unhealthy"
    except Exception:
        services_status["auth-service"] = "unhealthy"
    
    # Determine overall gateway status
    gateway_status = "healthy" if all(status == "healthy" for status in services_status.values()) else "degraded"
    
    return HealthResponse(
        status=gateway_status,
        timestamp=datetime.utcnow().isoformat(),
        services=services_status
    )

@app.get("/")
async def root() -> Dict[str, Any]:
    """Gateway information endpoint"""
    return {
        "service": "Azure API Gateway",
        "version": "1.0.0",
        "description": "FastAPI Gateway for microservices routing",
        "routes": {
            "authentication": ["/login", "/validate"],
            "health": ["/health", "/auth/health"],
            "development": ["/auth/users"]
        },
        "downstream_services": ["auth-service"],
        "azure_integration": [
            "API Management (future)",
            "Application Gateway (future)",
            "Container Apps Ingress (future)"
        ]
    }

# AZ-204 Exam Note: Gateway Middleware Patterns
@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    """
    Request logging middleware
    AZ-204 Pattern: Centralized logging and monitoring through gateway
    """
    
    start_time = datetime.utcnow()
    
    # Log incoming request
    logger.info(f"Gateway: {request.method} {request.url.path}")
    
    # Process request
    response = await call_next(request)
    
    # Calculate processing time
    process_time = datetime.utcnow() - start_time
    
    # Log response
    logger.info(f"Gateway: {request.method} {request.url.path} - {response.status_code} - {process_time.total_seconds():.3f}s")
    
    # Add custom headers for tracing (AZ-204: Distributed tracing patterns)
    response.headers["X-Process-Time"] = str(process_time.total_seconds())
    response.headers["X-Gateway-Version"] = "1.0.0"
    
    return response

# AZ-204 Exam Note: FastAPI automatically generates OpenAPI/Swagger documentation
# Access at /docs for interactive API testing - crucial for API Management integration

if __name__ == "__main__":    
    # AZ-204 Production Pattern: Use environment-based configuration
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", "8080"))
    
    # Gateway typically runs on port 8080
    uvicorn.run(
        "app:app",
        host=host,
        port=port,
        reload=os.environ.get("ENVIRONMENT", "development") == "development"
    ) 