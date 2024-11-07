from typing import Optional, List
from sqlalchemy import Column, Integer, String
from sqlmodel import SQLModel, Field, Relationship
from pydantic import ConfigDict


class MediaTypeBase(SQLModel):
    name: str = Field(
        default=None,
        description="The name of the media type",
        title="Media Type Name",
        min_length=0,
        max_length=120,
    )


class MediaType(MediaTypeBase, table=True):
    __tablename__ = "media_types"

    id: Optional[int] = Field(
        default=None,
        sa_column=Column("MediaTypeId", Integer, primary_key=True),
        description="The unique identifier for the media type",
    )

    tracks: List["Track"] = Relationship(back_populates="media_type")

    model_config = ConfigDict(from_attributes=True)


# Create operation
class MediaTypeCreate(MediaTypeBase):
    pass


# Read operation
class MediaTypeRead(MediaTypeBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class MediaTypeReadWithTracks(MediaTypeBase):
    id: int
    tracks: List["Track"] = []

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
    )


# Update operation (Put)
class MediaTypeUpdate(MediaTypeBase):
    name: str | None = Field(default=None)


# Patch operation
class MediaTypePatch(MediaTypeBase):
    name: Optional[str] = Field(default=None)


from .tracks import Track
