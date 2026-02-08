"""
JWT authentication and authorization module.

Implements FR-002 (JWT validation) and FR-003 (user identity extraction from JWT).

All protected routes MUST use get_current_user dependency to ensure
authenticated user_id is extracted from JWT token.
"""
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

from core.config import settings


# HTTP Bearer token security scheme
security = HTTPBearer()


def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]
) -> str:
    """
    Extract and validate authenticated user ID from JWT token.

    This dependency MUST be used on all protected endpoints to:
    1. Verify JWT signature using BETTER_AUTH_SECRET
    2. Extract user_id from 'sub' claim
    3. Return authenticated user_id for data isolation

    Args:
        credentials: Bearer token from Authorization header

    Returns:
        str: Authenticated user_id from JWT 'sub' claim

    Raises:
        HTTPException: 401 if token is missing, expired, invalid, or missing sub claim

    Usage:
        @app.get("/api/tasks")
        async def get_tasks(user_id: str = Depends(get_current_user)):
            # user_id is guaranteed to be authenticated
            # Filter all queries by this user_id
            pass

    Security Notes:
    - User identity MUST ONLY come from JWT token, NEVER from request body/params/query
    - All database queries MUST filter by this user_id to enforce data isolation
    - Token signature is verified using shared BETTER_AUTH_SECRET
    """
    token = credentials.credentials

    try:
        # Decode and verify JWT token
        # Algorithm: HS256 (symmetric, shared secret)
        # Verify signature, expiration (exp claim), and issued at (iat claim)
        payload = jwt.decode(
            token,
            settings.better_auth_secret,
            algorithms=["HS256"],
            options={
                "verify_signature": True,
                "verify_exp": True,
                "require": ["sub", "exp"],  # Require sub and exp claims
            }
        )

        # Extract user_id from 'sub' claim
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: missing sub claim",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return user_id

    except ExpiredSignatureError:
        # Token has expired
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except InvalidTokenError as e:
        # Token is malformed or signature is invalid
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        # Catch-all for unexpected errors
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed",
            headers={"WWW-Authenticate": "Bearer"},
        )


# Type alias for dependency injection
CurrentUser = Annotated[str, Depends(get_current_user)]


"""
JWT Token Format Assumptions (from Better Auth):

Expected JWT structure:
{
  "sub": "user-123",          # User identifier (REQUIRED)
  "exp": 1234567890,          # Expiration timestamp (REQUIRED)
  "iat": 1234567890,          # Issued at timestamp
  "iss": "better-auth",       # Issuer (optional)
  ... other claims
}

Algorithm: HS256 (HMAC with SHA-256)
Secret: BETTER_AUTH_SECRET environment variable (must match frontend)

Frontend Integration:
- Frontend sends JWT in Authorization header: "Bearer <token>"
- Token is issued by Better Auth on frontend
- Secret is shared between frontend and backend teams
- Token lifetime managed by frontend authentication system
"""
