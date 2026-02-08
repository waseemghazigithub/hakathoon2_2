from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
import jwt
from datetime import datetime, timedelta, timezone
import uuid
from typing import Optional

from db import get_session
from models import User
from core.config import settings
from auth import security

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=7)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.better_auth_secret, algorithm="HS256")
    return encoded_jwt

from pydantic import BaseModel

class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/register")
async def register(request: RegisterRequest, session: AsyncSession = Depends(get_session)):
    # Check if user already exists
    statement = select(User).where(User.email == request.email)
    result = await session.execute(statement)
    if result.scalar_one_or_none():
        return {"success": False, "error": "Email already registered"}

    # Create new user
    user_id = str(uuid.uuid4())
    new_user = User(
        id=user_id,
        email=request.email,
        name=request.name,
        hashed_password=request.password, # In a real app, use hashing!
    )
    
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    
    token = create_access_token({"sub": user_id, "email": request.email})
    
    return {
        "success": True,
        "token": token,
        "user": {
            "id": user_id,
            "name": request.name,
            "email": request.email
        }
    }

@router.post("/login")
async def login(request: LoginRequest, session: AsyncSession = Depends(get_session)):
    statement = select(User).where(User.email == request.email)
    result = await session.execute(statement)
    user = result.scalar_one_or_none()
    
    if not user or user.hashed_password != request.password:
        return {"success": False, "error": "Invalid email or password"}
    
    token = create_access_token({"sub": user.id, "email": user.email})
    
    return {
        "success": True,
        "token": token,
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email
        }
    }
