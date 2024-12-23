from sqlalchemy import Column, Integer, ForeignKey
from sqlmodel import SQLModel, Field


class PlaylistTrack(SQLModel, table=True):
    __tablename__ = "playlist_track"

    playlist_id: int = Field(
        sa_column=Column(
            "PlaylistId",
            Integer,
            ForeignKey("playlists.PlaylistId"),
            primary_key=True,
            nullable=False,
        ),
    )
    track_id: int = Field(
        sa_column=Column(
            "TrackId",
            Integer,
            ForeignKey("tracks.TrackId"),
            primary_key=True,
            nullable=False,
        ),
    )
