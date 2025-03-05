from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

class Artist(SQLModel, table=True):
    """Artist model representing the artists table in the Chinook database."""
    __tablename__ = "artists"

    id: Optional[int] = Field(default=None, primary_key=True, sa_column_kwargs={"name": "ArtistId"})
    name: str = Field(sa_column_kwargs={"name": "Name"})

    # Relationships
    albums: List["Album"] = Relationship(back_populates="artist")

from .album import Album  # noqa: E402 