"""
OpenAI Agent implementation for Todo Chatbot.
"""

import json
from typing import List
from openai import AsyncOpenAI
from openai.types.chat import ChatCompletionMessageParam, ChatCompletionToolParam
from core.config import settings
from server_mcp.tools import add_task, list_tasks, complete_task, delete_task, update_task

# Initialize OpenAI Client
client = AsyncOpenAI(api_key=settings.openai_api_key)

# Define tools for OpenAI Chat Completions
tools: List[ChatCompletionToolParam] = [
    {
        "type": "function",
        "function": {
            "name": "add_task",
            "description": "Create a new task for the user.",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {"type": "string", "description": "The ID of the user."},
                    "title": {"type": "string", "description": "The title of the task."},
                    "description": {"type": "string", "description": "Optional description."}
                },
                "required": ["user_id", "title"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_tasks",
            "description": "List tasks for a user.",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {"type": "string", "description": "The ID of the user."},
                    "status": {"type": "string", "description": "Filter by status (all, pending, completed).", "enum": ["all", "pending", "completed"]}
                },
                "required": ["user_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "complete_task",
            "description": "Mark a task as complete.",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {"type": "string", "description": "The ID of the user."},
                    "task_id": {"type": "integer", "description": "The ID of the task to complete."}
                },
                "required": ["user_id", "task_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "delete_task",
            "description": "Delete a task.",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {"type": "string", "description": "The ID of the user."},
                    "task_id": {"type": "integer", "description": "The ID of the task to delete."}
                },
                "required": ["user_id", "task_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "update_task",
            "description": "Update a task's title or description.",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {"type": "string", "description": "The ID of the user."},
                    "task_id": {"type": "integer", "description": "The ID of the task to update."},
                    "title": {"type": "string", "description": "New title."},
                    "description": {"type": "string", "description": "New description."}
                }
            },
            "required": ["user_id", "task_id"]
        }
    }
]

async def get_agent_response(user_id: str, messages: List[ChatCompletionMessageParam]) -> str:
    """
    Run the agent and get a response using OpenAI Chat Completions with function calling.
    """
    
    # Identify available functions
    available_functions = {
        "add_task": add_task,
        "list_tasks": list_tasks,
        "complete_task": complete_task,
        "delete_task": delete_task,
        "update_task": update_task,
    }

    # 1. Call OpenAI API
    response = await client.chat.completions.create(
        model=settings.openai_model,
        messages=messages,
        tools=tools,
        tool_choice="auto",
    )
    
    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls

    # 2. Check if the model wants to call a function
    if tool_calls:
        # Append the assistant's message (with tool calls) to history
        messages.append(response_message)
        
        # Execute tool calls
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions.get(function_name)
            function_args = json.loads(tool_call.function.arguments)
            
            # Security: Always force the user_id from the authenticated context.
            if "user_id" in function_args:
                function_args["user_id"] = user_id
            
            if function_to_call:
                try:
                    function_response = await function_to_call(**function_args)
                except Exception as e:
                    function_response = f"Error executing tool: {str(e)}"
                    
                messages.append(
                    {
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": str(function_response),
                    }
                )

        # 3. Get final response from model
        second_response = await client.chat.completions.create(
            model=settings.openai_model,
            messages=messages,
        )
        return second_response.choices[0].message.content

    return response_message.content
