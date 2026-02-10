"""
Database models for Task Management API.

Implements FR-005 (Task model with proper indexes and constraints).
"""
from enum import Enum
from datetime import datetime, timezone
from typing import Optional, List, TYPE_CHECKING

from sqlmodel import SQLModel, Field, Index, Relationship
from sqlalchemy import Column, DateTime, func


class User(SQLModel, table=True):
    """
    User model for authentication and data isolation.
    """
    id: str = Field(primary_key=True, max_length=255)
    email: str = Field(index=True, unique=True, nullable=False)
    name: str = Field(nullable=False)
    hashed_password: str = Field(nullable=False)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    )

class Task(SQLModel, table=True):
    """
    Task model for database storage.

    Implements:
    - FR-005: Task model with all required fields
    - FR-007: User data isolation via user_id indexed field
    - FR-010: Default completed=false
    - FR-011: Automatic timestamps

    Indexes:
    - user_id (single index for user-based queries)
    - completed (single index for filtering)
    - (user_id, completed) composite index for filtered user queries

    Constraints:
    - title: 1-200 characters, NOT NULL
    - description: max 10000 characters, NULLABLE
    - user_id: NOT NULL, indexed
    - completed: boolean, default False, indexed
    - created_at: auto-set on creation, NOT NULL
    - updated_at: auto-updated on modification, NOT NULL
    """

    __tablename__ = "tasks"

    # Primary key
    id: Optional[int] = Field(
        default=None,
        primary_key=True,
        description="Unique task identifier"
    )

    # User ownership (FR-003, FR-007)
    user_id: str = Field(
        index=True,
        nullable=False,
        max_length=255,
        description="User ID from JWT sub claim - enforces data isolation"
    )

    # Task content
    title: str = Field(
        min_length=1,
        max_length=200,
        nullable=False,
        description="Task title (1-200 characters)"
    )

    description: Optional[str] = Field(
        default=None,
        max_length=10000,
        description="Optional task description (max 10000 characters)"
    )

    # Task status (FR-010)
    completed: bool = Field(
        default=False,
        index=True,
        nullable=False,
        description="Completion status (default: False)"
    )

    # Timestamps (FR-011)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True), nullable=False, server_default=func.now()),
        description="Task creation timestamp (UTC)"
    )

    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False,
            server_default=func.now(),
            onupdate=func.now()
        ),
        description="Last modification timestamp (UTC, auto-updated)"
    )

    # Table-level indexes
    __table_args__ = (
        # Composite index for efficient user + completion status filtering
        Index("idx_task_user_completed", "user_id", "completed"),
    )


class Conversation(SQLModel, table=True):
    """
    Conversation entity for managing AI chat sessions.
    """
    __tablename__ = "conversations"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True, nullable=False, max_length=255)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False,
            server_default=func.now(),
            onupdate=func.now()
        )
    )

    # Relationships
    messages: List["Message"] = Relationship(back_populates="conversation")


class MessageRole(str, Enum):
    """Message role enum for user vs assistant messages."""
    USER = "user"
    ASSISTANT = "assistant"


class Message(SQLModel, table=True):
    """
    Message entity representing a single message in a conversation.
    """
    __tablename__ = "messages"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True, nullable=False, max_length=255)
    conversation_id: int = Field(foreign_key="conversations.id", nullable=False, index=True)
    role: MessageRole = Field(nullable=False)
    content: str = Field(nullable=False)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True), nullable=False, server_default=func.now(), index=True)
    )

    # Relationships
    conversation: "Conversation" = Relationship(back_populates="messages")


"""
Data Model Notes:

1. User Ownership:
   - user_id is ALWAYS derived from JWT token, NEVER from request
   - All queries MUST filter by user_id to enforce data isolation
   - user_id is indexed for query performance

2. Validation Rules:
   - title: required, 1-200 characters, stripped of whitespace
   - description: optional, max 10000 characters
   - completed: boolean only (no null)
   - timestamps: managed by database, not user-editable

3. Index Strategy:
   - user_id: for user-specific queries (list all tasks)
   - completed: for filtering by status
   - (user_id, completed): composite for filtered user queries

4. Timestamp Management:
   - created_at: set on insert, never changes
   - updated_at: automatically updated on any row modification
   - All timestamps are UTC for consistency
"""
