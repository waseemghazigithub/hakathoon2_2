# Implementation Plan: Full Backend + Frontend Integration

**Branch**: `1-backend-integration` | **Date**: 2026-02-07 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/1-backend-integration/spec.md`

**Note**: This plan follows the phased approach from the user's detailed planning principles, prioritizing authentication, database models, CRUD APIs, and continuous integration validation.

## Summary

Implement a production-grade FastAPI backend that integrates seamlessly with the existing Next.js frontend using Better Auth JWT authentication and Neon PostgreSQL database. The backend will provide secure, user-isolated task management through REST API endpoints, ensuring zero-defect operation and full frontend compatibility without requiring frontend code changes.

**Core Objectives**:
- JWT authentication & authorization with Better Auth integration
- SQLModel ORM with Neon PostgreSQL for data persistence
- Complete REST API for task CRUD operations
- User data isolation enforced at query level
- Production-grade error handling and validation
- CORS configuration for frontend integration
- Incremental validation at each phase

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: FastAPI 0.109+, SQLModel 0.0.14+, PyJWT 2.8+, psycopg2-binary 2.9+, python-dotenv 1.0+, uvicorn 0.27+
**Storage**: Neon PostgreSQL (serverless Postgres)
**Testing**: pytest 8.0+, httpx 0.26+ (FastAPI TestClient)
**Target Platform**: Linux/Windows server (Python ASGI deployment)
**Project Type**: Web application (backend only, integrates with existing Next.js frontend)
**Performance Goals**: <2 seconds response time for 95% of requests, support 1000+ concurrent users
**Constraints**: <200ms p95 latency for API calls, must use environment variables for all secrets, serverless-safe database connections
**Scale/Scope**: 10k+ users, 100k+ tasks, 6 REST endpoints, JWT-based authentication layer

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### ✅ Specs Are Law
- All implementation will follow specs/1-backend-integration/spec.md
- No undocumented features will be added
- Functional requirements FR-001 through FR-013 are binding

### ✅ Architecture First
- Implementation aligns with monorepo structure (backend/ directory)
- JWT-based authentication model is followed
- Layered architecture: routes → auth → services → models → db

### ✅ Authentication & Security Are Mandatory
- All endpoints require valid JWT authentication (FR-002)
- User identity derived ONLY from JWT token (FR-003)
- User data isolation enforced at query level (FR-007)
- Proper HTTP status codes for all error conditions (FR-008)

### ✅ API Contract Supremacy
- REST endpoints follow spec (FR-006): GET/POST/PUT/DELETE/PATCH /api/tasks
- JWT tokens in Authorization: Bearer format (A-005)
- Frontend compatibility maintained without code changes (FR-013)

### ✅ Database Ownership & Integrity
- SQLModel ORM used exclusively (FR-004)
- Task model with proper indexes on user_id and completed (FR-005)
- All queries filtered by authenticated user_id (FR-007)
- Timestamps managed automatically (FR-011)

### ✅ Monorepo & Spec-Kit Compliance
- Backend code in backend/ directory
- Frontend remains in frontend/ directory
- Clear separation of concerns maintained

### ✅ Change Management
- Any deviations from spec will require spec update first
- No silent divergence allowed

### ✅ Testing & Validation
- Acceptance criteria from spec will be validated
- Integration testing for auth and data isolation
- Frontend-backend contract compatibility verified

### Potential Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| JWT secret mismatch between frontend/backend | Medium | High | Establish shared secret handoff process in Phase 0 |
| Database connection pooling issues with Neon | Low | Medium | Use serverless-safe connection patterns from start |
| CORS misconfiguration blocking frontend | Medium | High | Configure and test CORS early in Phase 5 |
| User data leakage via incorrect query filters | Low | Critical | Enforce ownership checks in every query, add integration tests |
| Frontend expects different JSON schema | Medium | High | Document and validate API contracts in Phase 1 |

## Project Structure

### Documentation (this feature)

```text
specs/1-backend-integration/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
│   ├── openapi.yaml     # OpenAPI 3.0 specification
│   ├── tasks.schema.json # JSON schema for Task entity
│   └── errors.schema.json # Error response schemas
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── main.py              # FastAPI app entry point, CORS, route registration
├── db.py                # Database engine, session dependency
├── models.py            # SQLModel Task model with indexes
├── auth.py              # JWT verification, get_current_user dependency
├── schemas.py           # Pydantic request/response schemas
├── routes/
│   ├── __init__.py
│   └── tasks.py         # Task CRUD route handlers
├── core/
│   ├── __init__.py
│   └── config.py        # Environment config loader
├── .env.example         # Example environment variables (NO SECRETS)
└── tests/
    ├── __init__.py
    ├── test_auth.py     # JWT validation tests
    ├── test_tasks.py    # Task CRUD endpoint tests
    └── test_isolation.py # Multi-user data isolation tests

frontend/
└── [existing Next.js application - NO CHANGES REQUIRED]

