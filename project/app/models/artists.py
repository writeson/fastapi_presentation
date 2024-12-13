from typing import Optional, List
from functools import partial

from sqlalchemy import Column, Integer
from sqlmodel import SQLModel, Field, Relationship
from pydantic import ConfigDict

from .fields import ValidationConstant, create_string_field

NameField = partial(
    create_string_field,
    "Artist Name",
    "The name of the artist",
    ValidationConstant.STRING_120,
)


class ArtistBase(SQLModel):
    name: str = NameField(mapped_name="Name")


class Artist(ArtistBase, table=True):
    __tablename__ = "artists"

    id: Optional[int] = Field(
        default=None,
        sa_column=Column("ArtistId", Integer, primary_key=True),
        description="The unique identifier for the artist",
    )
    albums: List["Album"] = Relationship(back_populates="artist")

    model_config = ConfigDict(from_attributes=True)


# Create operation
class ArtistCreate(ArtistBase):
    pass


# Read operation
class ArtistRead(ArtistBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


# Update operation (Put)
class ArtistUpdate(ArtistBase):
    name: str | None = NameField()


# Patch operation
class ArtistPatch(ArtistBase):
    name: Optional[str] = NameField()


from .albums import Album  # noqa: E402
