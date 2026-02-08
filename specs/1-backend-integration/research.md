# Research Findings: Backend Integration

**Feature**: Full Backend + Frontend Integration
**Branch**: `1-backend-integration`
**Date**: 2026-02-07
**Status**: Complete

## Overview

This document consolidates research findings for all technical unknowns identified during planning. Each section follows the format: Decision, Rationale, Alternatives Considered, and References.

---

## 1. JWT Token Structure from Better Auth

### Decision
- **User Identifier Claim**: Use `sub` (subject) claim as the primary user identifier
- **Token Format**: JWT with HS256 algorithm (HMAC with SHA-256)
- **Expiration**: Respect `exp` claim; no refresh token handling in backend (frontend responsibility)
- **Required Claims**: `sub` (user ID), `exp` (expiration), `iat` (issued at)

### Rationale
- `sub` is the standard JWT claim for user identity according to RFC 7519
- HS256 is simpler and sufficient for shared-secret scenarios (frontend and backend share BETTER_AUTH_SECRET)
- Backend should be stateless and not manage token refresh - this is Better Auth's responsibility on the frontend
- Minimal claim validation reduces complexity while maintaining security

### Alternatives Considered
- **RS256 (RSA)**: More complex, requires public/private key pair. Overkill for internal monorepo where both services share a secret
- **Custom claim (user_id, userId)**: Non-standard. Better to follow JWT RFC conventions
- **Refresh token handling in backend**: Violates stateless design. Frontend should handle token refresh with Better Auth

### Implementation Details
```python
# JWT verification pseudo-code
import jwt
from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer

security = HTTPBearer()

def verify_token(credentials: HTTPAuthorizationCredentials):
    try:
        payload = jwt.decode(
            credentials.credentials,
            key=BETTER_AUTH_SECRET,
            algorithms=["HS256"]
        )
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(401, "Invalid token: missing sub claim")
        return user_id
    except jwt.ExpiredSignatureError:
        raise HTTPException(401, "Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(401, "Invalid token")
```

