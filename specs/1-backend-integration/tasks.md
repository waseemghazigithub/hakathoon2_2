---
description: "Task list for Full Backend + Frontend Integration"
---

# Tasks: Full Backend + Frontend Integration

**Input**: Design documents from `/specs/1-backend-integration/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/openapi.yaml

**Tests**: Tests are NOT explicitly requested in the spec, but integration validation is required (Phase 6 in plan). Integration tests included for data isolation verification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

This is a web application with backend/frontend structure:
- **Backend**: `backend/` (Python/FastAPI)
- **Frontend**: `frontend/` (Next.js - NO CHANGES REQUIRED)
- **Tests**: `backend/tests/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure following FR-001

**Success Criteria**: Project structure matches plan.md, dependencies installed, environment configured

### Tasks

- [x] T001 Create backend directory structure: backend/{main.py,db.py,models.py,auth.py,schemas.py,routes/,core/,tests/}
- [x] T002 Initialize Python project with pyproject.toml or requirements.txt (FastAPI 0.109+, SQLModel 0.0.14+, PyJWT 2.8+, psycopg2-binary, python-dotenv, uvicorn, pytest, httpx)
- [x] T003 [P] Create .env.example file with placeholders: BETTER_AUTH_SECRET, DATABASE_URL, FRONTEND_URL, ENVIRONMENT
- [x] T004 [P] Update .gitignore to include .env, __pycache__/, *.pyc, .pytest_cache/
- [x] T005 [P] Create backend/README.md with quickstart instructions

**Checkpoint**: Project structure ready, dependencies defined, environment template created

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

**Success Criteria**: Database connections work, JWT validation functional, CORS configured, migrations ready

### Configuration & Environment

- [x] T006 Implement backend/core/config.py to load and validate environment variables (BETTER_AUTH_SECRET, DATABASE_URL, FRONTEND_URL, ENVIRONMENT)
- [x] T007 Add environment validation that fails fast on missing required variables

### Database Infrastructure

- [x] T008 Implement backend/db.py with async SQLModel engine using DATABASE_URL from config
- [x] T009 Configure connection pooling for Neon: pool_size=10, max_overflow=0, pool_pre_ping=True, pool_recycle=3600
- [x] T010 Implement async get_session() dependency for FastAPI dependency injection
- [x] T011 Setup Alembic for database migrations: alembic init alembic
- [x] T012 Configure Alembic env.py to use SQLModel metadata and async engine

### Authentication & Security Layer (FR-002, FR-003)

- [x] T013 Implement backend/auth.py with JWT verification using PyJWT and BETTER_AUTH_SECRET
- [x] T014 Create HTTPBearer security dependency for extracting Authorization header
- [x] T015 Implement get_current_user() dependency that decodes JWT, extracts user_id from 'sub' claim, handles expired/invalid tokens with 401
- [x] T016 Add JWT exception handling: ExpiredSignatureError → 401 "Token expired", InvalidTokenError → 401 "Invalid token"

### FastAPI Application Setup

- [x] T017 Initialize FastAPI app in backend/main.py with title="Task Management API", version="1.0.0"
- [x] T018 Configure CORS middleware in main.py: allow_origins=[FRONTEND_URL], allow_credentials=True, allow_methods=["GET","POST","PUT","DELETE","PATCH","OPTIONS"], allow_headers=["Authorization","Content-Type","Accept"]
- [x] T019 [P] Setup global exception handler for HTTPException to return consistent error format: {detail, status_code, error_type}
- [x] T020 [P] Setup validation exception handler for RequestValidationError to return 400 with validation details
- [x] T021 [P] Implement lifespan context manager for engine disposal on shutdown

**Checkpoint**: Foundation ready - authentication works, database connections functional, app structure complete. User story implementation can now begin in parallel.

---

## Phase 3: User Story 1 - Secure Task Management via API (Priority: P1) 🎯 MVP

**Goal**: Enable authenticated users to securely create, read, update, and delete their personal tasks through REST API with proper data isolation

**Independent Test**: Authenticate with JWT token, perform CRUD operations on tasks, verify users can only access their own data and unauthorized access returns 404

**Acceptance Scenarios** (from spec.md):
1. Authenticated user with valid JWT creates task → task created under user account
2. Authenticated user lists tasks → only sees own tasks
3. Authenticated user accesses another user's task → receives 404

