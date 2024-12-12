from typing import List, Optional
from functools import partial

from sqlalchemy import Column, Integer
from sqlmodel import Field, Relationship, SQLModel
from pydantic import ConfigDict

from .playlist_track import PlaylistTrack
from .fields import ValidationConstant, create_string_field

NameField = partial(
    create_string_field,
    "Playlist name",
    "The name of the playlist",
    ValidationConstant.STRING_120,
)


class PlaylistBase(SQLModel):
    name: Optional[str] = NameField(
        mapped_name="Name",
    )


class Playlist(PlaylistBase, table=True):
    __tablename__ = "playlists"

    id: Optional[int] = Field(
        default=None,
        sa_column=Column("PlaylistId", Integer, primary_key=True),
        description="The unique identifier for the playlist",
    )
    tracks: List["Track"] = Relationship(
        back_populates="playlists", link_model=PlaylistTrack
    )

    model_config = ConfigDict(from_attributes=True)


class PlaylistCreate(PlaylistBase):
    pass


class PlaylistRead(PlaylistBase):
    id: int


class PlaylistUpdate(PlaylistBase):
    name: str = NameField()


class PlaylistPatch(PlaylistBase):
    name: Optional[str] = NameField()


from .tracks import Track  # noqa: E402
