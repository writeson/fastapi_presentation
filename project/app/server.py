"""
This application is a presentation of FastAPI to show how it can be used
to quickly build complete REST APIs with Python, SQLModel for connecting
to a database, and Pydantic for data validation and serialization.

FastAPI provides asynchronous endpoints and path operations for all
the REST CRUD operations. This allows it to scale well in terms of performance,
concurrency, scalability and being able to handle multiple requests at once.

A SQLite database is used for simplicity in getting the app
up and running. The database itself is the chinook sample database
available here: https://www.sqlitetutorial.net/sqlite-sample-database/
"""

from logging import getLogger
from contextlib import asynccontextmanager

from database import init_db
from endpoints.artists.routes import router as artists_router
from endpoints.albums.routes import router as albums_router
from endpoints.tracks.routes import router as tracks_router
from endpoints.genres.routes import router as genres_router
from endpoints.media_types.routes import router as media_types_router
from endpoints.playlists.routes import router as playlists_router
from endpoints.invoices.routes import router as invoices_router
from endpoints.invoice_items.routes import router as invoice_items_router

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from middleware import log_middleware
from logger import log_config

logger = getLogger()


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
        title="FastAPI Presentation API",
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
    fastapi_app.add_middleware(BaseHTTPMiddleware, dispatch=log_middleware)

    # add all the endpoint routers
    fastapi_app.include_router(artists_router, prefix="/api/v1")
    fastapi_app.include_router(albums_router, prefix="/api/v1")
    fastapi_app.include_router(tracks_router, prefix="/api/v1")
    fastapi_app.include_router(genres_router, prefix="/api/v1")
    fastapi_app.include_router(media_types_router, prefix="/api/v1")
    fastapi_app.include_router(playlists_router, prefix="/api/v1")
    fastapi_app.include_router(invoices_router, prefix="/api/v1")
    fastapi_app.include_router(invoice_items_router, prefix="/api/v1")
    return fastapi_app


app = app_factory()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level=log_config,
    )
