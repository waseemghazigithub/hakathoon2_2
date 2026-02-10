"""
Conversation repository for database operations.
"""

from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from datetime import datetime, timezone
from models import Conversation

async def create_conversation(session: AsyncSession, user_id: str) -> Conversation:
    conversation = Conversation(user_id=user_id)
    session.add(conversation)
    await session.commit()
    await session.refresh(conversation)
    return conversation

async def get_conversation(
    session: AsyncSession,
    conversation_id: int,
    user_id: str
) -> Optional[Conversation]:
    statement = (
        select(Conversation)
        .where(Conversation.id == conversation_id)
        .where(Conversation.user_id == user_id)
    )
    result = await session.execute(statement)
    return result.scalar_one_or_none()

async def touch_conversation(
    session: AsyncSession,
    conversation_id: int,
    user_id: str
) -> None:
    conversation = await get_conversation(session, conversation_id, user_id)
    if conversation:
        conversation.updated_at = datetime.now(timezone.utc)
        session.add(conversation)
        await session.commit()
