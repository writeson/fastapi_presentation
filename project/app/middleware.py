"""
This module contains the middleware that logs
information about every request the application
handles
"""

import json
from logging import getLogger
from typing import List, Dict
from http import HTTPStatus

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from starlette.concurrency import iterate_in_threadpool

from project.app.models.metadata import (
    MetaDataCreate,
    MetaDataReadAll,
    MetaDataReadOne,
    MetaDataUpdate,
    MetaDataPatch,
    MetaDataDelete
)

from http import HTTPStatus

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


class MetadataMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Get the response from the route handler
        response = response_1 = await call_next(request)

        # Get the response body
        response_body = [section async for section in response.body_iterator]
        response.body_iterator = iterate_in_threadpool(response_body)

        # Modify the response
        # Add a custom header

        # If you need to modify JSON response data
        if response.headers.get("content-type") == "application/json":
            # Decode the response body
            body = response_body[0].decode()
            data = json.loads(body)

            # Modify the response
            data = build_response_data(request, response, data)

            # Create new response with modified data
            response = Response(
                content=json.dumps(data),
                status_code=response.status_code,
                headers=dict(response.headers),
                media_type="application/json"
            )

        return response
    
    
def build_response_data(request: Request, response: Response, data: Dict) -> Dict:
    """
    Build a response based on the request and data
    """
    match request:

        case Request(method="POST"):
            data["status"] = "ok"

        case Request(method="GET") if "response" in data and isinstance(data["response"], List):
            data = {
                "metadata": MetaDataReadAll(
                    status_code=response.status_code,
                    message=HTTPStatus(response.status_code).description,
                    offset=data.get("offset", 0),
                    limit=data.get("limit", 0),
                    total_count=data.get("total_count", 0)
                ).dict(),
                "response": data["response"]
            }
            return data

        case Request(method="GET") if isinstance(data, Dict):
            data["status"] = "ok"

        case Request(method="PUT"):
            data["status"] = "ok"

        case Request(method="PATCH"):
            data["status"] = "ok"

        case Request(method="DELETE"):
            data["status"] = "ok"

        case _:
            pass
