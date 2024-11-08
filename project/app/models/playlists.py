from typing import List, Optional
from sqlalchemy import Column, Integer
from sqlmodel import Field, Relationship, SQLModel
from pydantic import ConfigDict

from .playlist_track import PlaylistTrack


class PlaylistBase(SQLModel):
    name: Optional[str] = Field(
        default=None,
        max_length=120,
        title="Playlist name",
        description="The name of the playlist",
    )


class Playlist(PlaylistBase, table=True):
    __tablename__ = "playlists"

    id: Optional[int] = Field(
        default=None,
        sa_column=Column("PlaylistId", Integer, primary_key=True),
        description="The unique identifier for the playlist",
    )
    tracks: List["Track"] = Relationship(back_populates="playlists", link_model=PlaylistTrack)

    model_config = ConfigDict(from_attributes=True)


class PlaylistCreate(PlaylistBase):
    pass


class PlaylistRead(PlaylistBase):
    playlist_id: int


class PlaylistUpdate(PlaylistBase):
    pass


class PlaylistPatch(PlaylistBase):
    name: Optional[str] = None


from .tracks import Track  # noqa: E402
