"""
Create a simple logger to use in the application.
This will be used in a middleware layer as well
"""

import logging
import sys
from typing import Any, Dict


def setup_logging() -> Dict[str, Any]:
    """Configure logging for both application and Uvicorn"""

    # Create formatter
    formatter = logging.Formatter(
        fmt="[%(asctime)s] %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Create handler
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    root_logger.addHandler(stream_handler)
    root_logger.setLevel(logging.INFO)

    # Configure Uvicorn loggers
    loggers = [
        "uvicorn",
        "uvicorn.error",
        "uvicorn.access",
    ]

    for logger_name in loggers:
        uvicorn_logger = logging.getLogger(logger_name)
        uvicorn_logger.handlers.clear()
        uvicorn_logger.addHandler(stream_handler)
        uvicorn_logger.setLevel(logging.INFO)
        uvicorn_logger.propagate = False  # This prevents propagation to root logger

    # Return LOGGING_CONFIG for Uvicorn
    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] %(levelname)s - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            }
        },
        "handlers": {
            "default": {
                "formatter": "default",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
            }
        },
        "loggers": {"": {"handlers": ["default"], "level": "INFO"}},
    }


# Use it in your application
log_config = setup_logging()
