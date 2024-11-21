"""
This module contains the middleware that logs
information about every request the application
handles
"""

import json
from logging import getLogger
from typing import List, Dict, Union, Any
from http import HTTPStatus

from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import Message



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


class MetadataMiddleware_1(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Skip modification for OpenAPI schema requests
        if request.url.path == "/openapi.json":
            return await call_next(request)

        # Get the response from the route handler
        original_response = await call_next(request)

        # Modify the response if it is JSON
        if original_response.headers.get("content-type") == "application/json":
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




class MetadataMiddleware(BaseHTTPMiddleware):
    async def set_body(self, request: Request):
        receive_ = await request._receive()

        async def receive() -> Message:
            return receive_

        request._receive = receive

    async def get_response_body(self, response: Response) -> Dict[Any, Any]:
        body = b""
        async for chunk in response.body_iterator:
            body += chunk
        return json.loads(body)

    async def dispatch(self, request: Request, call_next) -> Response:
        try:
            # Skip modification for OpenAPI schema requests
            if request.url.path == "/openapi.json":
                return await call_next(request)
            
            # Get the original response
            response = await call_next(request)

            # Only process JSON responses
            if not isinstance(response, JSONResponse):
                return response

            # Get the response body
            body = await self.get_response_body(response)

            # If the response is already in the MetaData format, return as is
            if isinstance(body, dict) and "meta_data" in body and "response" in body:
                return JSONResponse(
                    content=body,
                    status_code=response.status_code,
                    headers=dict(response.headers)
                )

            # Create new response with MetaData
            new_response = {
                "meta_data": {
                    "status_code": response.status_code,
                    "message": getattr(response, "message", "")
                },
                "response": body
            }

            return JSONResponse(
                content=new_response,
                status_code=response.status_code,
                headers=dict(response.headers)
            )

        except Exception as e:
            # Handle errors by returning them in the MetaData format
            error_response = {
                "meta_data": {
                    "status_code": 500,
                    "message": str(e)
                },
                "response": None
            }
            return JSONResponse(content=error_response, status_code=500)

# Example usage function
def add_metadata_middleware(app: FastAPI) -> None:
    """Add the MetaData middleware to a FastAPI application."""
    app.add_middleware(MetadataMiddleware)