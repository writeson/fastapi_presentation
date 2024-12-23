"""
The main entrypoint for the application

This just provides access to the FastAPI application
instance for gunicorn to run.
"""

from server import app  # noqa: F401
