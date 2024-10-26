from typing import Optional
from sqlalchemy import Column, Integer, String
from sqlmodel import SQLModel, Field, Relationship


class ArtistBase(SQLModel):
    name: str = Field(default=None) 
    

class Artist(ArtistBase, table=True):
    __tablename__ = "artists"

    id: Optional[int] = Field(
        default=None,
        sa_column=Column("ArtistId", Integer, primary_key=True),
    )
    name: Optional[str] = Field(
        default=None,
        max_length=120,
        sa_column=Column("Name")
    )

    # albums: List["Albums"] = Relationship(back_populates="artist")


# Create operation
class ArtistCreate(ArtistBase):
    pass

# Read operation
class ArtistRead(ArtistBase):
    id: int
    
    class Config:
        from_attributes = True

# Update operation (Put)
class ArtistUpdate(SQLModel):
    name: str | None

# Patch operation
class ArtistPatch(SQLModel):
    name: Optional[str | None] = None