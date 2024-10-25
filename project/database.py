from pathlib import Path

from fastapi import FastAPI
import aiosqlite
import asyncio
from typing import AsyncGenerator, Sized
from contextlib import asynccontextmanager


DB_PATH = Path(__file__).parent / "db" / "chinook.db"
POOL_SIZE = 5


class DatabasePool:
    """
    This class creates a database pool the system can use
    to re-use database connections, rather than re-connecting
    for every request. This improves database access
    performance.
    """
    
    def __init__(self, size: int = POOL_SIZE):
        self.pool = asyncio.Queue()
        self.size = size

    async def init(self):
        for _ in range(self.size):
            db = await aiosqlite.connect(DB_PATH)
            await self.pool.put(db)
            self.size += 1

    async def acquire(self):
        return await self.pool.get()

    async def release(self, conn):
        await self.pool.put(conn)

    async def close(self):
        while not self.pool.empty():
            conn = await self.pool.get()
            await conn.close()


db_pool = DatabasePool(size=POOL_SIZE)


@asynccontextmanager
async def get_db() -> AsyncGenerator[aiosqlite.Connection, None]:
    """
    An asyncio friendly function to get a connection
    from the database connection pool
    """
    conn = await db_pool.acquire()
    try:
        yield conn
    finally:
        await db_pool.release(conn)
        
        
def register_fastapi_events(app: FastAPI) -> None:
    @app.on_event("startup")
    async def startup():
        print("application starting up")
        await db_pool.init()

    @app.on_event("shutdown")
    async def shutdown():
        print("application closing down")
        await db_pool.close()

    
