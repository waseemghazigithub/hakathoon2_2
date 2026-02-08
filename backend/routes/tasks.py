"""
Task CRUD routes with JWT authentication and user data isolation.

Implements:
- FR-006: REST API endpoints for task operations
- FR-007: User data isolation enforcement
- FR-008: Proper HTTP status codes
- FR-009: Task validation
"""
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from auth import CurrentUser
from db import get_session
from models import Task
from schemas import TaskCreate, TaskRead, TaskUpdate, DashboardStats, RecentActivity


# Create router with prefix and tags
router = APIRouter(
    prefix="/api/tasks",
    tags=["Tasks"],
)


@router.get("/stats", response_model=DashboardStats, status_code=status.HTTP_200_OK)
async def get_task_stats(
    user_id: CurrentUser,
    session: AsyncSession = Depends(get_session),
) -> DashboardStats:
    """
    Get dashboard statistics for the authenticated user.
    """
    # Total tasks count
    total_query = select(func.count(Task.id)).where(Task.user_id == user_id)
    total_result = await session.execute(total_query)
    total_tasks = total_result.scalar() or 0

    # Completed tasks count
    completed_query = select(func.count(Task.id)).where(
        Task.user_id == user_id, Task.completed == True
    )
    completed_result = await session.execute(completed_query)
    completed_tasks = completed_result.scalar() or 0

    # Pending tasks
    pending_tasks = total_tasks - completed_tasks

    # Completion rate
    completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0

    # Recent activity (last 5 tasks)
    recent_query = (
        select(Task)
        .where(Task.user_id == user_id)
        .order_by(Task.updated_at.desc())
        .limit(5)
    )
    recent_result = await session.execute(recent_query)
    recent_tasks = recent_result.scalars().all()

    recent_activity = [
        RecentActivity(
            id=t.id,
            title=t.title,
            completed=t.completed,
            created_at=t.created_at,
            type="completed" if t.completed else "created"
        )
        for t in recent_tasks
    ]

    return DashboardStats(
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        pending_tasks=pending_tasks,
        completion_rate=round(completion_rate, 1),
        recent_activity=recent_activity
    )


@router.get("", response_model=List[TaskRead], status_code=status.HTTP_200_OK)
async def list_tasks(
    user_id: CurrentUser,
    session: AsyncSession = Depends(get_session),
    status_filter: Optional[str] = Query(
        None,
        alias="status",
        description="Filter by completion status: 'completed' or 'active'"
    ),
) -> List[Task]:
    """
    List all tasks for authenticated user (T031-T034).

    Implements:
    - FR-006: GET /api/tasks endpoint
    - FR-007: User data isolation (filter by user_id from JWT)
    - Optional filtering by completion status

    Query Parameters:
    - status: "completed" (completed=True) or "active" (completed=False)

    Returns:
    - 200 OK: List of tasks (sorted by created_at descending)
    - 401 Unauthorized: Invalid/missing JWT token

    Security:
    - ONLY returns tasks where task.user_id == authenticated user_id
    - Users cannot see other users' tasks
    """
    # Build query with user_id filter (FR-007 - CRITICAL)
    query = select(Task).where(Task.user_id == user_id)

    # Apply optional status filter (T032)
    if status_filter == "completed":
        query = query.where(Task.completed == True)
    elif status_filter == "active":
        query = query.where(Task.completed == False)
    elif status_filter is not None:
        # Invalid status value
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid status filter. Use 'completed' or 'active'",
        )

    # Sort by created_at descending (newest first) - T033
    query = query.order_by(Task.created_at.desc())

    # Execute query
    result = await session.execute(query)
    tasks = result.scalars().all()

    # Return empty list if no tasks (T033)
    return list(tasks)


@router.post("", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: TaskCreate,
    user_id: CurrentUser,
    session: AsyncSession = Depends(get_session),
) -> Task:
    """
    Create a new task for authenticated user (T035-T039).

    Implements:
    - FR-006: POST /api/tasks endpoint
    - FR-003: user_id from JWT ONLY (never from request body)
    - FR-009: Title validation (1-200 chars)
    - FR-010: Default completed=False

    Request Body:
    - title: required, 1-200 characters
    - description: optional, max 10000 characters

    Returns:
    - 201 Created: Task created successfully
    - 400 Bad Request: Validation error
    - 401 Unauthorized: Invalid/missing JWT token

    Security:
    - user_id is ALWAYS from JWT token (T037)
    - Request body CANNOT specify user_id
    """
    # Create task with user_id from JWT (T037 - SECURITY CRITICAL)
    # Title whitespace is stripped by TaskCreate validator (T038)
    task = Task(
        user_id=user_id,  # From JWT, not from request
        title=task_data.title,
        description=task_data.description,
        completed=False,  # Default per FR-010 (T037)
    )

    # Save to database
    session.add(task)
    await session.commit()
    await session.refresh(task)

    # Return 201 with TaskRead schema (T039)
    return task


@router.get("/{id}", response_model=TaskRead, status_code=status.HTTP_200_OK)
async def get_task(
    id: int,
    user_id: CurrentUser,
    session: AsyncSession = Depends(get_session),
) -> Task:
    """
    Get a single task by ID (T040-T043).

    Implements:
    - FR-006: GET /api/tasks/{id} endpoint
    - FR-007: User data isolation (ownership check)

    Path Parameters:
    - id: Task ID

    Returns:
    - 200 OK: Task details
    - 401 Unauthorized: Invalid/missing JWT token
    - 404 Not Found: Task doesn't exist OR doesn't belong to user

    Security:
    - Returns 404 for both "not found" and "unauthorized" (T042)
    - Prevents leaking existence of other users' tasks
    - Query MUST filter by both id AND user_id (T041)
    """
    # Query by id AND user_id for ownership enforcement (T041 - SECURITY CRITICAL)
    result = await session.execute(
        select(Task).where(Task.id == id, Task.user_id == user_id)
    )
    task = result.scalar_one_or_none()

    # Return 404 if not found or not owned (T042)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    # Return 200 with TaskRead schema (T043)
    return task


