from pathlib import Path

from typing import AsyncGenerator
from sqlmodel import SQLModel
from sqlalchemy.pool import StaticPool
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from contextlib import asynccontextmanager

DB_PATH = Path(__file__).parent / "db" / "active" / "chinook.db"
DATABASE_URL = f"sqlite+aiosqlite:///{DB_PATH}"
POOL_SIZE = 5

# create the async engine with connection pooling
engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)


async def init_db():
    """Initialize the database and create tables if they don't exist."""
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


@asynccontextmanager
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Provide a transactional scope for the database session."""
    async with AsyncSession(engine) as session:
        try:
            yield session
        finally:
            await session.close()
