"""
Task service layer for Todo AI Chatbot integration.
"""

from typing import List, Optional
from sqlmodel import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timezone

from models import Task

async def create_task(
    session: AsyncSession,
    user_id: str,
    title: str,
    description: Optional[str] = None
) -> Task:
    """Create a new task in the database."""
    task = Task(
        user_id=user_id,
        title=title,
        description=description,
        completed=False
    )
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task

async def get_user_tasks(
    session: AsyncSession,
    user_id: str,
    status_filter: str = "all"
) -> List[Task]:
    """Retrieve tasks for a user with optional filter."""
    statement = select(Task).where(Task.user_id == user_id)
    
    if status_filter == "pending":
        statement = statement.where(Task.completed == False)
    elif status_filter == "completed":
        statement = statement.where(Task.completed == True)
        
    statement = statement.order_by(desc(Task.created_at))
    result = await session.execute(statement)
    return list(result.scalars().all())

async def get_task_by_id(
    session: AsyncSession,
    user_id: str,
    task_id: int
) -> Optional[Task]:
    """Retrieve a specific task for a user."""
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    result = await session.execute(statement)
    return result.scalar_one_or_none()

async def update_task_status(
    session: AsyncSession,
    user_id: str,
    task_id: int,
    completed: bool
) -> Optional[Task]:
    """Update the status of a task."""
    task = await get_task_by_id(session, user_id, task_id)
    if not task:
        return None
        
    task.completed = completed
    # updated_at is handled by server_default/onupdate in models.py
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task

async def delete_task(
    session: AsyncSession,
    user_id: str,
    task_id: int
) -> bool:
    """Delete a task from the database."""
    task = await get_task_by_id(session, user_id, task_id)
    if not task:
        return False
        
    await session.delete(task)
    await session.commit()
    return True

async def update_task_details(
    session: AsyncSession,
    user_id: str,
    task_id: int,
    title: Optional[str] = None,
    description: Optional[str] = None
) -> Optional[Task]:
    """Update task title and/or description."""
    task = await get_task_by_id(session, user_id, task_id)
    if not task:
        return None
        
    if title:
        task.title = title
    if description is not None:
        task.description = description
        
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task