### References
- [RFC 7519 - JSON Web Token (JWT)](https://datatracker.ietf.org/doc/html/rfc7519)
- [PyJWT Documentation](https://pyjwt.readthedocs.io/)
- [Better Auth Documentation](https://www.better-auth.com/docs)

---

## 2. Neon PostgreSQL Connection Patterns

### Decision
- **Connection Pattern**: Use SQLModel with async engine and connection pooling
- **Pool Configuration**:
  - Min pool size: 1
  - Max pool size: 10
  - Pool recycle: 3600 seconds (1 hour)
  - Pool pre-ping: True (validates connections before use)
- **Environment Variable Format**: `postgresql+asyncpg://user:pass@host/dbname?sslmode=require`
- **Async Driver**: Use `asyncpg` for better performance with async FastAPI

### Rationale
- Neon is serverless and handles connection pooling on their end, but client-side pooling improves performance
- Async engine integrates better with FastAPI's async endpoints
- `pool_pre_ping=True` prevents "server closed connection" errors in serverless environments
- `pool_recycle=3600` ensures stale connections are refreshed
- SSL mode required for secure connections to Neon

### Alternatives Considered
- **Sync engine with psycopg2**: Simpler but blocks async event loop, reducing FastAPI performance
- **No connection pooling**: Would work but causes performance degradation under load
- **PgBouncer**: External connection pooler. Not needed since Neon handles this, and adds deployment complexity

### Implementation Details
```python
# db.py pseudo-code
from sqlmodel import create_engine, Session
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from contextlib import asynccontextmanager

DATABASE_URL = os.getenv("DATABASE_URL")

# Convert postgres:// to postgresql+asyncpg:// if needed
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+asyncpg://", 1)

engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    pool_size=10,
    max_overflow=0,
    pool_pre_ping=True,
    pool_recycle=3600
)

@asynccontextmanager
async def get_session():
    async with AsyncSession(engine) as session:
        yield session
```

### References
- [Neon Documentation - Connection Pooling](https://neon.tech/docs/connect/connection-pooling)
- [SQLAlchemy Async Documentation](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)
- [FastAPI with Databases](https://fastapi.tiangolo.com/advanced/async-sql-databases/)

---

## 3. FastAPI + SQLModel Integration Best Practices

### Decision
- **Pattern**: Async SQLModel with FastAPI dependency injection
- **Session Management**: Use FastAPI's `Depends()` to inject async database sessions
- **Migration Strategy**: Use Alembic for production migrations (not SQLModel.metadata.create_all)
- **Shutdown/Cleanup**: Implement lifespan context manager for engine disposal

### Rationale
- Dependency injection keeps route handlers clean and testable
- Alembic provides migration versioning, rollback capability, and team collaboration features
- Lifespan events ensure proper connection cleanup on shutdown
- Async SQLModel leverages FastAPI's async capabilities for better throughput

### Alternatives Considered
- **Sync SQLModel**: Simpler but blocks async endpoints, reducing performance
- **SQLModel.metadata.create_all**: Quick for development but no migration history or rollback
- **Manual session management**: More error-prone, harder to test
- **Raw SQLAlchemy without SQLModel**: More boilerplate, less type safety

### Implementation Details
```python
# Dependency injection pattern
from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

async def get_db_session() -> AsyncSession:
    async with AsyncSession(engine) as session:
        yield session

# Usage in routes
@router.get("/api/tasks")
async def get_tasks(
    db: AsyncSession = Depends(get_db_session),
    user_id: str = Depends(get_current_user)
):
    result = await db.execute(
        select(Task).where(Task.user_id == user_id)
    )
    return result.scalars().all()

# Lifespan for cleanup
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: could initialize DB here
    yield
    # Shutdown: dispose engine
    await engine.dispose()

app = FastAPI(lifespan=lifespan)
```

### References
- [FastAPI Dependency Injection](https://fastapi.tiangolo.com/tutorial/dependencies/)
- [SQLModel with FastAPI](https://sqlmodel.tiangolo.com/tutorial/fastapi/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)

---

## 4. CORS Configuration for Next.js Frontend

### Decision
- **Development Origin**: `http://localhost:3000`
- **Production Origin**: Environment variable `FRONTEND_URL` (e.g., `https://app.example.com`)
- **Allowed Methods**: GET, POST, PUT, DELETE, PATCH, OPTIONS
- **Allowed Headers**: Authorization, Content-Type, Accept
- **Expose Headers**: None required
- **Allow Credentials**: True (for cookies if needed in future)
- **Max Age**: 600 seconds (10 minutes for preflight cache)

### Rationale
- Next.js default dev server runs on port 3000
- Production origin should be configurable via environment variable
- `allow_credentials=True` enables cookie-based sessions if needed in future (currently JWT-only)
- Preflight caching reduces OPTIONS requests
- Authorization header is required for JWT Bearer tokens

### Alternatives Considered
- **Wildcard origins (*)**:  insecure, allows any origin
- **Hardcoded production URL**: Not flexible for staging/production environments
- **No CORS** (proxy through Next.js): Adds complexity, defeats purpose of separate backend

### Implementation Details
```python
# main.py
from fastapi.middleware.cors import CORSMiddleware

FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "Accept"],
    max_age=600
)
```

### References
- [FastAPI CORS Documentation](https://fastapi.tiangolo.com/tutorial/cors/)
- [MDN CORS Guide](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS)
- [Next.js API Routes](https://nextjs.org/docs/api-routes/introduction)

---

## 5. Error Handling Patterns

### Decision
- **Primary Mechanism**: FastAPI's built-in `HTTPException`
- **Custom Exception Handler**: Global handler for consistent error format
- **Error Response Format**:
  ```json
  {
    "detail": "Human-readable error message",
    "status_code": 400,
    "error_type": "validation_error"
  }
  ```
- **Logging**: Use Python's `logging` module with structured logs (no sensitive data)
- **Stack Traces**: Never expose in production (FastAPI hides by default)

### Rationale
- `HTTPException` is FastAPI's standard, well-integrated error mechanism
- Consistent error format makes frontend error handling predictable
- Structured logging enables observability without exposing sensitive data
- Global exception handler catches unexpected errors and formats them consistently

### Alternatives Considered
- **Custom exception classes**: More complex, FastAPI's `HTTPException` is sufficient
- **Exception middleware**: Possible but global handler is cleaner
- **Detailed error objects**: Too verbose, frontend only needs status and message

### Implementation Details
```python
# Custom exception handler
from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

app = FastAPI()

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content={
            "detail": "Validation error",
            "status_code": 400,
            "error_type": "validation_error",
            "errors": exc.errors()
        }
    )

# Usage in routes
from fastapi import HTTPException

@router.get("/api/tasks/{task_id}")
async def get_task(task_id: int, db: AsyncSession = Depends(get_db_session)):
    task = await db.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.user_id != current_user_id:
        raise HTTPException(status_code=404, detail="Task not found")  # Don't leak existence
    return task
```

### Logging Best Practices
- **Never log**: Passwords, JWT tokens, sensitive user data
- **Always log**: Request IDs, user IDs (hashed if needed), error types, stack traces (server-side only)
- **Use structured logging**: JSON format for easy parsing

```python
import logging
import json

logger = logging.getLogger(__name__)

# Structured log example
logger.info(json.dumps({
    "event": "task_created",
    "user_id": user_id,
    "task_id": task.id,
    "timestamp": datetime.utcnow().isoformat()
}))
```

### References
- [FastAPI Exception Handling](https://fastapi.tiangolo.com/tutorial/handling-errors/)
- [Python Logging Best Practices](https://docs.python.org/3/howto/logging.html)
- [OWASP Logging Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html)

---

## 6. Testing Strategy

### Decision
- **Test Framework**: pytest with FastAPI TestClient
- **JWT Mocking**: Create test tokens with known BETTER_AUTH_SECRET
- **Database Fixtures**: Use pytest fixtures with test database (separate from dev/prod)
- **Test Categories**:
  - **Unit Tests**: Individual functions (auth, validation)
  - **Integration Tests**: API endpoints with real DB
  - **Isolation Tests**: Multi-user data isolation scenarios
- **Coverage Target**: 80%+ for critical paths (auth, data isolation, CRUD)

### Rationale
- pytest is the Python standard with excellent FastAPI integration
- TestClient allows testing without running server
- Test database prevents pollution of dev/prod data
- Mocking JWT tokens enables testing auth flows without real Better Auth
- Multi-user tests are critical for verifying data isolation

### Alternatives Considered
- **unittest**: Less feature-rich than pytest
- **In-memory SQLite**: Faster but behavior differs from PostgreSQL (type system, constraints)
- **Mocking database**: Too fragile, misses real DB issues
- **Manual testing only**: Not repeatable, prone to regression

### Implementation Details

#### Test JWT Token Creation
```python
# tests/conftest.py
import pytest
import jwt
from datetime import datetime, timedelta

BETTER_AUTH_SECRET = "test-secret-key"

@pytest.fixture
def create_test_token():
    def _create(user_id: str, exp_delta: timedelta = timedelta(hours=1)):
        payload = {
            "sub": user_id,
            "exp": datetime.utcnow() + exp_delta,
            "iat": datetime.utcnow()
        }
        return jwt.encode(payload, BETTER_AUTH_SECRET, algorithm="HS256")
    return _create

@pytest.fixture
def auth_headers(create_test_token):
    token = create_test_token("test-user-123")
    return {"Authorization": f"Bearer {token}"}
```

#### Database Fixture Pattern
```python
# tests/conftest.py
import pytest
from sqlmodel import create_engine, Session, SQLModel
from fastapi.testclient import TestClient

TEST_DATABASE_URL = "postgresql://localhost/test_db"

@pytest.fixture(scope="function")
def db_session():
    engine = create_engine(TEST_DATABASE_URL)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    SQLModel.metadata.drop_all(engine)

@pytest.fixture
def client(db_session):
    # Override get_db_session dependency
    from main import app
    app.dependency_overrides[get_db_session] = lambda: db_session
    return TestClient(app)
```

#### Multi-User Isolation Test Example
```python
# tests/test_isolation.py
def test_user_cannot_access_other_user_tasks(client, create_test_token):
    # User A creates task
    token_a = create_test_token("user-a")
    response = client.post(
        "/api/tasks",
        headers={"Authorization": f"Bearer {token_a}"},
        json={"title": "User A's task"}
    )
    task_id = response.json()["id"]

    # User B tries to access User A's task
    token_b = create_test_token("user-b")
    response = client.get(
        f"/api/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token_b}"}
    )
    assert response.status_code == 404  # Should not expose task existence
```

### References
- [FastAPI Testing Documentation](https://fastapi.tiangolo.com/tutorial/testing/)
- [pytest Documentation](https://docs.pytest.org/)
- [pytest-asyncio](https://pytest-asyncio.readthedocs.io/)

---

## Summary of Key Decisions

| Area | Decision | Primary Rationale |
|------|----------|------------------|
| JWT Claims | Use `sub` claim with HS256 | RFC 7519 standard, simpler than RS256 |
| Database | Async SQLModel with asyncpg | Better FastAPI integration, connection pooling |
| Sessions | FastAPI dependency injection | Clean, testable, follows framework patterns |
| Migrations | Alembic | Version control, rollback capability |
| CORS | Environment-based origins | Flexible for dev/staging/prod |
| Errors | HTTPException with global handler | Consistent, secure, frontend-friendly |
| Testing | pytest + TestClient + test DB | Standard, reliable, real DB behavior |
| JWT Mocking | Create tokens with test secret | Enables auth testing without external dependencies |

---

## Open Questions & Assumptions

### Assumptions Made
1. Better Auth uses standard JWT with `sub` claim (will validate with frontend team)
2. Neon database URL will be provided in expected format
3. Frontend expects HTTP 404 for both "not found" and "not authorized" (security best practice)
4. No WebSocket support needed initially (per OS-010)

### Questions for Frontend Team
1. What is the exact claim name for user ID in Better Auth JWT? (assuming `sub`)
2. What is the production frontend URL for CORS configuration?
3. Are there any specific error formats or status codes the frontend expects?
4. Does Better Auth handle token refresh automatically, or does backend need refresh endpoints?

### Next Steps
1. Validate JWT assumptions with frontend team before implementation
2. Obtain test BETTER_AUTH_SECRET for development
3. Set up Neon database and get DATABASE_URL
4. Create data-model.md with concrete Task schema
5. Generate OpenAPI contracts based on research findings

---

**Research Status**: ✅ Complete

**Validated By**: Backend planning phase

**Next Artifact**: data-model.md
