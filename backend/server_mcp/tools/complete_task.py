"""
MCP tool: complete_task
"""

from mcp.server import Server
from services.task_service import update_task_status
from db import async_session_maker

async def complete_task(user_id: str, task_id: int) -> str:
    """
    Mark a task as complete.
    """
    async with async_session_maker() as session:
        task = await update_task_status(session, user_id=user_id, task_id=task_id, completed=True)
        if not task:
            return f"Task {task_id} not found."
        return f"Task {task_id} marked as complete."

def register_complete_task(mcp_server: Server):
    mcp_server.tool("complete_task")(complete_task)
