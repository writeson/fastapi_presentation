"""
This module contains the middleware that logs
information about every request the application
handles
"""

from fastapi import Request
from logging import getLogger

logger = getLogger()


async def log_middleware(request: Request, call_next):
    """
    Middleware that logs information about every request
    the application handles
    """
    log_dict = {
        "url": request.url.path,
        "method": request.method,
        "query": request.query_params,
    }
    logger.info(log_dict, extra=log_dict)
    response = await call_next(request)
    return response
