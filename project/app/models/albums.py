from typing import Optional, Annotated, List
from sqlalchemy import Column, Integer, Index, ForeignKey
from sqlmodel import SQLModel, Field, Relationship
from pydantic import ConfigDict


class AlbumBase(SQLModel):
    title: str = Field(
        default=None,
        description="The title of the album",
        title="Album Title",
        max_length=120,
    )
    artist_id: int = Field(foreign_key="artists.ArtistId")


class Album(AlbumBase, table=True):
    __tablename__ = "albums"

    id: Optional[int] = Field(
        default=None,
        sa_column=Column("AlbumId", Integer, primary_key=True),
        description="The unique identifier for the album",
    )
    title: str = Field(sa_column=Column("Title"))
    artist_id: int = Field(
        sa_column=Column("ArtistId", Integer, ForeignKey("artists.ArtistId")),
    )

    # Define the relationship to Artist
    artist: "Artist" = Relationship(back_populates="albums")

    # Define the relationship to Tracks
    tracks: List["Track"] = Relationship(back_populates="album")

    model_config = ConfigDict(from_attributes=True)
    
    __table_args__ = (
        Index("IFK_AlbumArtistId", "ArtistId"),
    )


# Create operation
class AlbumCreate(AlbumBase):
    pass


# Read operation
class AlbumRead(AlbumBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class AlbumReadWithTracks(AlbumBase):
    id: int
    tracks: List["Track"] = []

    model_config = ConfigDict(from_attributes=True)
        
        
# Update operation (Put)
class AlbumUpdate(AlbumBase):
    title: str | None = Field(default=None)


# Patch operation
class AlbumPatch(AlbumBase):
    title: Optional[str] = Field(default=None)


from .artists import Artist, ArtistRead
from .tracks import Track
