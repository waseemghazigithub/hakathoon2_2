"""
MCP tool: add_task
"""

from mcp.server import Server
from services.task_service import create_task
from db import async_session_maker

async def add_task(user_id: str, title: str, description: str = None) -> str:
    """
    Create a new task for the user.
    """
    async with async_session_maker() as session:
        task = await create_task(session, user_id=user_id, title=title, description=description)
        return f"Task created: ID={task.id}, title='{task.title}'"

def register_add_task(mcp_server: Server):
    mcp_server.tool("add_task")(add_task)
