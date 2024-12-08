from typing import List, Optional
from sqlalchemy import Column, Integer
from sqlmodel import Field, Relationship, SQLModel
from pydantic import ConfigDict

from .playlist_track import PlaylistTrack
from .fields import String120Field


class PlaylistBase(SQLModel):
    name: Optional[str] = String120Field(
        title="Playlist name",
        description="The name of the playlist",
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
    pass


class PlaylistPatch(PlaylistBase):
    name: Optional[str] = None


from .tracks import Track  # noqa: E402
