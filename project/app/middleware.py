"""
This module contains the middleware that logs
information about every request the application
handles
"""

import json
from logging import getLogger
from typing import List, Dict
from http import HTTPStatus
from urllib.parse import parse_qs

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware


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

        # Modify the response if it is JSON
        if original_response.headers.get("content-type") == "application/json":
            # Extract the response body
            response_body = [
                section async for section in original_response.body_iterator
            ]
            # Decode the JSON response body
            decoded_body = b"".join(response_body).decode()

            # parse the JSON response body
            try:
                data = json.loads(decoded_body)
            except json.JSONDecodeError:
                return original_response

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
            return response
        else:
            return original_response


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
            query_string = request.scope.get("query_string", b"").decode()
            query_params = parse_qs(query_string)
            data["meta_data"] = {
                "status_code": original_response.status_code,
                "message": HTTPStatus(original_response.status_code).description,
                "offset": query_params["offset"][0],
                "limit": query_params["limit"][0],
                "total_count": data.pop("total_count", 0),
            }
            return data

        case Request(method="GET") if "response" in data and isinstance(data["response"], Dict):
            data["meta_data"] = {
                "status_code": original_response.status_code,
                "message": HTTPStatus(original_response.status_code).description,
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
