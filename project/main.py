
from database import get_db, register_fastapi_events

from fastapi import FastAPI, HTTPException, Depends
import aiosqlite


app = FastAPI()
register_fastapi_events(app=app)


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
        
# @app.get("/tracks/{track_id}")
# async def get_track(track_id: int):
#     async with aiosqlite.connect(DB_PATH) as db:
#         db.row_factory = aiosqlite.Row
#         async with db.execute("SELECT * FROM tracks WHERE TrackId = ?", (track_id,)) as cursor:
#             track = await cursor.fetchone()
#             if track is None:
#                 raise HTTPException(status_code=404, detail="Track not found")
#             return dict(track)
# 
# @app.get("/albums")
# async def get_albums(limit: int = 10):
#     async with aiosqlite.connect(DB_PATH) as db:
#         db.row_factory = aiosqlite.Row
#         async with db.execute(f"SELECT AlbumId, Title FROM albums LIMIT {limit}") as cursor:
#             albums = await cursor.fetchall()
#             return [dict(album) for album in albums]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
