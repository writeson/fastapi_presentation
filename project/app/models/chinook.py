from typing import Optional, List
from datetime import datetime
from decimal import Decimal
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Index, Integer, Numeric


# class Artists(SQLModel, table=True):
#     __tablename__ = "artists"
# 
#     artist_id: Optional[int] = Field(default=None, primary_key=True)
#     name: Optional[str] = Field(default=None, max_length=120)
# 
#     albums: List["Albums"] = Relationship(back_populates="artist")
# 
#     class Config:
#         sa_column_kwargs = {
#             "artist_id": {"name": "ArtistId"},
#             "name": {"name": "Name"}
#         }


class Employees(SQLModel, table=True):
    __tablename__ = "employees"

    employee_id: Optional[int] = Field(default=None, primary_key=True)
    last_name: str = Field(max_length=20)
    first_name: str = Field(max_length=20)
    title: Optional[str] = Field(default=None, max_length=30)
    reports_to: Optional[int] = Field(default=None, foreign_key="employees.EmployeeId")
    birth_date: Optional[datetime] = Field(default=None)
    hire_date: Optional[datetime] = Field(default=None)
    address: Optional[str] = Field(default=None, max_length=70)
    city: Optional[str] = Field(default=None, max_length=40)
    state: Optional[str] = Field(default=None, max_length=40)
    country: Optional[str] = Field(default=None, max_length=40)
    postal_code: Optional[str] = Field(default=None, max_length=10)
    phone: Optional[str] = Field(default=None, max_length=24)
    fax: Optional[str] = Field(default=None, max_length=24)
    email: Optional[str] = Field(default=None, max_length=60)

    manager: Optional["Employees"] = Relationship(
        back_populates="subordinates",
        sa_relationship_kwargs={"remote_side": "Employees.employee_id"}
    )
    subordinates: List["Employees"] = Relationship(back_populates="manager")

    class Config:
        sa_column_kwargs = {
            "employee_id": {"name": "EmployeeId"},
            "last_name": {"name": "LastName"},
            "first_name": {"name": "FirstName"},
            "title": {"name": "Title"},
            "reports_to": {"name": "ReportsTo"},
            "birth_date": {"name": "BirthDate"},
            "hire_date": {"name": "HireDate" },
            "address": {"name": "Address"},
            "city": {"name": "City"},
            "state": {"name": "State"},
            "country": {"name": "Country"},
            "postal_code": {"name": "PostalCode"},
            "phone": {"name": "Phone"},
            "fax": {"name": "Fax"},
            "email": {"name": "Email"}
        }

    __table_args__ = (
        Index("IFK_EmployeeReportsTo", "ReportsTo"),
    )


class Genres(SQLModel, table=True):
    __tablename__ = "genres"

    genre_id: Optional[int] = Field(default=None, primary_key=True)
    name: Optional[str] = Field(default=None, max_length=120)

    tracks: List["Tracks"] = Relationship(back_populates="genre")

    class Config:
        sa_column_kwargs = {
            "genre_id": {"name": "GenreId"},
            "name": {"name": "Name"}
        }


class MediaTypes(SQLModel, table=True):
    __tablename__ = "media_types"

    media_type_id: Optional[int] = Field(default=None, primary_key=True)
    name: Optional[str] = Field(default=None, max_length=120)

    tracks: List["Tracks"] = Relationship(back_populates="media_type")

    class Config:
        sa_column_kwargs = {
            "media_type_id": {"name": "MediaTypeId"},
            "name": {"name": "Name"}
        }


class Playlists(SQLModel, table=True):
    __tablename__ = "playlists"

    playlist_id: Optional[int] = Field(default=None, primary_key=True)
    name: Optional[str] = Field(default=None, max_length=120)

    tracks: List["Tracks"] = Relationship(back_populates="playlists")

    class Config:
        sa_column_kwargs = {
            "playlist_id": {"name": "PlaylistId"},
            "name": {"name": "Name"}
        }

class Albums(SQLModel, table=True):
    __tablename__ = "albums"

    album_id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(max_length=160)
    artist_id: int = Field(foreign_key="artists.ArtistId")


    class Config:
        sa_column_kwargs = {
            "album_id": {"name": "AlbumId"},
            "title": {"name": "Title"},
            "artist_id": {"name": "ArtistId"}
        }

    __table_args__ = (
        Index("IFK_AlbumArtistId", "ArtistId"),
    )

class Customers(SQLModel, table=True):
    __tablename__ = "customers"

    customer_id: Optional[int] = Field(default=None, primary_key=True)
    first_name: str = Field(max_length=40)
    last_name: str = Field(max_length=20)
    email: str = Field(max_length=60)
    company: Optional[str] = Field(default=None, max_length=80)
    address: Optional[str] = Field(default=None, max_length=70)
    city: Optional[str] = Field(default=None, max_length=40)
    state: Optional[str] = Field(default=None, max_length=40)
    country: Optional[str] = Field(default=None, max_length=40)
    postal_code: Optional[str] = Field(default=None, max_length=10)
    phone: Optional[str] = Field(default=None, max_length=24)
    fax: Optional[str] = Field(default=None, max_length=24)
    support_rep_id: Optional[int] = Field(default=None, foreign_key="employees.EmployeeId")

    support_rep: Optional["Employees"] = Relationship(back_populates="customers")


    class Config:
        sa_column_kwargs = {
            "customer_id": {"name": "CustomerId"},
            "first_name": {"name": "FirstName"},
            "last_name": {"name": "LastName"},
            "email": {"name": "Email"},
            "company": {"name": "Company"},
            "address": {"name": "Address"},
            "city": {"name": "City"},
            "state": {"name": "State"},
            "country": {"name": "Country"},
            "postal_code": {"name": "PostalCode"},
            "phone": {"name": "Phone"},
            "fax": {"name": "Fax"},
            "support_rep_id": {"name": "SupportRepId"}
        }

    __table_args__ = (
        Index("IFK_CustomerSupportRepId", "SupportRepId"),
    )

