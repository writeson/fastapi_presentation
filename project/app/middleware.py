"""
This module contains the middleware that logs
information about every request the application
handles
"""

from logging import getLogger

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware.base import RequestResponseEndpoint
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession as SQLModelAsyncSession
from project.app.models.genres import Genre  # Replace with the actual module where Genre is defined


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


# Middleware to wrap responses
class MetadataMiddleware(BaseHTTPMiddleware):
    async def dispatch(
            self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        # Extract offset and limit from query parameters
        offset = int(request.query_params.get("offset", 0))
        limit = int(request.query_params.get("limit", 10))

        # Call the next middleware or endpoint
        response = await call_next(request)

        if hasattr(response, "body"):
            body = response.body
        else:
            body = await response.body()
            
        print(f"{body =}")

        # If response is JSON, wrap it with metadata
        if isinstance(response, JSONResponse):
            # Extract the total records count (you'll need a database session for this)
            db_session: SQLModelAsyncSession = request.state.db  # Assuming db is stored in `request.state.db`
            total_records = await self.get_total_genres_count(db_session)

            # Build metadata object
            metadata = {
                "status": response.status_code,
                "offset": offset,
                "limit": limit,
                "total_records": total_records,
            }

            # Wrap the response JSON with metadata
            original_data = response.body
            response_data = {
                "metadata": metadata,
                "data": response.json(),
            }

            # Return the new JSON response
            response = JSONResponse(content=response_data, status_code=response.status_code)

        return response
    

    async def get_total_genres_count(self, db_session: AsyncSession) -> int:
        result = await db_session.execute(select(Genre))
        return len(result.scalars().all())
