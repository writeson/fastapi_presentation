"""
This module contains the middleware that logs
information about every request the application
handles
"""

import json
from logging import getLogger
from typing import List, Dict
from http import HTTPStatus

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

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
        # Skip modification for OpenAPI schema requests
        if request.url.path == "/openapi.json":
            return await call_next(request)

        # Get the response from the route handler
        original_response = await call_next(request)

        # Extract the response body
        response_body = b"".join(
            [section async for section in original_response.body_iterator]
        )

        # Modify the response if it is JSON
        if original_response.headers.get("content-type") == "application/json":
            # Decode the JSON response body
            data = json.loads(response_body.decode())

            # Modify the JSON data
            data = build_response_data(request, original_response, data)

            # Create a new JSON response with updated content
            response = Response(
                content=json.dumps(data),
                status_code=original_response.status_code,
                headers=dict(original_response.headers),
                media_type="application/json",
            )

            # Update the Content-Length header for the modified JSON response
            response.headers["Content-Length"] = str(len(response.body))
        else:
            # If not JSON, pass through the original response
            response = Response(
                content=response_body,
                status_code=original_response.status_code,
                headers=dict(original_response.headers),
                media_type=original_response.media_type,
            )

        return response


def build_response_data(
    request: Request, original_response: Response, data: Dict
) -> Dict:
    """
    Build a response based on the request and data
    """
    match request:
        case Request(method="POST"):
            data["status"] = "ok"

        case Request(method="GET") if "response" in data and isinstance(
            data["response"], List
        ):
            data["meta_data"] = {
                "status_code": original_response.status_code,
                "message": HTTPStatus(original_response.status_code).description,
                "offset": data.get("offset", 0),
                "limit": data.get("limit", 0),
                "total_count": data.get("total_count", 0),
            }
            return data

        case Request(method="GET") if isinstance(data, Dict):
            data = {
                "meta_data": {
                    "status_code": original_response.status_code,
                    "message": HTTPStatus(original_response.status_code).description,
                }
            }
            return data

        case Request(method="PUT"):
            data["status"] = "ok"

        case Request(method="PATCH"):
            data["status"] = "ok"

        case Request(method="DELETE"):
            data["status"] = "ok"

        case _:
            pass
