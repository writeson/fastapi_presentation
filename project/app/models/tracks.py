from typing import Optional, List
from sqlalchemy import Column, Integer, Numeric, Index, ForeignKey
from sqlmodel import SQLModel, Field, Relationship
from pydantic import ConfigDict, condecimal, conint

from .playlist_track import PlaylistTrack
from .fields import (
    String200Field,
    String220Field,
)


class TrackBase(SQLModel):
    name: str = String200Field(
        title="Track Name",
        description="The name of the track",
        mapped_name="Name",
    )
    milliseconds: conint(ge=0) = Field(
        sa_column=Column("Milliseconds", Integer),
        title="Track Length",
        description="The length of the track in milliseconds",
    )
    unit_price: condecimal(ge=0.0, le=10.0, max_digits=4, decimal_places=2) = Field(
        sa_column=Column("UnitPrice", Numeric(10, 2)),
        title="Track Price",
        description="The price of the track",
    )
    album_id: Optional[int] = Field(
        default=None,
        sa_column=Column("AlbumId", Integer, ForeignKey("albums.AlbumId")),
        title="Album ID",
        description="Foreign key to the album",
    )
    media_type_id: conint(ge=0) = Field(
        sa_column=Column("MediaTypeId", Integer, ForeignKey("media_types.MediaTypeId")),
        title="Media Type ID",
        description="Foreign key to the media type",
    )
    genre_id: Optional[int] = Field(
        default=None,
        sa_column=Column("GenreId", Integer, ForeignKey("genres.GenreId")),
        title="Genre ID",
        description="Foreign key to the genre",
    )
    composer: Optional[str] = String220Field(
        title="Composer",
        description="The composer of the track",
        mapped_name="Composer",
    )
    bytes: Optional[int] = Field(
        default=None,
        sa_column=Column("Bytes", Integer),
        title="Track Size",
        description="The size of the track in bytes",
    )


# class TrackReadBase(SQLModel):
#     name: str = Field(
#         default=None,
#         sa_column=Column("Name", String(200)),
#         description="The name of the track",
#     )
#     milliseconds: int = Field(
#         sa_column=Column("Milliseconds", Integer),
#         description="The length of the track in milliseconds",
#     )
#     unit_price: Decimal = Field(
#         sa_column=Column("UnitPrice", Numeric(10, 2)),
#         description="The price of the track",
#     )
#     album_id: Optional[int] = Field(
#         default=None,
#         sa_column=Column("AlbumId", Integer, ForeignKey("albums.AlbumId")),
#         description="Foreign key to the album",
#     )
#     composer: Optional[str] = Field(
#         default=None,
#         sa_column=Column("Composer", String(220)),
#         description="The composer of the track",
#     )
#     bytes: Optional[int] = Field(
#         default=None,
#         sa_column=Column("Bytes", Integer),
#         description="The size of the track in bytes",
#     )


class Track(TrackBase, table=True):
    __tablename__ = "tracks"

    id: Optional[int] = Field(
        default=None,
        sa_column=Column("TrackId", Integer, primary_key=True),
        description="The unique identifier for the track",
    )

    playlists: List["Playlist"] = Relationship(
        back_populates="tracks", link_model=PlaylistTrack
    )
    album: Optional["Album"] = Relationship(back_populates="tracks")  # noqa: F821
    genre: Optional["Genre"] = Relationship(back_populates="tracks")  # noqa: F821
    media_type: Optional["MediaType"] = Relationship(back_populates="tracks")  # noqa: F821
    invoice_items: List["InvoiceItem"] = Relationship(back_populates="track")

    __table_args__ = (
        Index("IFK_TrackAlbumId", "AlbumId"),
        Index("IFK_TrackGenreId", "GenreId"),
        Index("IFK_TrackMediaTypeId", "MediaTypeId"),
    )


# Create operation
class TrackCreate(TrackBase):
    pass


# Read operation
class TrackRead(TrackBase):
    id: int
    # genre: "GenreRead"
    # media_type: "MediaTypeRead"

    model_config = ConfigDict(from_attributes=True)


# Read with playlists operation
# class TrackReadWithPlaylists(TrackReadBase):
#     id: int
#     genre: "GenreRead"
#     media_type: "MediaTypeRead"
#     playlists: List["PlaylistRead"] = Field(default_factory=list)
#
#     model_config = ConfigDict(
#         from_attributes=True,
#         populate_by_name=True,
#     )


# Update operation (Put)
class TrackUpdate(TrackBase):
    name: str | None = Field(default=None)


# Patch operation
class TrackPatch(TrackBase):
    name: Optional[str] = Field(default=None)


from .playlists import Playlist  # noqa: E402
from .invoice_items import InvoiceItem  # noqa: E402