.gitignore               # MUST include .env
```

**Structure Decision**: Web application structure (Option 2) selected. Backend is a standalone FastAPI application in the backend/ directory, integrating with the existing Next.js frontend in frontend/. Clear separation allows independent deployment and testing.

## Complexity Tracking

> No constitution violations detected. Implementation follows all architectural principles and security requirements.

## Phase 0: Outline & Research

### Objective
Resolve all technical unknowns and establish best practices before implementation begins. Document all architectural decisions with rationales.

### Research Tasks

1. **JWT Token Structure from Better Auth**
   - Investigate Better Auth JWT token format
   - Identify user identifier claim (sub vs user_id vs id)
   - Document token expiration and refresh patterns
   - Determine signature algorithm (HS256 vs RS256)

2. **Neon PostgreSQL Connection Patterns**
   - Research serverless-safe connection patterns
   - Investigate connection pooling for SQLModel + Neon
   - Document environment variable format for DATABASE_URL
   - Evaluate pgbouncer compatibility if needed

3. **FastAPI + SQLModel Integration Best Practices**
   - Research dependency injection patterns for database sessions
   - Investigate async vs sync SQLModel with FastAPI
   - Document migration strategy (Alembic vs SQLModel.metadata.create_all)
   - Evaluate proper shutdown/cleanup for database connections

4. **CORS Configuration for Next.js Frontend**
   - Identify frontend origin (localhost:3000 for dev, production domain)
   - Document required headers (Authorization, Content-Type)
   - Investigate credentials and preflight request handling
   - Determine if WebSocket support needed (out of scope per OS-010)

5. **Error Handling Patterns**
   - Research FastAPI exception handlers
   - Document standard error response format for frontend consumption
   - Investigate logging best practices (no sensitive data in logs)
   - Evaluate HTTPException vs custom exception classes

6. **Testing Strategy**
   - Research FastAPI TestClient patterns
   - Investigate JWT mocking for tests
   - Document database fixture patterns (test DB vs in-memory)
   - Evaluate integration test approaches for multi-user isolation

### Output
All research findings will be consolidated in `research.md` following the format:
- Decision: [what was chosen]
- Rationale: [why chosen]
- Alternatives considered: [what else evaluated]
- References: [links to docs, examples]

## Phase 1: Design & Contracts

### Prerequisites
- `research.md` complete with all unknowns resolved
- JWT token format documented
- Database connection pattern selected

### Deliverables

#### 1.1 Data Model (`data-model.md`)

**Task Entity**:
```
Task
├── id: int (PK, auto-increment)
├── user_id: str (indexed, not null, FK to User identity from JWT)
├── title: str (1-200 chars, not null)
├── description: str (nullable, text)
├── completed: bool (default: false, indexed)
├── created_at: datetime (auto, not null)
└── updated_at: datetime (auto-update, not null)

Indexes:
- idx_task_user_id ON user_id
- idx_task_completed ON completed
- composite idx_task_user_completed ON (user_id, completed) for filtered queries