class Customers(SQLModel, table=True):
    __tablename__ = "customers"

    customer_id: Optional[int] = Field(default=None, primary_key=True)
    first_name: str = Field(max_length=40)
    last_name: str = Field(max_length=20)
    email: str = Field(max_length=60)
    company: Optional[str] = Field(default=None, max_length=80)
    address: Optional[str] = Field(default=None, max_length=70)
    city: Optional[str] = Field(default=None, max_length=40)
    state: Optional[str] = Field(default=None, max_length=40)
    country: Optional[str] = Field(default=None, max_length=40)
    postal_code: Optional[str] = Field(default=None, max_length=10)
    phone: Optional[str] = Field(default=None, max_length=24)
    fax: Optional[str] = Field(default=None, max_length=24)
    support_rep_id: Optional[int] = Field(default=None, foreign_key="employees.EmployeeId")

    support_rep: Optional["Employees"] = Relationship(back_populates="customers")


    class Config:
        sa_column_kwargs = {
            "customer_id": {"name": "CustomerId"},
            "first_name": {"name": "FirstName"},
            "last_name": {"name": "LastName"},
            "email": {"name": "Email"},
            "company": {"name": "Company"},
            "address": {"name": "Address"},
            "city": {"name": "City"},
            "state": {"name": "State"},
            "country": {"name": "Country"},
            "postal_code": {"name": "PostalCode"},
            "phone": {"name": "Phone"},
            "fax": {"name": "Fax"},
            "support_rep_id": {"name": "SupportRepId"}
        }

    __table_args__ = (
        Index("IFK_CustomerSupportRepId", "SupportRepId"),
    )

class Tracks(SQLModel, table=True):
    __tablename__ = "tracks"

    track_id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=200)
    media_type_id: int = Field(foreign_key="media_types.MediaTypeId")
    milliseconds: int
    unit_price: Decimal = Field(max_digits=10, decimal_places=2)
    album_id: Optional[int] = Field(default=None, foreign_key="albums.AlbumId")
    genre_id: Optional[int] = Field(default=None, foreign_key="genres.GenreId")
    composer: Optional[str] = Field(default=None, max_length=220)
    bytes: Optional[int] = Field(default=None)

    playlists: List["Playlists"] = Relationship(back_populates="tracks")
    album: Optional["Albums"] = Relationship(back_populates="tracks")
    genre: Optional["Genres"] = Relationship(back_populates="tracks")
    media_type: Optional["MediaTypes"] = Relationship(back_populates="tracks")
    invoice_items: List["InvoiceItems"] = Relationship(back_populates="tracks")

    class Config:
        sa_column_kwargs = {
            "track_id": {"name": "TrackId"},
            "name": {"name": "Name"},
            "media_type_id": {"name": "MediaTypeId"},
            "milliseconds": {"name": "Milliseconds", "type_": Integer},
            "unit_price": {"name": "UnitPrice", "type_": Numeric(10, 2)},
            "album_id": {"name": "AlbumId"},
            "genre_id": {"name": "GenreId"},
            "composer": {"name": "Composer"},
            "bytes": {"name": "Bytes", "type_": Integer}
        }

    __table_args__ = (
        Index("IFK_TrackAlbumId", "AlbumId"),
        Index("IFK_TrackGenreId", "GenreId"),
        Index("IFK_TrackMediaTypeId", "MediaTypeId")
    )

class Customers(SQLModel, table=True):
    __tablename__ = "customers"

    customer_id: Optional[int] = Field(default=None, primary_key=True)
    first_name: str = Field(max_length=40)
    last_name: str = Field(max_length=20)
    email: str = Field(max_length=60)
    company: Optional[str] = Field(default=None, max_length=80)
    address: Optional[str] = Field(default=None, max_length=70)
    city: Optional[str] = Field(default=None, max_length=40)
    state: Optional[str] = Field(default=None, max_length=40)
    country: Optional[str] = Field(default=None, max_length=40)
    postal_code: Optional[str] = Field(default=None, max_length=10)
    phone: Optional[str] = Field(default=None, max_length=24)
    fax: Optional[str] = Field(default=None, max_length=24)
    support_rep_id: Optional[int] = Field(default=None, foreign_key="employees.EmployeeId")

    support_rep: Optional["Employees"] = Relationship(back_populates="customers")


    class Config:
        sa_column_kwargs = {
            "customer_id": {"name": "CustomerId"},
            "first_name": {"name": "FirstName"},
            "last_name": {"name": "LastName"},
            "email": {"name": "Email"},
            "company": {"name": "Company"},
            "address": {"name": "Address"},
            "city": {"name": "City"},
            "state": {"name": "State"},
            "country": {"name": "Country"},
            "postal_code": {"name": "PostalCode"},
            "phone": {"name": "Phone"},
            "fax": {"name": "Fax"},
            "support_rep_id": {"name": "SupportRepId"}
        }

    __table_args__ = (
        Index("IFK_CustomerSupportRepId", "SupportRepId"),
    )

class PlaylistTrack(SQLModel, table=True):
    __tablename__ = "playlist_track"

    playlist_id: int = Field(
        foreign_key="playlists.PlaylistId",
        primary_key=True,
        nullable=False
    )
    track_id: int = Field(
        foreign_key="tracks.TrackId",
        primary_key=True,
        nullable=False
    )