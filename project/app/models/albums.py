from typing import Optional, List
from functools import partial

from sqlalchemy import Column, Integer, Index, ForeignKey
from sqlmodel import SQLModel, Field, Relationship
from pydantic import ConfigDict

from .fields import ValidationConstant, create_string_field

TitleField = partial(
    create_string_field,
    "Album Title",
    "The title of the album",
    ValidationConstant.STRING_160,
)


class AlbumBase(SQLModel):
    title: str = TitleField(mapped_name="Title")
    artist_id: int = Field(
        sa_column=Column("ArtistId", Integer, ForeignKey("artists.ArtistId")),
    )


class Album(AlbumBase, table=True):
    __tablename__ = "albums"

    id: Optional[int] = Field(
        default=None,
        sa_column=Column("AlbumId", Integer, primary_key=True, index=True),
        description="The unique identifier for the album",
    )
    # Define the relationship to Artist
    artist: "Artist" = Relationship(back_populates="albums")

    # Define the relationship to Tracks
    tracks: List["Track"] = Relationship(back_populates="album")

    model_config = ConfigDict(from_attributes=True)

    __table_args__ = (Index("IFK_AlbumArtistId", "ArtistId"),)


# Create operation
class AlbumCreate(AlbumBase):
    pass


# Read operation
class AlbumRead(AlbumBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


# Update operation (Put)
class AlbumUpdate(AlbumBase):
    pass


# Patch operation
class AlbumPatch(AlbumBase):
    title: Optional[str] = TitleField(default=None)


from .artists import Artist  # noqa: E402
from .tracks import Track  # noqa: E402
