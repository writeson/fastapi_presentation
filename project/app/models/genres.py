from typing import Optional, List
from sqlalchemy import Column, Integer
from sqlmodel import SQLModel, Field, Relationship
from pydantic import ConfigDict


class GenreBase(SQLModel):
    name: str = Field(
        default=None,
        description="The name of the genre",
        title="Genre Name",
        min_length=0,
        max_length=120,
    )


class Genre(GenreBase, table=True):
    __tablename__ = "genres"

    id: Optional[int] = Field(
        default=None,
        sa_column=Column("GenreId", Integer, primary_key=True),
        description="The unique identifier for the genre",
    )

    tracks: List["Track"] = Relationship(back_populates="genre")

    model_config = ConfigDict(from_attributes=True)


# Create operation
class GenreCreate(GenreBase):
    meta_data: "MetaDataCreate"


# Read operation
class GenreRead(GenreBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


# Create a new Pydantic model for the paginated response
class PaginatedGenreResponse(SQLModel):
    meta_data: Optional["MetaDataReadAll"]
    response: list[GenreRead]
    total_count: int
    offset: int
    limit: int


class GenreReadWithTracks(GenreBase):
    meta_data: "MetaDataReadOne"
    id: int
    tracks: List["Track"] = []

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
    )


# Update operation (Put)
class GenreUpdate(GenreBase):
    meta_data: "MetaDataUpdate"
    name: str | None = Field(default=None)


# Patch operation
class GenrePatch(GenreBase):
    meta_data: "MetaDataPatch"
    name: Optional[str] = Field(default=None)


from .tracks import Track  # noqa: E402
from .metadata import (  # noqa: E402
    MetaDataCreate,
    MetaDataReadAll,
    MetaDataReadOne,
    MetaDataUpdate,
    MetaDataPatch,
)
