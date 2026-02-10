"""
MCP tool: list_tasks
"""

from mcp.server import Server
from services.task_service import get_user_tasks
from db import async_session_maker

async def list_tasks(user_id: str, status: str = "all") -> str:
    """
    List tasks for a user.
    """
    async with async_session_maker() as session:
        tasks = await get_user_tasks(session, user_id=user_id, status_filter=status)
        if not tasks:
            return "No tasks found."
        task_list = "\n".join([f"- [{ 'X' if t.completed else ' ' }] {t.id}: {t.title}" for t in tasks])
        return f"Tasks for {user_id} ({status}):\n{task_list}"

def register_list_tasks(mcp_server: Server):
    mcp_server.tool("list_tasks")(list_tasks)
