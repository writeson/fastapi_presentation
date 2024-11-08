from typing import Optional

from sqlmodel import SQLModel, Field, Relationship


class PlaylistTrack(SQLModel, table=True):
    __tablename__ = "playlist_track"

    playlist_id: int = Field(
        foreign_key="playlists.PlaylistId",
        primary_key=True,
        nullable=False,
    )
    track_id: int = Field(
        foreign_key="tracks.TrackId",
        primary_key=True,
        nullable=False,
    )
    playlist: Optional["Playlist"] = Relationship(back_populates="tracks")
    track: Optional["Track"] = Relationship(back_populates="playlists")    
    
    
    # from .playlists import Playlist  # noqa: E402
    # from .tracks import Track  # noqa: E402