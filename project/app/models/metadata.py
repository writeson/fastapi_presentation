"""
This module defines the MetaData class, an instance of which
is attached to every response by the `MetadataMiddleware`
middleware. It contains the response data, status code, message
and other information relevant to the response.
"""

from typing import Optional, List, Generic, TypeVar
from pydantic import BaseModel


T = TypeVar("T")


class MetaData(BaseModel):
    status_code: int = 200
    message: str = ""
    
    
class MetaDataBaseResponse(Generic[T], BaseModel):
    meta_data: MetaData
    response: T
    
    
class MetaDataCreate(MetaData):
    location: Optional[str] = ""
    
    
class MetaDataReadAll(MetaData):
    total_count: Optional[int]
    offset: Optional[int]
    limit: Optional[int]


class MetaDataReadOne(MetaData):
    pass

class MetaDataUpdate(MetaData):
    location: Optional[str] = ""


class MetaDataPatch(MetaData):
    location: Optional[str] = ""


# class MetaDataDelete(MetaData):
#     pass    
    