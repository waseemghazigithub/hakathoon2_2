"""
Chat API route for Todo AI Chatbot.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_session
from auth import CurrentUser
from services.chat_service import process_chat_message

router = APIRouter(prefix="/api/chat", tags=["Chat"])

class ChatRequest(BaseModel):
    conversation_id: Optional[int] = None
    message: str

class ChatResponse(BaseModel):
    conversation_id: int
    response: str

@router.post("", response_model=ChatResponse)
async def chat_endpoint(
    request: ChatRequest,
    user_id: CurrentUser,
    session: AsyncSession = Depends(get_session)
):
    """
    Handle chat messages and return AI agent responses.
    
    The user_id is automatically extracted from the JWT token.
    """
    try:
        conv_id, response_text = await process_chat_message(
            session=session,
            user_id=user_id,
            message_content=request.message,
            conversation_id=request.conversation_id
        )
        
        return ChatResponse(
            conversation_id=conv_id,
            response=response_text
        )
        
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Error in chat endpoint: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )
