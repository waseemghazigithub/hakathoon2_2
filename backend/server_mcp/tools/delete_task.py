"""
MCP tool: delete_task
"""

from mcp.server import Server
from services.task_service import delete_task as db_delete_task
from db import async_session_maker

async def delete_task(user_id: str, task_id: int) -> str:
    """
    Delete a task.
    """
    async with async_session_maker() as session:
        success = await db_delete_task(session, user_id=user_id, task_id=task_id)
        if not success:
            return f"Task {task_id} not found."
        return f"Task {task_id} deleted successfully."

def register_delete_task(mcp_server: Server):
    mcp_server.tool("delete_task")(delete_task)
