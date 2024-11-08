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
    # add all the endpoint routers
    fastapi_app.include_router(artists_router, prefix="/api/v1")
    fastapi_app.include_router(albums_router, prefix="/api/v1")
    fastapi_app.include_router(tracks_router, prefix="/api/v1")

    configure_logging(logging_level=logging.DEBUG)
    return fastapi_app


app = app_factory()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
