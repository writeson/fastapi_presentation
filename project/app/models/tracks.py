from typing import Optional
from sqlalchemy import Column, Integer, Numeric, String, Index, ForeignKey
from sqlmodel import SQLModel, Field, Relationship
from decimal import Decimal
from pydantic import ConfigDict


class TrackBase(SQLModel):
    name: str = Field(
        default=None,
        sa_column=Column("Name", String(200)),
        description="The name of the track",
    )
    media_type_id: int = Field(
        sa_column=Column("MediaTypeId", Integer, ForeignKey("media_types.MediaTypeId")),
        description="Foreign key to the media type",
    )
    milliseconds: int = Field(
        sa_column=Column("Milliseconds", Integer),
        description="The length of the track in milliseconds",
    )
    unit_price: Decimal = Field(
        sa_column=Column("UnitPrice", Numeric(10, 2)),
        description="The price of the track",
    )
    album_id: Optional[int] = Field(
        default=None,
        sa_column=Column("AlbumId", Integer, ForeignKey("albums.AlbumId")),
        description="Foreign key to the album",
    )
    genre_id: Optional[int] = Field(
        default=None,
        sa_column=Column("GenreId", Integer, ForeignKey("genres.GenreId")),
        description="Foreign key to the genre",
    )
    composer: Optional[str] = Field(
        default=None,
        sa_column=Column("Composer", String(220)),
        description="The composer of the track",
    )
    bytes: Optional[int] = Field(
        default=None,
        sa_column=Column("Bytes", Integer),
        description="The size of the track in bytes",
    )


class TrackReadBase(SQLModel):
    name: str = Field(
        default=None,
        sa_column=Column("Name", String(200)),
        description="The name of the track",
    )
    milliseconds: int = Field(
        sa_column=Column("Milliseconds", Integer),
        description="The length of the track in milliseconds",
    )
    unit_price: Decimal = Field(
        sa_column=Column("UnitPrice", Numeric(10, 2)),
        description="The price of the track",
    )
    album_id: Optional[int] = Field(
        default=None,
        sa_column=Column("AlbumId", Integer, ForeignKey("albums.AlbumId")),
        description="Foreign key to the album",
    )
    composer: Optional[str] = Field(
        default=None,
        sa_column=Column("Composer", String(220)),
        description="The composer of the track",
    )
    bytes: Optional[int] = Field(
        default=None,
        sa_column=Column("Bytes", Integer),
        description="The size of the track in bytes",
    )


class Track(TrackBase, table=True):
    __tablename__ = "tracks"

    id: Optional[int] = Field(
        default=None,
        sa_column=Column("TrackId", Integer, primary_key=True),
        description="The unique identifier for the track",
    )

    # playlists: List["Playlists"] = Relationship(back_populates="tracks")
    album: Optional["Album"] = Relationship(back_populates="tracks")  # noqa: F821
    genre: Optional["Genre"] = Relationship(back_populates="tracks")  # noqa: F821
    media_type: Optional["MediaType"] = Relationship(back_populates="tracks")  # noqa: F821
    # invoice_items: List["InvoiceItems"] = Relationship(back_populates="tracks")

    __table_args__ = (
        Index("IFK_TrackAlbumId", "AlbumId"),
        Index("IFK_TrackGenreId", "GenreId"),
        Index("IFK_TrackMediaTypeId", "MediaTypeId"),
    )


# Create operation
class TrackCreate(TrackBase):
    pass


# Read operation
class TrackRead(TrackReadBase):
    id: int
    genre: "GenreRead"
    media_type: "MediaTypeRead"


model_config = ConfigDict(from_attributes=True)


# Update operation (Put)
class TrackUpdate(TrackBase):
    name: str | None = Field(default=None)


# Patch operation
class TrackPatch(TrackBase):
    name: Optional[str] = Field(default=None)


from .genres import GenreRead  # noqa: E402
from .media_types import MediaTypeRead  # noqa: E402
