"""
Message repository for database operations.
"""

from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from models import Message, MessageRole

async def save_message(
    session: AsyncSession,
    user_id: str,
    conversation_id: int,
    role: MessageRole,
    content: str
) -> Message:
    message = Message(
        user_id=user_id,
        conversation_id=conversation_id,
        role=role,
        content=content
    )
    session.add(message)
    await session.commit()
    await session.refresh(message)
    return message

async def get_conversation_history(
    session: AsyncSession,
    conversation_id: int,
    user_id: str,
    limit: int = 50
) -> List[Message]:
    statement = (
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .where(Message.user_id == user_id)
        .order_by(Message.created_at.asc())
        .limit(limit)
    )
    result = await session.execute(statement)
    return list(result.scalars().all())
