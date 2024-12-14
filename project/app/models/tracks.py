from typing import Optional, List
from functools import partial

from sqlalchemy import Column, Integer, Numeric, Index, ForeignKey
from sqlmodel import SQLModel, Field, Relationship
from pydantic import ConfigDict, condecimal, conint

from .playlist_track import PlaylistTrack
from .fields import ValidationConstant, create_string_field

NameField = partial(
    create_string_field,
    "Track Name",
    "The name of the track",
    ValidationConstant.STRING_200,
)
ComposerField = partial(
    create_string_field,
    "Composer",
    "The composer of the track",
    ValidationConstant.STRING_220,
)


class TrackBase(SQLModel):
    name: str = NameField(mapped_name="Name")
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
    composer: str | None = ComposerField(mapped_name="Composer")
    bytes: int = Field(
        default=None,
        sa_column=Column("Bytes", Integer),
        title="Track Size",
        description="The size of the track in bytes",
    )
    media_type_id: conint(ge=0) = Field(
        sa_column=Column(
            "MediaTypeId", Integer, ForeignKey("media_types.MediaTypeId"), index=True
        ),
        title="Media Type ID",
        description="Foreign key to the media type",
    )
    album_id: Optional[int] = Field(
        default=None,
        sa_column=Column("AlbumId", Integer, ForeignKey("albums.AlbumId"), index=True),
        title="Album ID",
        description="Foreign key to the album",
    )
    genre_id: Optional[int] = Field(
        default=None,
        sa_column=Column("GenreId", Integer, ForeignKey("genres.GenreId"), index=True),
        title="Genre ID",
        description="Foreign key to the genre",
    )


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

    model_config = ConfigDict(from_attributes=True)


# Update operation (Put)
class TrackUpdate(TrackBase):
    pass


# Patch operation
class TrackPatch(TrackBase):
    name: Optional[str] = NameField()
    composer: Optional[str | None] = ComposerField()
    milliseconds: Optional[conint(ge=0)]
    unit_price: Optional[condecimal(ge=0.0, le=10.0, max_digits=4, decimal_places=2)]
    album_id: Optional[int]
    media_type_id: Optional[conint(ge=0)]
    genre_id: Optional[int]
    bytes: Optional[int]


from .playlists import Playlist  # noqa: E402
from .invoice_items import InvoiceItem  # noqa: E402