@router.put("/{id}", response_model=TaskRead, status_code=status.HTTP_200_OK)
async def update_task(
    id: int,
    task_data: TaskUpdate,
    user_id: CurrentUser,
    session: AsyncSession = Depends(get_session),
) -> Task:
    """
    Update an existing task (T044-T050).

    Implements:
    - FR-006: PUT /api/tasks/{id} endpoint
    - FR-007: User data isolation (ownership check)
    - FR-009: Title validation if provided
    - FR-011: Auto-update updated_at timestamp

    Path Parameters:
    - id: Task ID

    Request Body (all fields optional):
    - title: 1-200 characters if provided
    - description: max 10000 characters if provided
    - completed: boolean if provided

    Returns:
    - 200 OK: Task updated successfully
    - 400 Bad Request: Validation error
    - 401 Unauthorized: Invalid/missing JWT token
    - 404 Not Found: Task doesn't exist OR doesn't belong to user

    Security:
    - Query MUST filter by both id AND user_id (T045)
    - Returns 404 for unauthorized access (T046)
    """
    # Query by id AND user_id for ownership enforcement (T045 - SECURITY CRITICAL)
    result = await session.execute(
        select(Task).where(Task.id == id, Task.user_id == user_id)
    )
    task = result.scalar_one_or_none()

    # Return 404 if not found or not owned (T046)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    # Update only provided fields (T047)
    # Title whitespace is stripped by TaskUpdate validator (T047)
    update_data = task_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)

    # Commit changes
    # updated_at is automatically updated by SQLModel onupdate (T049)
    session.add(task)
    await session.commit()
    await session.refresh(task)

    # Return 200 with updated TaskRead schema (T050)
    return task


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    id: int,
    user_id: CurrentUser,
    session: AsyncSession = Depends(get_session),
) -> None:
    """
    Delete a task permanently (T051-T055).

    Implements:
    - FR-006: DELETE /api/tasks/{id} endpoint
    - FR-007: User data isolation (ownership check)

    Path Parameters:
    - id: Task ID

    Returns:
    - 204 No Content: Task deleted successfully
    - 401 Unauthorized: Invalid/missing JWT token
    - 404 Not Found: Task doesn't exist OR doesn't belong to user

    Security:
    - Query MUST filter by both id AND user_id (T052)
    - Returns 404 for unauthorized access (T053)
    """
    # Query by id AND user_id for ownership enforcement (T052 - SECURITY CRITICAL)
    result = await session.execute(
        select(Task).where(Task.id == id, Task.user_id == user_id)
    )
    task = result.scalar_one_or_none()

    # Return 404 if not found or not owned (T053)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    # Delete task from database (T054)
    await session.delete(task)
    await session.commit()

    # Return 204 No Content (T055)
    return None


@router.patch("/{id}/toggle-complete", response_model=TaskRead, status_code=status.HTTP_200_OK)
async def toggle_task_complete(
    id: int,
    user_id: CurrentUser,
    session: AsyncSession = Depends(get_session),
) -> Task:
    """
    Toggle task completion status (T056-T061).

    Implements:
    - FR-006: PATCH /api/tasks/{id}/complete endpoint
    - FR-007: User data isolation (ownership check)
    - FR-011: Auto-update updated_at timestamp

    Path Parameters:
    - id: Task ID

    Returns:
    - 200 OK: Task completion toggled (False → True or True → False)
    - 401 Unauthorized: Invalid/missing JWT token
    - 404 Not Found: Task doesn't exist OR doesn't belong to user

    Security:
    - Query MUST filter by both id AND user_id (T057)
    - Returns 404 for unauthorized access (T058)
    """
    # Query by id AND user_id for ownership enforcement (T057 - SECURITY CRITICAL)
    result = await session.execute(
        select(Task).where(Task.id == id, Task.user_id == user_id)
    )
    task = result.scalar_one_or_none()

    # Return 404 if not found or not owned (T058)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    # Toggle completed field (T059)
    task.completed = not task.completed

    # Commit changes
    # updated_at is automatically updated by SQLModel onupdate (T060)
    session.add(task)
    await session.commit()
    await session.refresh(task)

    # Return 200 with updated TaskRead schema (T061)
    return task


"""
Route Implementation Notes:

1. Security (FR-007 - CRITICAL):
   - ALL queries filter by user_id from JWT
   - user_id NEVER comes from request body/params/query
   - 404 returned for both "not found" and "unauthorized"
   - Prevents leaking existence of other users' tasks

2. HTTP Status Codes (FR-008):
   - 200 OK: Successful GET/PUT/PATCH
   - 201 Created: Successful POST
   - 204 No Content: Successful DELETE
   - 400 Bad Request: Validation errors
   - 401 Unauthorized: Auth errors (handled by get_current_user)
   - 404 Not Found: Resource not found or unauthorized

3. Validation (FR-009):
   - Pydantic schemas validate request data
   - Title: 1-200 characters, whitespace stripped
   - Description: max 10000 characters
   - FastAPI returns 400 for validation errors

4. Data Isolation (FR-007):
   - Every query includes: .where(Task.user_id == user_id)
   - No exceptions - user_id filter is mandatory
   - This is the PRIMARY security mechanism

5. Timestamp Management (FR-011):
   - created_at: set on insert, never modified
   - updated_at: automatically updated by SQLModel onupdate
   - No manual timestamp management needed
"""
