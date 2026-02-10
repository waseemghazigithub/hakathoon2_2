"""
Chat service orchestration for Todo AI Chatbot.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List

from repositories.conversation_repo import create_conversation, get_conversation, touch_conversation
from repositories.message_repo import save_message, get_conversation_history
from agents.todo_agent import get_agent_response
from models import MessageRole

async def process_chat_message(
    session: AsyncSession,
    user_id: str,
    message_content: str,
    conversation_id: Optional[int] = None
):
    # 1. Get or create conversation
    if conversation_id:
        conversation = await get_conversation(session, conversation_id, user_id)
        if not conversation:
            raise ValueError("Conversation not found")
    else:
        conversation = await create_conversation(session, user_id)

    # 2. Get history
    history = await get_conversation_history(session, conversation.id, user_id)

    # 3. Store user message
    await save_message(
        session,
        user_id,
        conversation.id,
        MessageRole.USER,
        message_content
    )

    # 4. Prepare messages for Agent
    agent_messages = [
        {"role": msg.role.value, "content": msg.content}
        for msg in history
    ]
    # Add system hint for context
    agent_messages.insert(0, {
        "role": "system",
        "content": f"The current user_id is '{user_id}'. Always use this user_id for task operations. Be concise and friendly."
    })
    agent_messages.append({"role": "user", "content": message_content})

    # 5. Get Agent response
    assistant_content = await get_agent_response(user_id, agent_messages)

    # 6. Store assistant message
    await save_message(
        session,
        user_id,
        conversation.id,
        MessageRole.ASSISTANT,
        assistant_content
    )

    # 7. Update conversation timestamp
    await touch_conversation(session, conversation.id, user_id)

    return conversation.id, assistant_content
