
import logging
from contextlib import asynccontextmanager

from database import init_db
from endpoints.artists.routes import router as artists_router
from endpoints.albums.routes import router as albums_router
from endpoints.tracks.routes import router as tracks_router

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from structlog import get_logger

from helpers.config import configure_logging


logger = get_logger(__name__)


class TagsMetaDataFileNotFound(Exception):
    """Exception raised when the tags metadata file is not found"""


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Async context manager for the lifespan of the FastAPI application"""
    """Event handler for the startup event"""
    logger.info("Starting up presentation app")
    await init_db()

    # yield to the application until it is shutdown
    yield

    """Event handler for the shutdown event"""
    logger.info("Shutting down presentation app")
    
    
def app_factory():
    """
    Creates the FastAPI application object and configures
    it for CORS

    :return: FastAPI application object
    """
    fastapi_app: FastAPI = FastAPI(
        title="Recurring Payment API",
        description=__doc__,
        version="0.1.0",
        openapi_url="/openapi.json",
        lifespan=lifespan,
        debug=True,
    )

    # add CORS middleware
    fastapi_app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    # add all the endpoint routers
    fastapi_app.include_router(artists_router, prefix="/api/v1")
    fastapi_app.include_router(albums_router, prefix="/api/v1")
    fastapi_app.include_router(tracks_router, prefix="/api/v1")

    configure_logging(
        logging_level=logging.DEBUG
    )
    return fastapi_app


app = app_factory()
    

# @app.get("/")
# async def root():
#     return {"message": "Welcome to the Chinook API"}
# 
# @app.get("/tracks")
# async def get_tracks(limit: int = 10, db: aiosqlite.Connection = Depends(get_db)):
#     async with get_db() as db:
#         db.row_factory = aiosqlite.Row
#         async with db.execute(f"SELECT TrackId, Name, Composer FROM tracks LIMIT {limit}") as cursor:
#             tracks = await cursor.fetchall()
#             return [dict(track) for track in tracks]
        
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
