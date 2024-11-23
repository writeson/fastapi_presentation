"""
This module defines the combined response class. This class is
used to pull together the particular route class response and
a corresponding metadata response.
"""

from typing import Optional, List, Generic, TypeVar
from pydantic import BaseModel

from .metadata import (
    MetaDataCreate,
    MetaDataReadAll,
    MetaDataReadOne,
    MetaDataUpdate,
    MetaDataPatch,
)


T = TypeVar("T")
U = TypeVar("U")


class CombinedResponse(BaseModel):
    pass


class CombinedResponseCreate(CombinedResponse):
    meta_data: MetaDataCreate
    response: T


class CombinedResponseReadAll(BaseModel, Generic[T, U]):
    meta_data: MetaDataReadAll = MetaDataReadAll()
    response: T
    total_count: U


class CombinedResponseRead(BaseModel, Generic[T]):
    meta_data: MetaDataReadAll = MetaDataReadAll()
    response: T
