from typing import Optional, List
from functools import partial

from sqlalchemy import Column, Integer
from sqlmodel import SQLModel, Field, Relationship
from pydantic import ConfigDict

from .fields import ValidationConstant, create_string_field

NameField = partial(
    create_string_field,
    "Genre Name",
    "The name of the genre",
    ValidationConstant.STRING_120,
)


class GenreBase(SQLModel):
    name: str = NameField(
        mapped_name="Name",
    )


class Genre(GenreBase, table=True):
    __tablename__ = "genres"

    id: Optional[int] = Field(
        default=None,
        sa_column=Column("GenreId", Integer, primary_key=True),
        description="The unique identifier for the genre",
    )
    tracks: List["Track"] = Relationship(back_populates="genre")

    model_config = ConfigDict(from_attributes=True)


# Create operation
class GenreCreate(GenreBase):
    pass


# Read operation
class GenreRead(GenreBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class GenreReadWithTracks(GenreBase):
    id: int
    tracks: List["Track"] = []

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
    )


# Update operation (Put)
class GenreUpdate(GenreBase):
    name: str = NameField()


# Patch operation
class GenrePatch(GenreBase):
    name: Optional[str] = NameField()


from .tracks import Track  # noqa: E402
