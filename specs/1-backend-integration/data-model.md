# Data Model: Backend Integration

**Feature**: Full Backend + Frontend Integration
**Branch**: `1-backend-integration`
**Date**: 2026-02-07
**Status**: Final

## Overview

This document defines the data model for the FastAPI backend, including entities, relationships, validation rules, and state transitions. The model is derived from functional requirements FR-005 and user stories in the feature specification.

---

## Entity: Task

### Purpose
Represents a user's task with title, description, completion status, and ownership tracking. Tasks are user-isolated and support basic CRUD operations.

### Schema

| Field | Type | Constraints | Default | Description |
|-------|------|-------------|---------|-------------|
| `id` | `int` | Primary Key, Auto-increment | Auto | Unique task identifier |
| `user_id` | `str` | Not Null, Indexed, Length(1-255) | - | Owner's user ID from JWT `sub` claim |
| `title` | `str` | Not Null, Length(1-200) | - | Task title/summary |
| `description` | `str` | Nullable, Length(0-10000) | `null` | Optional detailed description |
| `completed` | `bool` | Not Null, Indexed | `false` | Completion status |
| `created_at` | `datetime` | Not Null, Timezone-aware (UTC) | `now()` | Task creation timestamp |
| `updated_at` | `datetime` | Not Null, Timezone-aware (UTC) | `now()` | Last modification timestamp |

### Indexes

```sql
-- Single-column indexes
CREATE INDEX idx_task_user_id ON tasks(user_id);
CREATE INDEX idx_task_completed ON tasks(completed);

-- Composite index for filtered queries
CREATE INDEX idx_task_user_completed ON tasks(user_id, completed);
```