Constraints:
- title length: 1-200 characters
- user_id must match authenticated JWT user
- timestamps are UTC
```

**User Entity** (conceptual, not stored):
```
User (represented only in JWT)
├── sub/user_id: str (unique identifier from JWT)
└── 0 or more Tasks (one-to-many relationship)
```

**State Transitions**:
```
Task.completed: false → true (via PATCH /api/tasks/{id}/complete)
Task.completed: true → false (via PATCH /api/tasks/{id}/complete)
```

**Validation Rules**:
- Title: required, 1-200 characters, no leading/trailing whitespace
- Description: optional, max 10000 characters
- Completed: boolean only (no null)
- Timestamps: managed by system, cannot be set by user
- User ownership: immutable after creation

#### 1.2 API Contracts (`contracts/`)

**Base URL**: `/api`

**Authentication**: All endpoints require `Authorization: Bearer <jwt_token>` header

**Endpoints**:

1. **GET /api/tasks**
   - Query params: `status` (optional: "completed" | "active")
   - Response: `200 OK` with `Task[]`
   - Errors: `401 Unauthorized`

2. **POST /api/tasks**
   - Body: `CreateTaskRequest { title: str, description?: str }`
   - Response: `201 Created` with `Task`
   - Errors: `400 Bad Request`, `401 Unauthorized`

3. **GET /api/tasks/{id}**
   - Path param: `id` (int)
   - Response: `200 OK` with `Task`
   - Errors: `401 Unauthorized`, `404 Not Found`

4. **PUT /api/tasks/{id}**
   - Path param: `id` (int)
   - Body: `UpdateTaskRequest { title?: str, description?: str, completed?: bool }`
   - Response: `200 OK` with `Task`
   - Errors: `400 Bad Request`, `401 Unauthorized`, `404 Not Found`

5. **DELETE /api/tasks/{id}**
   - Path param: `id` (int)
   - Response: `204 No Content`
   - Errors: `401 Unauthorized`, `404 Not Found`

6. **PATCH /api/tasks/{id}/complete**
   - Path param: `id` (int)
   - Response: `200 OK` with `Task` (completed toggled)
   - Errors: `401 Unauthorized`, `404 Not Found`

**Standard Error Response**:
```json
{
  "detail": "Human-readable error message",
  "status_code": 400,
  "error_type": "validation_error"
}
```

**OpenAPI Specification**: Full OpenAPI 3.0 spec in `contracts/openapi.yaml`

#### 1.3 Quickstart Guide (`quickstart.md`)

Development setup instructions:
1. Prerequisites (Python 3.11+, Neon account)
2. Environment setup (.env configuration)
3. Dependency installation (pip/poetry/uv)
4. Database initialization
5. Running the dev server
6. Testing with curl/Postman
7. Integration with frontend

#### 1.4 Agent Context Update

Run: `.specify/scripts/powershell/update-agent-context.ps1 -AgentType claude`

This will update the appropriate agent context file (CLAUDE.md) with:
- FastAPI as backend framework
- SQLModel for ORM
- PyJWT for authentication
- Neon PostgreSQL for storage
- pytest for testing

## Phase 2: Implementation Phases (Overview)

*Note: Detailed tasks will be generated by `/sp.tasks` command after this plan is approved.*

### Phase Summary

**Phase 0: Pre-Implementation Safety & Setup** (Security First)
- Secrets rotation and .env configuration
- Project structure scaffolding
- .gitignore validation

**Phase 1: Core Infrastructure** (Foundation)
- Configuration loader with validation
- Database engine and session management
- Connection testing

**Phase 2: Authentication & Security Layer** (Auth First)
- JWT verification implementation
- get_current_user dependency
- Token validation testing

**Phase 3: Database Models & Schemas** (Data Layer)
- SQLModel Task model with indexes
- Pydantic request/response schemas
- Validation rules

**Phase 4: Task CRUD Routes** (API Layer)
- Route registration
- GET /api/tasks (list with filtering)
- POST /api/tasks (create)
- GET /api/tasks/{id} (retrieve)
- PUT /api/tasks/{id} (update)
- DELETE /api/tasks/{id} (delete)
- PATCH /api/tasks/{id}/complete (toggle)
- Ownership enforcement in all routes

**Phase 5: Frontend Integration & CORS** (Integration)
- CORS configuration
- JSON contract validation
- Error response standardization

**Phase 6: Integration Validation** (Verification)
- Manual integration testing with frontend
- Multi-user data isolation testing
- End-to-end workflow validation

**Phase 7: Hardening & Production Readiness** (Polish)
- Error handling standardization
- Logging implementation
- Performance validation
- Security audit

**Phase 8: Completion & Sign-Off** (Delivery)
- Spec compliance review
- Frontend contract freeze
- Documentation finalization

### Risk Management

**Critical Success Factors**:
1. JWT secret must be shared securely between frontend and backend
2. All database queries must filter by authenticated user_id
3. Frontend must work without any code changes
4. Data isolation must be 100% effective

**Validation Gates**:
- After Phase 2: Auth working, can validate JWT from frontend
- After Phase 4: All CRUD operations working with proper isolation
- After Phase 5: Frontend can perform all operations
- After Phase 6: Multi-user testing passes

**Rollback Points**:
- If JWT integration fails: review Better Auth token format
- If CORS fails: verify frontend origin configuration
- If data isolation fails: audit all query filters
- If performance issues: review database indexes and connection pooling

## Next Steps

1. **Review and approve this plan**
2. **Generate detailed tasks**: Run `/sp.tasks` to break down implementation phases into specific, testable tasks
3. **Begin Phase 0 Research**: Create `research.md` by investigating unknowns listed above
4. **Generate Phase 1 artifacts**: Create data-model.md, contracts/, and quickstart.md
5. **Update agent context**: Run update script to inform Claude Code of tech stack
6. **Execute implementation**: Follow task list in dependency order

## Appendix: Key Decisions

### Why FastAPI?
- High performance async framework
- Built-in OpenAPI documentation
- Excellent dependency injection for auth
- Strong type hints with Pydantic
- Large ecosystem and community

### Why SQLModel?
- Combines SQLAlchemy and Pydantic
- Type-safe ORM with IDE support
- Seamless FastAPI integration
- Supports migrations via Alembic
- Neon PostgreSQL compatible

### Why JWT Authentication?
- Stateless, scalable authentication
- Frontend already uses Better Auth with JWT
- No session management needed
- Easy to validate and decode
- Standard Authorization: Bearer pattern

### Why User Data Isolation at Query Level?
- Defense in depth: prevents logic bugs from exposing data
- Performance: indexed queries are fast
- Simplicity: every query has same pattern
- Auditability: clear ownership model
- Security: minimizes attack surface

---

**Plan Status**: ✅ Ready for Phase 0 Research & Phase 1 Design

**Constitution Compliance**: ✅ All gates passed

**Next Command**: `/sp.tasks` (after Phase 0 research and Phase 1 design are complete)
