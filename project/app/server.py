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

from typing import Dict
from logging import getLogger
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from middleware import log_middleware, MetadataMiddleware

from database import init_db

# get the endpoint models to build the routes
from project.app.models import artists
from project.app.models import albums
from project.app.models import tracks
from project.app.models import genres
from project.app.models import playlists
from project.app.models import media_types
from project.app.models import invoices
from project.app.models import invoice_items
from project.app.models import customers
from project.app.models import employees
from endpoints.routes import build_routes

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
        {
            "prefix": "artists",
            "tags": "Artists",
            "module": artists,
            "children_modules": [albums],
        },
        {
            "prefix": "albums",
            "tags": "Albums",
            "module": albums,
            "children_modules": [tracks],
        },
        {
            "prefix": "genres",
            "tags": "Genres",
            "module": genres,
            "children_modules": [],
        },
        {
            "prefix": "tracks",
            "tags": "Tracks",
            "module": tracks,
            "children_modules": [playlists, media_types, genres],
        },
        {
            "prefix": "playlists",
            "tags": "Playlists",
            "module": playlists,
            "children_modules": [],
        },
        {
            "prefix": "media_types",
            "tags": "Media Types",
            "module": media_types,
            "children_modules": [],
        },
        {
            "prefix": "invoices",
            "tags": "Invoices",
            "module": invoices,
            "children_modules": [invoice_items],
        },
        {
            "prefix": "invoice_items",
            "tags": "Invoice Items",
            "module": invoice_items,
            "children_modules": [],
        },
        {
            "prefix": "customers",
            "tags": "Customers",
            "module": customers,
            "children_modules": [],
        },
        {
            "prefix": "employees",
            "tags": "Employees",
            "module": employees,
            "children_modules": [],
        },
    ]


# Initialize and create the application
app = app_factory()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level=log_config,
    )
