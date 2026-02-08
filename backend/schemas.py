"""
Pydantic schemas for request/response validation.

Implements data validation for task operations (FR-009, FR-010, FR-011).
"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator, ConfigDict
from pydantic.alias_generators import to_camel


class TaskCreate(BaseModel):
    """
    Schema for creating a new task.

    Validation (FR-009):
    - title: required, 1-200 characters, whitespace stripped
    - description: optional, max 10000 characters

    Note:
    - user_id is NOT accepted from request (FR-003)
    - user_id is derived from JWT token by get_current_user dependency
    - completed defaults to False (FR-010)
    """

    title: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Task title (1-200 characters)"
    )

    description: Optional[str] = Field(
        default=None,
        max_length=10000,
        description="Optional task description (max 10000 characters)"
    )

    @field_validator("title")
    @classmethod
    def strip_title_whitespace(cls, v: str) -> str:
        """Strip leading/trailing whitespace from title."""
        stripped = v.strip()
        if not stripped:
            raise ValueError("Title cannot be empty or only whitespace")
        return stripped

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "Buy groceries",
                    "description": "Milk, eggs, bread"
                },
                {
                    "title": "Meeting at 3pm"
                }
            ]
        }
    }


class TaskUpdate(BaseModel):
    """
    Schema for updating an existing task.

    Validation:
    - All fields are optional (partial updates)
    - title: if provided, 1-200 characters, whitespace stripped
    - description: if provided, max 10000 characters
    - completed: if provided, boolean only

    Note:
    - user_id cannot be changed (enforced by ownership check)
    - updated_at is automatically updated (FR-011)
    """

    title: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=200,
        description="Updated task title (1-200 characters, optional)"
    )

    description: Optional[str] = Field(
        default=None,
        max_length=10000,
        description="Updated task description (max 10000 characters, optional)"
    )

    completed: Optional[bool] = Field(
        default=None,
        description="Updated completion status (optional)"
    )

    @field_validator("title")
    @classmethod
    def strip_title_whitespace(cls, v: Optional[str]) -> Optional[str]:
        """Strip leading/trailing whitespace from title if provided."""
        if v is not None:
            stripped = v.strip()
            if not stripped:
                raise ValueError("Title cannot be empty or only whitespace")
            return stripped
        return v

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "Buy groceries and snacks"
                },
                {
                    "title": "Buy groceries",
                    "description": "Milk, eggs, bread, cheese",
                    "completed": True
                }
            ]
        }
    }


class TaskRead(BaseModel):
    """
    Schema for reading task data (responses).

    Includes all task fields including system-managed fields:
    - id: task identifier
    - user_id: owner identifier
    - title, description, completed: user data
    - created_at, updated_at: timestamps
    """

    id: int = Field(
        ...,
        description="Unique task identifier"
    )

    user_id: str = Field(
        ...,
        description="Owner's user ID from JWT"
    )

    title: str = Field(
        ...,
        description="Task title"
    )

    description: Optional[str] = Field(
        default=None,
        description="Task description"
    )

    completed: bool = Field(
        ...,
        description="Completion status"
    )

    created_at: datetime = Field(
        ...,
        description="Task creation timestamp (UTC)"
    )

    updated_at: datetime = Field(
        ...,
        description="Last modification timestamp (UTC)"
    )

    model_config = ConfigDict(
        from_attributes=True,
        alias_generator=to_camel,
        populate_by_name=True,
        json_schema_extra={
            "examples": [
                {
                    "id": 1,
                    "userId": "user-123",
                    "title": "Buy groceries",
                    "description": "Milk, eggs, bread",
                    "completed": False,
                    "createdAt": "2026-02-07T14:30:00Z",
                    "updatedAt": "2026-02-07T14:30:00Z"
                }
            ]
        }
    )


class RecentActivity(BaseModel):
    """Schema for recent task activity items on dashboard."""
    id: int
    title: str
    completed: bool
    created_at: datetime
    type: str  # 'created' or 'completed'

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True
    )


class DashboardStats(BaseModel):
    """Schema for dashboard summary statistics."""
    total_tasks: int
    completed_tasks: int
    pending_tasks: int
    completion_rate: float
    recent_activity: list[RecentActivity]

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True
    )


"""
Schema Design Notes:

1. Request Schemas (Create/Update):
   - DO NOT include user_id (security: FR-003)
   - DO NOT include timestamps (managed by system)
   - DO NOT include id (auto-generated)
   - Strip whitespace from title to prevent validation bypass
   - Validate length constraints per FR-009

2. Response Schema (Read):
   - Include ALL fields for frontend display
   - Enable from_attributes for SQLModel ORM conversion
   - Timestamps in ISO 8601 format (UTC)

3. Validation Strategy:
   - Pydantic validates BEFORE database insert/update
   - Database constraints provide second layer of validation
   - FastAPI automatically returns 422 for validation errors
   - Custom validators handle whitespace and business rules

4. Frontend Contract:
   - TaskCreate: what frontend sends to create task
   - TaskUpdate: what frontend sends to update task
   - TaskRead: what frontend receives from API
   - All schemas match OpenAPI spec (contracts/openapi.yaml)
"""
