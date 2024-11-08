from typing import Optional, List
from sqlalchemy import Column, Integer
from sqlmodel import SQLModel, Field, Relationship
from pydantic import ConfigDict


class ArtistBase(SQLModel):
    name: str = Field(
        default=None,
        description="The name of the artist",
        title="Artist Name",
        min_length=0,
        max_length=120,
    )


class Artist(ArtistBase, table=True):
    __tablename__ = "artists"

    id: Optional[int] = Field(
        default=None,
        sa_column=Column("ArtistId", Integer, primary_key=True),
        description="The unique identifier for the artist",
    )
    name: str = Field(sa_column=Column("Name"))

    albums: List["Album"] = Relationship(back_populates="artist")

    model_config = ConfigDict(from_attributes=True)


# Create operation
class ArtistCreate(ArtistBase):
    pass


# Read operation
class ArtistRead(ArtistBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class ArtistReadWithAlbums(ArtistBase):
    id: int
    albums: List["Album"] = []

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
    )


# Update operation (Put)
class ArtistUpdate(ArtistBase):
    name: str | None = Field(default=None)


# Patch operation
class ArtistPatch(ArtistBase):
    name: Optional[str] = Field(default=None)


from .albums import Album  # noqa: E402
