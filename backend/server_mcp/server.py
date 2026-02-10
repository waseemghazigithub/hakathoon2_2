"""
MCP Server implementation for Todo AI Chatbot.
"""

from mcp.server import Server
from .tools.add_task import register_add_task
from .tools.list_tasks import register_list_tasks
from .tools.complete_task import register_complete_task
from .tools.delete_task import register_delete_task
from .tools.update_task import register_update_task

# Initialize the MCP Server
mcp_server = Server("TodoMCP")

# Register all tools
register_add_task(mcp_server)
register_list_tasks(mcp_server)
register_complete_task(mcp_server)
register_delete_task(mcp_server)
register_update_task(mcp_server)
