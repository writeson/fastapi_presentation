"""
This application is a presentation about FastAPI to show how it can be used
to quickly build complete REST APIs with Python, SQLModel for connecting
to a database, and Pydantic for data validation and serialization.

FastAPI provides asynchronous endpoints and path operations for all
the REST CRUD operations. This allows it to scale well in terms of performance,
concurrency, and being able to handle multiple requests at once.

A SQLite database is used for simplicity in getting the app
up and running. The database itself is the chinook sample database
available here: https://www.sqlitetutorial.net/sqlite-sample-database/
"""

from typing import Dict
from logging import getLogger
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from middleware import log_middleware, MetadataMiddleware

from database import init_db

# get the endpoint models to build the routes
from app.models import artists
from app.models import albums
from app.models import tracks
from app.models import genres
from app.models import playlists
from app.models import media_types
from app.models import invoices
from app.models import invoice_items
from app.models import customers
from app.models import employees
from app.endpoints.routes import build_routes
from logger_config import setup_logging


setup_logging()
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
    it for CORS and our custom middleware

    :return: FastAPI application object
    """
    fastapi_app: FastAPI = FastAPI(
        title="FastAPI Presentation API",
        description=__doc__,
        version="1.0.0",
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
    fastapi_app.add_middleware(MetadataMiddleware)

    # add all the endpoint routes
    for route_config in get_routes_config():
        fastapi_app.include_router(build_routes(**route_config), prefix="/api/v1")

    return fastapi_app


def get_routes_config() -> Dict:
    """
    Returns all the routes configuration for the application

    :return: Dict of router info
    """
    return [
        {"model": artists, "child_models": [albums]},
        {"model": albums, "child_models": [tracks]},
        {"model": tracks, "child_models": [invoice_items, playlists]},
        {"model": genres, "child_models": [tracks]},
        {"model": media_types, "child_models": [tracks]},
        {"model": playlists, "child_models": [tracks]},
        {"model": invoices, "child_models": [invoice_items]},
        {"model": invoice_items, "child_models": []},
        {"model": customers, "child_models": [invoices]},
        {"model": employees, "child_models": [customers, employees]},
    ]


# Initialize and create the application
app = app_factory()
