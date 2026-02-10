"""
Pydantic schemas for MCP tools.
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class AddTaskInput(BaseModel):
    user_id: str = Field(..., description="User ID")
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=2000)

class AddTaskOutput(BaseModel):
    task_id: int
    status: str
    title: str

class ListTasksInput(BaseModel):
    user_id: str
    status: str = Field(default="all", description="all, pending, or completed")

class TaskDetail(BaseModel):
    id: int
    title: str
    description: Optional[str]
    completed: bool
    created_at: datetime

class ListTasksOutput(BaseModel):
    tasks: List[TaskDetail]
    count: int

class CompleteTaskInput(BaseModel):
    user_id: str
    task_id: int

class DeleteTaskOutput(BaseModel):
    task_id: int
    status: str
    title: str

class UpdateTaskInput(BaseModel):
    user_id: str
    task_id: int
    title: Optional[str] = None
    description: Optional[str] = None
