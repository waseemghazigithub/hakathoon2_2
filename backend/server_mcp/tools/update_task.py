"""
MCP tool: update_task
"""

from mcp.server import Server
from services.task_service import update_task_details
from db import async_session_maker

async def update_task(user_id: str, task_id: int, title: str = None, description: str = None) -> str:
    """
    Update a task's title or description.
    """
    async with async_session_maker() as session:
        task = await update_task_details(session, user_id=user_id, task_id=task_id, title=title, description=description)
        if not task:
            return f"Task {task_id} not found."
        return f"Task {task_id} updated successfully."

def register_update_task(mcp_server: Server):
    mcp_server.tool("update_task")(update_task)
