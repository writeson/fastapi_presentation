"""
This module defines the MetaData class, an instance of which
is attached to every response by the `MetadataMiddleware`
middleware. It contains the response data, status code, message
and other information relevant to the response.
"""

from typing import Optional
from pydantic import BaseModel, HttpUrl
from http import HTTPStatus

from sqlmodel import Field


class MetaData(BaseModel):
    status_code: int = Field(
        default=HTTPStatus.OK.value,
        description="HTTP status code",
    )
    message: str = Field(
        default=HTTPStatus(HTTPStatus.OK.value).description,
        description="HTTP status message description",
    )


class MetaDataCreate(MetaData):
    location: HttpUrl = Field(
        default="https://example.com", description="Location of the created resource"
    )


class MetaDataReadAll(MetaData):
    page: int = Field(default=0, ge=0, description="Current page number")
    page_count: int = Field(default=0, ge=0, description="Total number of pages")
    offset: int = Field(default=0, ge=0, description="Offset value")
    limit: int = Field(default=0, ge=0, description="Limit value")
    total_count: int = Field(default=0, ge=0, description="Total number of records")
    


class MetaDataReadOne(MetaData):
    pass


class MetaDataUpdate(MetaData):
    location: HttpUrl = Field(
        default="https://example.com", description="Location of the created resource"
    )


class MetaDataPatch(MetaData):
    location: Optional[HttpUrl] = Field(
        default="https://example.com", description="Location of the created resource"
    )