**Rationale**:
- `idx_task_user_id`: Enables fast queries filtering by authenticated user
- `idx_task_completed`: Supports filtering by completion status
- `idx_task_user_completed`: Optimizes common query pattern (user's completed/active tasks)

### Validation Rules

#### Title
- **Required**: Must be provided (not null, not empty string)
- **Length**: 1-200 characters (inclusive)
- **Format**: Any Unicode string
- **Trimming**: Leading/trailing whitespace should be trimmed before storage
- **Examples**:
  - Valid: "Buy groceries", "Meeting at 3pm", "Review PR #42"
  - Invalid: "" (empty), "   " (only whitespace), "A" * 201 (too long)

#### Description
- **Optional**: Can be null or empty string
- **Length**: 0-10000 characters (inclusive)
- **Format**: Any Unicode string, supports multi-line text
- **Trimming**: No automatic trimming (preserve user formatting)

#### Completed
- **Required**: Must be boolean (true/false)
- **No Null**: Cannot be null (always false or true)
- **Default**: `false` for new tasks

#### User ID
- **Required**: Must be extracted from JWT `sub` claim
- **Immutable**: Cannot be changed after task creation
- **Format**: String matching JWT `sub` claim format (typically UUID or integer string)
- **Never from Request**: Must NEVER be accepted from request body, query params, or path params

#### Timestamps
- **Timezone**: All timestamps stored as UTC
- **Managed by System**: Cannot be set or modified by users
- **Auto-set**: `created_at` set on creation, `updated_at` updated on modification
- **Format**: ISO 8601 (e.g., "2026-02-07T14:30:00Z")

### SQLModel Implementation

```python
from sqlmodel import SQLModel, Field, Column, DateTime, Index
from datetime import datetime
from typing import Optional

class Task(SQLModel, table=True):
    """
    Represents a user's task with ownership tracking and timestamps.

    All queries MUST filter by user_id to enforce data isolation.
    """
    __tablename__ = "tasks"

    # Primary key
    id: Optional[int] = Field(default=None, primary_key=True)

    # Ownership (CRITICAL: filter all queries by this field)
    user_id: str = Field(
        ...,  # Required (no default)
        index=True,
        max_length=255,
        description="User ID from JWT sub claim"
    )

    # Task data
    title: str = Field(
        ...,  # Required
        min_length=1,
        max_length=200,
        description="Task title (1-200 chars)"
    )

    description: Optional[str] = Field(
        default=None,
        max_length=10000,
        description="Optional task description"
    )

    completed: bool = Field(
        default=False,
        index=True,
        description="Task completion status"
    )

    # Timestamps (auto-managed)
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(DateTime(timezone=True), nullable=False),
        description="Creation timestamp (UTC)"
    )

    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(DateTime(timezone=True), nullable=False, onupdate=datetime.utcnow),
        description="Last update timestamp (UTC)"
    )

    # Table-level configuration
    __table_args__ = (
        Index('idx_task_user_completed', 'user_id', 'completed'),
    )

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "user_id": "user-123",
                "title": "Buy groceries",
                "description": "Milk, eggs, bread",
                "completed": False,
                "created_at": "2026-02-07T14:30:00Z",
                "updated_at": "2026-02-07T14:30:00Z"
            }
        }
```

---

## Entity: User (Conceptual)

### Purpose
Represents the authenticated user. **Not stored in database** - identity comes from JWT token.

### Schema

| Field | Type | Source | Description |
|-------|------|--------|-------------|
| `user_id` (or `sub`) | `str` | JWT `sub` claim | Unique user identifier |

### Relationship to Tasks
- **One-to-Many**: One user can have zero or more tasks
- **Enforcement**: Filtered at query level (not foreign key, since User table doesn't exist)
- **Isolation**: All task queries MUST include `WHERE user_id = <authenticated_user_id>`

### Notes
- User authentication and management handled by Better Auth on frontend
- Backend only validates JWT and extracts `user_id` from `sub` claim
- No user registration, profile, or password management in backend

---

## State Transitions

### Task Completion Status

```
[New Task]
     ↓
  completed: false (default)
     ↓
     ├─→ PATCH /api/tasks/{id}/complete → completed: true
     │                                          ↓
     └──────────────────────────────────────────┘
                    (toggle)
```

**Transition Rules**:
1. New tasks start with `completed = false` (automatic)
2. `PATCH /api/tasks/{id}/complete` toggles status:
   - `false` → `true`
   - `true` → `false`
3. `PUT /api/tasks/{id}` can also set `completed` directly (optional in request body)
4. No other states allowed (e.g., "in_progress", "archived") - out of scope

### Timestamp Updates

```
Task Created
    ↓
created_at ← UTC now()
updated_at ← UTC now()
    ↓
Task Modified (PUT, PATCH)
    ↓
updated_at ← UTC now() (created_at unchanged)
```

**Update Triggers**:
- `created_at`: Set once on task creation, never changes
- `updated_at`: Updated automatically on any modification (title, description, completed)
- System-managed: Users cannot set these timestamps manually

---

## Relationships

### Task → User (Conceptual)

```
Task {
    user_id: str  ──→  JWT sub claim (User identity)
}
```

**Type**: Many-to-One (conceptual, not enforced by foreign key)

**Enforcement**:
- Application-level validation
- All queries filtered by `user_id = authenticated_user_from_jwt`

**Why Not Foreign Key?**
- User table doesn't exist in database
- User identity managed by Better Auth (external to backend)
- Flexibility: users can exist without backend database records

---

## Query Patterns

### User's Tasks (List)

```python
# Get all tasks for authenticated user
result = await session.execute(
    select(Task)
    .where(Task.user_id == current_user_id)
    .order_by(Task.created_at.desc())
)
tasks = result.scalars().all()
```

### User's Active Tasks (Filtered)

```python
# Get incomplete tasks for authenticated user
result = await session.execute(
    select(Task)
    .where(Task.user_id == current_user_id, Task.completed == False)
    .order_by(Task.created_at.desc())
)
tasks = result.scalars().all()
```

### User's Specific Task (Retrieve)

```python
# Get specific task (enforces ownership)
result = await session.execute(
    select(Task)
    .where(Task.id == task_id, Task.user_id == current_user_id)
)
task = result.scalar_one_or_none()

if not task:
    raise HTTPException(404, "Task not found")  # Don't leak existence
```

### Task Creation (Insert)

```python
# Create task with authenticated user_id
task = Task(
    user_id=current_user_id,  # From JWT, NEVER from request
    title=request.title.strip(),  # Trim whitespace
    description=request.description,
    completed=False  # Default
)
session.add(task)
await session.commit()
await session.refresh(task)
```

### Task Update (Modify)

```python
# Update task (enforce ownership)
result = await session.execute(
    select(Task)
    .where(Task.id == task_id, Task.user_id == current_user_id)
)
task = result.scalar_one_or_none()

if not task:
    raise HTTPException(404, "Task not found")

# Update fields
if request.title is not None:
    task.title = request.title.strip()
if request.description is not None:
    task.description = request.description
if request.completed is not None:
    task.completed = request.completed

# updated_at will auto-update
await session.commit()
await session.refresh(task)
```

### Task Deletion (Remove)

```python
# Delete task (enforce ownership)
result = await session.execute(
    select(Task)
    .where(Task.id == task_id, Task.user_id == current_user_id)
)
task = result.scalar_one_or_none()

if not task:
    raise HTTPException(404, "Task not found")

await session.delete(task)
await session.commit()
```

---

## Security Considerations

### Data Isolation
- **CRITICAL**: Every query MUST include `where Task.user_id == current_user_id`
- **Defense in Depth**: Even if route logic has bugs, query-level filtering prevents leaks
- **404 for Unauthorized**: Return same error for "not found" and "not yours" (don't leak existence)

### User ID Source
- **ONLY from JWT**: `user_id` extracted from `sub` claim in validated JWT token
- **NEVER from Request**: Reject any `user_id` in request body, query params, or path params
- **Immutable**: Once task is created, `user_id` cannot be changed

### Validation at DB Layer
- **Length Constraints**: Enforced by SQLModel/SQLAlchemy to prevent oversized data
- **Not Null Constraints**: Critical fields (user_id, title, completed) cannot be null
- **Type Safety**: SQLModel provides runtime validation of types

### Timestamp Integrity
- **System-Managed**: Users cannot forge timestamps
- **UTC Only**: Prevents timezone confusion and manipulation
- **Audit Trail**: `created_at` provides immutable creation record

---

## Performance Considerations

### Index Strategy
- **Primary Queries**: Filtered by `user_id` (indexed)
- **Status Filtering**: Filtered by `completed` (indexed)
- **Common Pattern**: `user_id + completed` (composite index)
- **Sorting**: `ORDER BY created_at DESC` (no index needed for typical result set sizes)

### Expected Load
- **Scale**: 10k+ users, 100k+ tasks
- **Query Pattern**: Mostly reads (GET) with occasional writes (POST, PUT, PATCH, DELETE)
- **Indexing Impact**: Composite index reduces query time from O(n) to O(log n) for filtered queries

### Connection Pooling
- See research.md for Neon connection pooling strategy
- Pool size: 10 connections (sufficient for typical workload)
- Pre-ping enabled to handle serverless connection drops

---

## Migration Strategy

### Initial Migration (Alembic)

```python
# alembic/versions/001_create_tasks_table.py
def upgrade():
    op.create_table(
        'tasks',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('user_id', sa.String(255), nullable=False, index=True),
        sa.Column('title', sa.String(200), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('completed', sa.Boolean(), nullable=False, default=False, index=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now(), onupdate=sa.func.now())
    )

    op.create_index('idx_task_user_completed', 'tasks', ['user_id', 'completed'])

def downgrade():
    op.drop_table('tasks')
```

### Future Migrations
- Add columns: Use nullable initially, then backfill if needed
- Change constraints: Validate data first, then apply constraint
- Add indexes: Create concurrently to avoid locking (PostgreSQL)

---

## Testing Data

### Test Fixtures

```python
# tests/fixtures.py
import pytest
from models import Task
from datetime import datetime

@pytest.fixture
def sample_task_data():
    return {
        "user_id": "test-user-123",
        "title": "Test Task",
        "description": "This is a test task",
        "completed": False
    }

@pytest.fixture
def create_task(db_session, sample_task_data):
    def _create(**overrides):
        data = {**sample_task_data, **overrides}
        task = Task(**data)
        db_session.add(task)
        db_session.commit()
        db_session.refresh(task)
        return task
    return _create
```

### Test Cases for Validation

```python
# tests/test_task_model.py
def test_task_title_required(db_session):
    with pytest.raises(ValidationError):
        task = Task(user_id="user-123", completed=False)
        db_session.add(task)
        db_session.commit()

def test_task_title_too_long(db_session):
    with pytest.raises(ValidationError):
        task = Task(
            user_id="user-123",
            title="A" * 201,  # Exceeds 200 char limit
            completed=False
        )
        db_session.add(task)
        db_session.commit()

def test_task_default_values(create_task):
    task = create_task(title="Test")
    assert task.completed is False
    assert task.description is None
    assert task.created_at is not None
    assert task.updated_at is not None
```

---

## Summary

### Key Entities
- **Task**: User-owned task with title, description, completion status, and timestamps
- **User** (conceptual): Identity from JWT, not stored in database

### Critical Rules
1. All task queries MUST filter by `user_id` from authenticated JWT
2. `user_id` MUST come from JWT `sub` claim, NEVER from request
3. Return 404 for both "not found" and "unauthorized" (don't leak existence)
4. Timestamps are system-managed, cannot be set by users
5. Title is required (1-200 chars), description is optional (0-10000 chars)

### Next Steps
1. Generate OpenAPI contracts based on this data model
2. Create Pydantic schemas for request/response validation
3. Implement SQLModel Task class in `backend/models.py`
4. Create Alembic migration for tasks table
5. Write unit tests for Task model validation

---

**Data Model Status**: ✅ Complete

**Validated By**: Aligned with FR-005, FR-007, FR-009, FR-010, FR-011

**Next Artifact**: API contracts (OpenAPI specification)
