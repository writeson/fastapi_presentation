from typing import Optional
from sqlalchemy import Column, Integer, String
from sqlmodel import SQLModel, Field, Relationship

from project.app.models.albums import Album

class ArtistBase(SQLModel):
    name: str = Field(
        default=None, 
        description="The name of the artist",
        title="Artist Name",
        max_length=120,
    ) 
    

class Artist(ArtistBase, table=True):
    __tablename__ = "artists"

    id: Optional[int] = Field(
        default=None,
        sa_column=Column("ArtistId", Integer, primary_key=True),
        description="The unique identifier for the artist",
    )
    name: str = Field(sa_column=Column("Name"))

    albums: list[Album] = Relationship(back_populates="artist")


# Create operation
class ArtistCreate(ArtistBase):
    pass

# Read operation
class ArtistRead(ArtistBase):
    id: int
    
    class Config:
        from_attributes = True

# Update operation (Put)
class ArtistUpdate(ArtistBase):
    name: str | None = Field(default=None)

# Patch operation
class ArtistPatch(ArtistBase):
    name: Optional[str] = Field(default=None)