from pathlib import Path

from fastapi import FastAPI
import aiosqlite
import asyncio
from typing import AsyncGenerator
from contextlib import asynccontextmanager


DB_PATH = Path(__file__).parent / "db" / "chinook.db"

class DatabasePool:
    """
    This class creates a database pool the system can use
    to re-use database connections, rather than re-connecting
    for every request. This improves database access
    performance.
    """
    POOL_SIZE = 5
    
    def __init__(self):
        self.pool = asyncio.Queue()
        self.size = 0

    async def init(self):
        for _ in range(DatabasePool:POOL_SIZE):
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

db_pool = DatabasePool()

@asynccontextmanager
async def get_db() -> AsyncGenerator[aiosqlite.Connection, None]:
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

    
