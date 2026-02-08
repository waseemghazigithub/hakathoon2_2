"""
Database engine and session management for async SQLModel.

Implements connection pooling strategy from research.md for Neon PostgreSQL.
"""
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

from core.config import settings


# Convert postgres:// to postgresql+asyncpg:// if needed
database_url = settings.database_url
if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql+asyncpg://", 1)
elif database_url.startswith("postgresql://"):
    database_url = database_url.replace("postgresql://", "postgresql+asyncpg://", 1)

# Remove query parameters like sslmode from URL as asyncpg doesn't support them directly
if "?" in database_url:
    database_url = database_url.split("?")[0]

# Create async engine with connection pooling for Neon
engine: AsyncEngine = create_async_engine(
    database_url,
    echo=False,
    pool_size=10,
    max_overflow=0,
    pool_pre_ping=True,
    pool_recycle=3600,
    connect_args={"ssl": True} # Explicitly enable SSL for Neon
)


# Create async session factory
async_session_maker = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency for database sessions.

    Usage:
        @app.get("/items")
        async def get_items(session: AsyncSession = Depends(get_session)):
            result = await session.execute(select(Item))
            return result.scalars().all()

    Yields:
        AsyncSession: Database session for the request

    Note:
        Session is automatically committed on success and rolled back on exception.
    """
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def create_db_and_tables():
    """
    Create all database tables.

    Note: In production, use Alembic migrations instead.
    This is useful for testing and initial development only.
    """
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def dispose_engine():
    """
    Dispose of the database engine.

    Should be called on application shutdown to clean up connections.
    """
    await engine.dispose()