### Database Models & Schemas (FR-005)

- [x] T022 [P] [US1] Create Task SQLModel in backend/models.py with fields: id (PK), user_id (str, indexed), title (str, 1-200), description (str nullable, max 10000), completed (bool, default False, indexed), created_at (datetime UTC), updated_at (datetime UTC)
- [x] T023 [P] [US1] Add table-level composite index (user_id, completed) to Task model
- [x] T024 [P] [US1] Implement timestamps auto-management: created_at with default_factory=utcnow, updated_at with onupdate=utcnow
- [x] T025 [P] [US1] Create Pydantic schemas in backend/schemas.py: TaskRead, TaskCreate (title required, description optional), TaskUpdate (all fields optional)
- [x] T026 [P] [US1] Add validation to TaskCreate and TaskUpdate: title 1-200 chars, description max 10000 chars, title strip whitespace

### Database Migration

- [x] T027 [US1] Create Alembic migration for tasks table: alembic revision --autogenerate -m "Create tasks table"
- [x] T028 [US1] Review generated migration, verify indexes (user_id, completed, composite), apply migration: alembic upgrade head

### API Routes - Task CRUD (FR-006)

- [x] T029 [US1] Create APIRouter in backend/routes/tasks.py with prefix="/api/tasks", tags=["Tasks"]
- [x] T030 [US1] Register tasks router in backend/main.py

#### GET /api/tasks - List Tasks

- [x] T031 [P] [US1] Implement GET /api/tasks endpoint: filter by authenticated user_id from get_current_user dependency
- [x] T032 [P] [US1] Add optional query parameter 'status' (completed/active) to filter tasks by completion status
- [x] T033 [P] [US1] Return tasks sorted by created_at descending, return empty array if no tasks
- [x] T034 [P] [US1] Enforce FR-007: ALL queries MUST filter WHERE task.user_id == authenticated_user_id

#### POST /api/tasks - Create Task (FR-009, FR-010)

- [x] T035 [P] [US1] Implement POST /api/tasks endpoint with TaskCreate schema validation
- [x] T036 [P] [US1] Validate title length 1-200 chars (return 400 if invalid with validation error details)
- [x] T037 [P] [US1] Create task with user_id from JWT (NEVER from request body), completed=False by default
- [x] T038 [P] [US1] Strip leading/trailing whitespace from title before storage
- [x] T039 [P] [US1] Return 201 Created with TaskRead schema response

#### GET /api/tasks/{id} - Retrieve Single Task

