"""
This module contains the middleware that logs
information about every request the application
handles, and modifies the response to include
metadata about the response
"""

import json
from logging import getLogger
from typing import List, Dict, Optional
from http import HTTPStatus
from urllib.parse import parse_qs
from functools import lru_cache

from fastapi import Request, Response
from fastapi.responses import JSONResponse
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
    """
    This middleware class modifies the response to include
    metadata about the response, like location of resource for POST, PUT
    and PATCH requests, and pagination information for GET requests of collections
    """

    async def dispatch(self, request: Request, call_next):
        # Skip modification for OpenAPI schema requests
        if request.url.path == "/openapi.json":
            return await call_next(request)

        # Get the response from the route handler
        original_response = await call_next(request)

        # return original response if not JSON
        if original_response.headers.get("content-type") != "application/json":
            return original_response

        # Extract the response body
        response_body = [section async for section in original_response.body_iterator]
        # Decode the JSON response body
        decoded_body = b"".join(response_body).decode()

        # parse the JSON response body
        try:
            data = json.loads(decoded_body)
        except json.JSONDecodeError:
            return original_response

        # Modify the JSON data
        modified_data = build_response_data(request, original_response, data)

        # Create a new JSON response with updated content
        response = JSONResponse(
            content=modified_data,
            status_code=original_response.status_code,
            headers=original_response.headers,
        )
        # Update the Content-Length header for the modified JSON response
        response.headers["Content-Length"] = str(len(response.body))
        return response


@lru_cache(maxsize=32)
def get_status_description(status_code: int) -> str:
    """Cache HTTP status descriptions to avoid repeated lookups"""
    return HTTPStatus(status_code).description


def build_response_data(
    request: Request, original_response: Response, data: Dict
) -> Optional[Dict]:
    """
    Build a response based on the request and data

    :param request: FastAPI Request object
    :param original_response: FastAPI Response object
    :param data: Dictionary containing response data

    returns: Dict containing formatted response data or None
    """
    # get common metadata elements
    base_meta = {
        "status_code": original_response.status_code,
        "status_message": get_status_description(original_response.status_code),
    }
    request_url = str(request.url)

    match request.method:
        case "POST":
            data["meta_data"] = {
                **base_meta,
                "location": f"{request_url}{data['response']['id']}",
            }
            return data

        case "PUT" | "PATCH":
            data["meta_data"] = {
                **base_meta,
                "location": f"{request_url}",
            }
            return data

        case "GET" if "response" in data and isinstance(data["response"], List):
            try:
                query_string = request.scope.get("query_string", b"").decode()
                query_params = parse_qs(query_string)
                offset = int(query_params.get("offset", [0])[0])
                limit = int(query_params.get("limit", [10])[0])
                total_count = int(data.pop("total_count", 0))
                page = (offset // limit) + 1
                page_count = total_count // limit + (
                    1 if total_count % limit != 0 else 0
                )
                if page_count == 0:
                    collection_name = request.url.path.split("/")[-1]
                    base_meta["status_message"] = f"No {collection_name} found"
                data["meta_data"] = {
                    **base_meta,
                    "offset": offset,
                    "limit": limit,
                    "page": page,
                    "page_count": page_count,
                    "total_count": total_count,
                }
                return data
            except (KeyError, ValueError, TypeError):
                data["meta_data"] = base_meta
                return data

        case "GET" if "response" in data and isinstance(data["response"], Dict):
            data["meta_data"] = {
                **base_meta,
            }
            return data

        case _:
            pass
