from pathlib import Path

from fastapi import FastAPI, HTTPException, Depends
import aiosqlite
import asyncio
from typing import AsyncGenerator
from contextlib import asynccontextmanager


DB_PATH = Path(__file__).parent / "db" / "chinook.db"
POOL_SIZE = 5

app = FastAPI()


class DatabasePool:
    def __init__(self):
        self.pool = asyncio.Queue()
        self.size = 0

    async def init(self):
        for _ in range(POOL_SIZE):
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


@app.on_event("startup")
async def startup():
    await db_pool.init()

@app.on_event("shutdown")
async def shutdown():
    await db_pool.close()

@app.get("/")
async def root():
    return {"message": "Welcome to the Chinook API"}

@app.get("/tracks")
async def get_tracks(limit: int = 10, db: aiosqlite.Connection = Depends(get_db)):
    async with get_db() as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(f"SELECT TrackId, Name, Composer FROM tracks LIMIT {limit}") as cursor:
            tracks = await cursor.fetchall()
            return [dict(track) for track in tracks]
@app.get("/tracks/{track_id}")
async def get_track(track_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM tracks WHERE TrackId = ?", (track_id,)) as cursor:
            track = await cursor.fetchone()
            if track is None:
                raise HTTPException(status_code=404, detail="Track not found")
            return dict(track)

@app.get("/albums")
async def get_albums(limit: int = 10):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(f"SELECT AlbumId, Title FROM albums LIMIT {limit}") as cursor:
            albums = await cursor.fetchall()
            return [dict(album) for album in albums]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