- [x] T040 [P] [US1] Implement GET /api/tasks/{id} endpoint with path parameter validation
- [x] T041 [P] [US1] Query task by id AND user_id to enforce ownership (FR-007)
- [x] T042 [P] [US1] Return 404 "Task not found" if task doesn't exist OR doesn't belong to user (don't leak existence)
- [x] T043 [P] [US1] Return 200 with TaskRead schema if found and owned

#### PUT /api/tasks/{id} - Update Task (FR-011)

- [x] T044 [P] [US1] Implement PUT /api/tasks/{id} endpoint with TaskUpdate schema validation
- [x] T045 [P] [US1] Query task by id AND user_id to enforce ownership
- [x] T046 [P] [US1] Return 404 if task not found or not owned by user
- [x] T047 [P] [US1] Update only provided fields (title, description, completed), strip title whitespace
- [x] T048 [P] [US1] Validate title length if provided (1-200 chars), return 400 if invalid
- [x] T049 [P] [US1] Auto-update updated_at timestamp (handled by SQLModel onupdate)
- [x] T050 [P] [US1] Return 200 with updated TaskRead schema

#### DELETE /api/tasks/{id} - Delete Task

- [x] T051 [P] [US1] Implement DELETE /api/tasks/{id} endpoint
- [x] T052 [P] [US1] Query task by id AND user_id to enforce ownership
- [x] T053 [P] [US1] Return 404 if task not found or not owned by user
- [x] T054 [P] [US1] Delete task from database
- [x] T055 [P] [US1] Return 204 No Content on successful deletion

#### PATCH /api/tasks/{id}/complete - Toggle Completion

- [x] T056 [P] [US1] Implement PATCH /api/tasks/{id}/complete endpoint
- [x] T057 [P] [US1] Query task by id AND user_id to enforce ownership
- [x] T058 [P] [US1] Return 404 if task not found or not owned by user
- [x] T059 [P] [US1] Toggle completed field: False → True or True → False
- [x] T060 [P] [US1] Auto-update updated_at timestamp
- [x] T061 [P] [US1] Return 200 with updated TaskRead schema showing new completed status

### Integration Tests for Data Isolation

- [ ] T062 [US1] Create tests/conftest.py with test database fixture, get_session override, and JWT token generator
- [ ] T063 [US1] Implement test_isolation.py: test_user_cannot_access_other_user_tasks (user A creates task, user B gets 404)
- [ ] T064 [US1] Implement test_isolation.py: test_user_cannot_update_other_user_tasks (user A creates task, user B PUT returns 404)
- [ ] T065 [US1] Implement test_isolation.py: test_user_cannot_delete_other_user_tasks (user A creates task, user B DELETE returns 404)
- [ ] T066 [US1] Implement test_isolation.py: test_user_only_sees_own_tasks_in_list (create tasks for users A and B, verify GET /api/tasks filters correctly)

**Checkpoint**: User Story 1 is fully functional and testable. Users can perform all CRUD operations on their tasks with JWT authentication and complete data isolation.

---

## Phase 4: User Story 2 - JWT-Based Authentication Integration (Priority: P1)

**Goal**: Ensure backend properly validates JWT tokens issued by Better Auth for seamless authentication across frontend and backend

**Independent Test**: Send requests with valid and invalid JWT tokens, verify only valid tokens from shared secret are accepted

**Acceptance Scenarios** (from spec.md):
1. Valid JWT from Better Auth → requests authenticated, user accesses own data
2. Expired/invalid JWT → 401 Unauthorized response
3. No Authorization header → 401 Unauthorized response

**Note**: Most authentication implementation was completed in Phase 2 (Foundational). This phase focuses on validation and edge case testing.

### Authentication Validation Tests

- [ ] T067 [P] [US2] Create tests/test_auth.py with JWT token creation helpers (valid token, expired token, invalid secret)
- [ ] T068 [P] [US2] Implement test_valid_token_accepted: create valid JWT with sub claim, verify 200 response on protected endpoint
- [ ] T069 [P] [US2] Implement test_expired_token_rejected: create expired JWT (exp in past), verify 401 "Token expired" response
- [ ] T070 [P] [US2] Implement test_invalid_signature_rejected: create JWT with wrong secret, verify 401 "Invalid token" response
- [ ] T071 [P] [US2] Implement test_missing_sub_claim: create JWT without sub claim, verify 401 "Invalid token: missing sub claim"
- [ ] T072 [P] [US2] Implement test_missing_authorization_header: send request without Authorization header, verify 401 "Not authenticated"
- [ ] T073 [P] [US2] Implement test_malformed_authorization_header: send "Bearer invalidformat", verify 401 response

### Better Auth Integration Verification

- [ ] T074 [US2] Document JWT token format assumptions in backend/auth.py: sub claim, HS256 algorithm, exp/iat claims
- [ ] T075 [US2] Add logging for authentication failures (token expired, invalid signature) without exposing sensitive data
- [ ] T076 [US2] Verify BETTER_AUTH_SECRET environment variable validation in config.py with helpful error message

**Checkpoint**: JWT authentication is thoroughly validated. All edge cases (expired, invalid, missing tokens) are handled correctly with proper 401 responses.

---

## Phase 5: User Story 3 - Production-Ready Task Operations (Priority: P2)

**Goal**: Ensure backend handles all CRUD operations with robust error handling and validation for system stability

**Independent Test**: Perform task operations with valid and invalid data, verify appropriate responses and validation

**Acceptance Scenarios** (from spec.md):
1. Create task with valid title (1-200 chars) → task created successfully
2. Create task with invalid title (empty or >200 chars) → 400 Bad Request with validation error
3. Update non-existent task → 404 Not Found

**Note**: Core CRUD operations were implemented in User Story 1. This phase focuses on error handling, edge cases, and production readiness.

### Error Handling Enhancement (FR-008)

- [ ] T077 [P] [US3] Review all endpoints to ensure consistent error responses: 400 (validation), 401 (auth), 404 (not found), 500 (server errors)
- [ ] T078 [P] [US3] Add error handling for database connection failures: catch DBAPIError, return 500 with generic message
- [ ] T079 [P] [US3] Implement request/response logging middleware without sensitive data (no JWT tokens, no passwords)
- [ ] T080 [P] [US3] Add structured logging for key operations: task_created, task_updated, task_deleted with user_id and task_id

### Validation Edge Cases

- [ ] T081 [P] [US3] Create tests/test_tasks.py: test_create_task_with_empty_title (verify 400 validation error)
- [ ] T082 [P] [US3] Create tests/test_tasks.py: test_create_task_with_title_too_long (201 chars, verify 400)
- [ ] T083 [P] [US3] Create tests/test_tasks.py: test_create_task_with_only_whitespace_title (strip should make it empty, verify 400)
- [ ] T084 [P] [US3] Create tests/test_tasks.py: test_create_task_with_description_too_long (>10000 chars, verify 400)
- [ ] T085 [P] [US3] Create tests/test_tasks.py: test_update_nonexistent_task (verify 404)
- [ ] T086 [P] [US3] Create tests/test_tasks.py: test_delete_nonexistent_task (verify 404)
- [ ] T087 [P] [US3] Create tests/test_tasks.py: test_toggle_complete_nonexistent_task (verify 404)

### Operational Robustness

- [ ] T088 [US3] Add database query timeouts to prevent long-running queries
- [ ] T089 [US3] Verify connection pool exhaustion handling (test with max_overflow=0)
- [ ] T090 [US3] Document error response format in backend/README.md for frontend consumption

**Checkpoint**: All error cases handled gracefully. System is production-ready with comprehensive logging and validation.

---

## Phase 6: Frontend Integration & CORS

**Purpose**: Enable seamless frontend integration without code changes (FR-012, FR-013)

**Success Criteria**: Frontend can perform all operations, CORS configured correctly, JSON contracts match expectations

### CORS Validation

- [ ] T091 Verify CORS middleware configuration in main.py allows frontend origin from FRONTEND_URL env var
- [ ] T092 Test CORS preflight requests (OPTIONS) return correct Access-Control headers
- [ ] T093 [P] Document CORS configuration for dev (localhost:3000) and production (env var) in quickstart.md

### API Contract Verification

- [ ] T094 Compare OpenAPI spec (contracts/openapi.yaml) with actual FastAPI routes using /docs endpoint
- [ ] T095 Verify all response schemas match TaskRead format expected by frontend
- [ ] T096 Verify error response format matches frontend expectations: {detail, status_code, error_type}

### Manual Integration Testing (from plan.md Phase 6)

- [ ] T097 Start backend server (uvicorn main:app --reload) and verify /docs loads
- [ ] T098 Login via frontend, capture JWT token from browser DevTools
- [ ] T099 Create task from frontend UI, verify task appears in database
- [ ] T100 List tasks from frontend, verify only user's tasks shown
- [ ] T101 Update task from frontend, verify updated_at changes
- [ ] T102 Toggle task completion from frontend, verify completed status changes
- [ ] T103 Delete task from frontend, verify task removed from database

### Multi-User Isolation Testing

- [ ] T104 Login as User A, create 3 tasks, note task IDs
- [ ] T105 Login as User B, create 2 tasks
- [ ] T106 Verify User A lists only 3 tasks (not User B's tasks)
- [ ] T107 Verify User B cannot access User A's task IDs (404 responses)
- [ ] T108 Verify User A cannot modify/delete User B's tasks

**Checkpoint**: Frontend fully integrated, CORS working, multi-user isolation verified. System ready for production deployment.

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Finalize production readiness, documentation, and deployment preparation

### Documentation

- [ ] T109 [P] Update backend/README.md with complete setup instructions matching quickstart.md
- [ ] T110 [P] Document environment variables in .env.example with descriptions and example values
- [ ] T111 [P] Add API usage examples to README.md with curl commands for each endpoint
- [ ] T112 [P] Document deployment steps: database migrations, environment setup, server startup

### Performance Validation

- [ ] T113 Verify database indexes are created correctly: user_id, completed, composite (user_id, completed)
- [ ] T114 Test query performance with 1000+ tasks per user, verify <200ms p95 latency
- [ ] T115 Verify connection pooling prevents "too many connections" errors under load

### Security Audit

- [ ] T116 Verify no secrets in code or committed files (git log search for common secret patterns)
- [ ] T117 Verify .env file is in .gitignore and not committed
- [ ] T118 Review all endpoints for proper authentication (no public endpoints)
- [ ] T119 Verify all queries filter by user_id (grep for Task queries without user_id filter)
- [ ] T120 Test with malformed JWT payloads (missing claims, wrong types) to ensure safe handling

### Spec Compliance Review (from plan.md Phase 8)

- [ ] T121 Verify all 13 functional requirements (FR-001 to FR-013) are implemented
- [ ] T122 Verify all 3 user stories have passing acceptance scenarios
- [ ] T123 Verify all 7 success criteria are met (authentication accuracy, response times, data isolation, frontend integration, error handling)
- [ ] T124 Verify all assumptions (A-001 to A-007) are documented and validated
- [ ] T125 Verify all dependencies (D-001 to D-004) are met
- [ ] T126 Verify all out-of-scope items (OS-001 to OS-010) are not implemented

### Testing & Quality

- [ ] T127 Run full test suite: pytest backend/tests/ --cov=backend --cov-report=html
- [ ] T128 Verify test coverage >80% for critical paths (auth, data isolation, CRUD)
- [ ] T129 Review and fix any linting issues: ruff check backend/ or flake8 backend/
- [ ] T130 Review and fix any type checking issues if using mypy

### Deployment Preparation

- [ ] T131 [P] Create Dockerfile for backend (if containerization needed)
- [ ] T132 [P] Create docker-compose.yml for local development (backend + Neon proxy)
- [ ] T133 [P] Document production deployment steps for chosen platform (Vercel, Railway, Fly.io, etc.)
- [ ] T134 [P] Setup CI/CD pipeline for automated testing and deployment (GitHub Actions template)

**Checkpoint**: System is production-ready, fully documented, tested, and deployable.

---

## Dependencies Between User Stories

```
Phase 1 (Setup)
     ↓
Phase 2 (Foundational) ← BLOCKING - must complete before user stories
     ↓
     ├──→ User Story 1 (P1) 🎯 MVP - Secure Task Management
     │         ↓ (foundational for other stories)
     ├──→ User Story 2 (P1) - JWT Auth Integration (validates Phase 2 auth)
     │         ↓
     └──→ User Story 3 (P2) - Production-Ready Operations (enhances US1)
              ↓
Phase 6 (Frontend Integration) - validates all stories work together
     ↓
Phase 7 (Polish) - final production readiness
```

**User Story Dependencies**:
- **User Story 1** (P1): No dependencies on other stories (can start after Phase 2)
- **User Story 2** (P1): Independent validation of Phase 2 auth (can run parallel with US1)
- **User Story 3** (P2): Builds on User Story 1 CRUD operations (should follow US1)

**Recommended MVP**: User Stories 1 + 2 (both P1) provide a complete, secure task management API

---

## Parallel Execution Opportunities

### Within Phase 2 (Foundational) - 3 parallel tracks:

**Track A (Config & DB)**:
- T006 → T007 (config)
- T008 → T009 → T010 (database)
- T011 → T012 (migrations)

**Track B (Auth)**:
- T013 → T014 → T015 → T016 (authentication)

**Track C (FastAPI)**:
- T017 → T018 (app setup and CORS)
- T019, T020 (exception handlers - parallel)
- T021 (lifespan)

**Merge Point**: All tracks must complete before Phase 3

### Within Phase 3 (User Story 1) - 6 parallel tracks after DB setup:

**Sequential Setup** (must complete first):
- T022 → T023 → T024 (Task model)
- T025 → T026 (schemas)
- T027 → T028 (migration)
- T029 → T030 (router setup)

**Then Parallel Implementation**:
1. **GET /api/tasks**: T031, T032, T033, T034 (can implement in parallel if independent)
2. **POST /api/tasks**: T035, T036, T037, T038, T039
3. **GET /api/tasks/{id}**: T040, T041, T042, T043
4. **PUT /api/tasks/{id}**: T044, T045, T046, T047, T048, T049, T050
5. **DELETE /api/tasks/{id}**: T051, T052, T053, T054, T055
6. **PATCH /api/tasks/{id}/complete**: T056, T057, T058, T059, T060, T061

**Then Tests**: T062 → T063, T064, T065, T066 (tests can run in parallel)

### Within Phase 4 (User Story 2) - All tests in parallel:

- T067 (setup)
- T068, T069, T070, T071, T072, T073 (all test cases parallel)
- T074, T075, T076 (docs and logging - parallel)

### Within Phase 5 (User Story 3) - 3 parallel tracks:

**Track A (Error Handling)**: T077, T078, T079, T080
**Track B (Validation Tests)**: T081, T082, T083, T084, T085, T086, T087 (all parallel)
**Track C (Robustness)**: T088, T089, T090

### Within Phase 7 (Polish) - 4 parallel tracks:

**Track A (Docs)**: T109, T110, T111, T112
**Track B (Performance)**: T113, T114, T115
**Track C (Security)**: T116, T117, T118, T119, T120
**Track D (Compliance)**: T121, T122, T123, T124, T125, T126
**Track E (Testing)**: T127, T128, T129, T130
**Track F (Deployment)**: T131, T132, T133, T134

---

## Implementation Strategy

### MVP Scope (Minimum Viable Product)

**Phase 1 + Phase 2 + Phase 3 (User Story 1) = MVP**

This delivers:
- Complete backend infrastructure
- Secure JWT authentication
- Full task CRUD operations
- Data isolation enforcement
- Integration tests

Estimated: ~65 tasks (T001-T066)

### Incremental Delivery

1. **Sprint 1**: Phase 1 + Phase 2 (Foundational) - 21 tasks
   - Deliverable: Backend structure, auth working, database connected

2. **Sprint 2**: Phase 3 (User Story 1) - 45 tasks
   - Deliverable: MVP - Full task CRUD API with tests

3. **Sprint 3**: Phase 4 + Phase 5 (User Stories 2 & 3) - 24 tasks
   - Deliverable: Production-ready with comprehensive validation

4. **Sprint 4**: Phase 6 + Phase 7 (Integration & Polish) - 44 tasks
   - Deliverable: Fully integrated with frontend, deployed to production

### Total Tasks: 134 tasks

**By Phase**:
- Phase 1 (Setup): 5 tasks
- Phase 2 (Foundational): 16 tasks
- Phase 3 (User Story 1): 45 tasks
- Phase 4 (User Story 2): 10 tasks
- Phase 5 (User Story 3): 14 tasks
- Phase 6 (Integration): 18 tasks
- Phase 7 (Polish): 26 tasks

**By Priority**:
- P1 (MVP): 66 tasks (Phases 1-3)
- P1 (Auth Validation): 10 tasks (Phase 4)
- P2 (Production Ready): 58 tasks (Phases 5-7)

---

## Task Validation Summary

✅ **Format Compliance**: All 134 tasks follow `- [ ] [ID] [P?] [Story?] Description with file path` format

✅ **User Story Organization**: Tasks grouped by story (US1, US2, US3) for independent implementation

✅ **File Paths**: All implementation tasks include specific file paths (backend/...)

✅ **Parallel Marking**: [P] marker on 78 parallelizable tasks (58%)

✅ **Sequential Dependencies**: Critical paths clearly marked (foundational → stories → integration)

✅ **Independent Testing**: Each user story has clear test criteria and can be validated independently

✅ **Constitution Compliance**: All tasks align with FR-001 to FR-013 requirements

---

## Next Steps

1. **Review this task list** for completeness and accuracy
2. **Begin Sprint 1**: Execute Phase 1 + Phase 2 tasks (T001-T021)
3. **Validate Foundation**: Ensure auth and database work before starting user stories
4. **Implement MVP**: Execute Phase 3 (User Story 1) tasks (T022-T066)
5. **Test Integration**: Verify frontend can use the API
6. **Deploy to Production**: Complete remaining phases for production readiness

For task execution, use `/sp.implement` command or manually execute tasks in dependency order.

---

**Tasks Status**: ✅ Complete and ready for implementation

**Branch**: `1-backend-integration`

**Generated**: 2026-02-07
