from datetime import datetime
from decimal import Decimal
from typing import List, Optional

from sqlalchemy import Column, DateTime, ForeignKey, Index, Integer, NVARCHAR, Numeric, Table
from sqlalchemy.orm import mapped_column
from sqlmodel import Field, Relationship, SQLModel

class Artists(SQLModel, table=True):
    ArtistId: Optional[int] = Field(default=None, sa_column=mapped_column('ArtistId', Integer, primary_key=True))
    Name: Optional[str] = Field(default=None, sa_column=mapped_column('Name', NVARCHAR(120)))

    albums: List['Albums'] = Relationship(back_populates='artists')


class Employees(SQLModel, table=True):
    __table_args__ = (
        Index('IFK_EmployeeReportsTo', 'ReportsTo'),
    )

    EmployeeId: Optional[int] = Field(default=None, sa_column=mapped_column('EmployeeId', Integer, primary_key=True))
    LastName: str = Field(sa_column=mapped_column('LastName', NVARCHAR(20)))
    FirstName: str = Field(sa_column=mapped_column('FirstName', NVARCHAR(20)))
    Title: Optional[str] = Field(default=None, sa_column=mapped_column('Title', NVARCHAR(30)))
    ReportsTo: Optional[int] = Field(default=None, sa_column=mapped_column('ReportsTo', ForeignKey('employees.EmployeeId')))
    BirthDate: Optional[datetime] = Field(default=None, sa_column=mapped_column('BirthDate', DateTime))
    HireDate: Optional[datetime] = Field(default=None, sa_column=mapped_column('HireDate', DateTime))
    Address: Optional[str] = Field(default=None, sa_column=mapped_column('Address', NVARCHAR(70)))
    City: Optional[str] = Field(default=None, sa_column=mapped_column('City', NVARCHAR(40)))
    State: Optional[str] = Field(default=None, sa_column=mapped_column('State', NVARCHAR(40)))
    Country: Optional[str] = Field(default=None, sa_column=mapped_column('Country', NVARCHAR(40)))
    PostalCode: Optional[str] = Field(default=None, sa_column=mapped_column('PostalCode', NVARCHAR(10)))
    Phone: Optional[str] = Field(default=None, sa_column=mapped_column('Phone', NVARCHAR(24)))
    Fax: Optional[str] = Field(default=None, sa_column=mapped_column('Fax', NVARCHAR(24)))
    Email: Optional[str] = Field(default=None, sa_column=mapped_column('Email', NVARCHAR(60)))

    employees: Optional['Employees'] = Relationship(back_populates='employees_reverse')
    employees_reverse: List['Employees'] = Relationship(back_populates='employees')
    customers: List['Customers'] = Relationship(back_populates='employees')


class Genres(SQLModel, table=True):
    GenreId: Optional[int] = Field(default=None, sa_column=mapped_column('GenreId', Integer, primary_key=True))
    Name: Optional[str] = Field(default=None, sa_column=mapped_column('Name', NVARCHAR(120)))

    tracks: List['Tracks'] = Relationship(back_populates='genres')


class MediaTypes(SQLModel, table=True):
    __tablename__ = 'media_types'

    MediaTypeId: Optional[int] = Field(default=None, sa_column=mapped_column('MediaTypeId', Integer, primary_key=True))
    Name: Optional[str] = Field(default=None, sa_column=mapped_column('Name', NVARCHAR(120)))

    tracks: List['Tracks'] = Relationship(back_populates='media_types')


class Playlists(SQLModel, table=True):
    PlaylistId: Optional[int] = Field(default=None, sa_column=mapped_column('PlaylistId', Integer, primary_key=True))
    Name: Optional[str] = Field(default=None, sa_column=mapped_column('Name', NVARCHAR(120)))

    tracks: List['Tracks'] = Relationship(back_populates='playlists')


class Albums(SQLModel, table=True):
    __table_args__ = (
        Index('IFK_AlbumArtistId', 'ArtistId'),
    )

    AlbumId: Optional[int] = Field(default=None, sa_column=mapped_column('AlbumId', Integer, primary_key=True))
    Title: str = Field(sa_column=mapped_column('Title', NVARCHAR(160)))
    ArtistId: int = Field(sa_column=mapped_column('ArtistId', ForeignKey('artists.ArtistId')))

    artists: Optional['Artists'] = Relationship(back_populates='albums')
    tracks: List['Tracks'] = Relationship(back_populates='albums')


class Customers(SQLModel, table=True):
    __table_args__ = (
        Index('IFK_CustomerSupportRepId', 'SupportRepId'),
    )

    CustomerId: Optional[int] = Field(default=None, sa_column=mapped_column('CustomerId', Integer, primary_key=True))
    FirstName: str = Field(sa_column=mapped_column('FirstName', NVARCHAR(40)))
    LastName: str = Field(sa_column=mapped_column('LastName', NVARCHAR(20)))
    Email: str = Field(sa_column=mapped_column('Email', NVARCHAR(60)))
    Company: Optional[str] = Field(default=None, sa_column=mapped_column('Company', NVARCHAR(80)))
    Address: Optional[str] = Field(default=None, sa_column=mapped_column('Address', NVARCHAR(70)))
    City: Optional[str] = Field(default=None, sa_column=mapped_column('City', NVARCHAR(40)))
    State: Optional[str] = Field(default=None, sa_column=mapped_column('State', NVARCHAR(40)))
    Country: Optional[str] = Field(default=None, sa_column=mapped_column('Country', NVARCHAR(40)))
    PostalCode: Optional[str] = Field(default=None, sa_column=mapped_column('PostalCode', NVARCHAR(10)))
    Phone: Optional[str] = Field(default=None, sa_column=mapped_column('Phone', NVARCHAR(24)))
    Fax: Optional[str] = Field(default=None, sa_column=mapped_column('Fax', NVARCHAR(24)))
    SupportRepId: Optional[int] = Field(default=None, sa_column=mapped_column('SupportRepId', ForeignKey('employees.EmployeeId')))

    employees: Optional['Employees'] = Relationship(back_populates='customers')
    invoices: List['Invoices'] = Relationship(back_populates='customers')


class Invoices(SQLModel, table=True):
    __table_args__ = (
        Index('IFK_InvoiceCustomerId', 'CustomerId'),
    )

    InvoiceId: Optional[int] = Field(default=None, sa_column=mapped_column('InvoiceId', Integer, primary_key=True))
    CustomerId: int = Field(sa_column=mapped_column('CustomerId', ForeignKey('customers.CustomerId')))
    InvoiceDate: datetime = Field(sa_column=mapped_column('InvoiceDate', DateTime))
    Total: Decimal = Field(sa_column=mapped_column('Total', Numeric(10, 2)))
    BillingAddress: Optional[str] = Field(default=None, sa_column=mapped_column('BillingAddress', NVARCHAR(70)))
    BillingCity: Optional[str] = Field(default=None, sa_column=mapped_column('BillingCity', NVARCHAR(40)))
    BillingState: Optional[str] = Field(default=None, sa_column=mapped_column('BillingState', NVARCHAR(40)))
    BillingCountry: Optional[str] = Field(default=None, sa_column=mapped_column('BillingCountry', NVARCHAR(40)))
    BillingPostalCode: Optional[str] = Field(default=None, sa_column=mapped_column('BillingPostalCode', NVARCHAR(10)))

    customers: Optional['Customers'] = Relationship(back_populates='invoices')
    invoice_items: List['InvoiceItems'] = Relationship(back_populates='invoices')


class Tracks(SQLModel, table=True):
    __table_args__ = (
        Index('IFK_TrackAlbumId', 'AlbumId'),
        Index('IFK_TrackGenreId', 'GenreId'),
        Index('IFK_TrackMediaTypeId', 'MediaTypeId')
    )

    TrackId: Optional[int] = Field(default=None, sa_column=mapped_column('TrackId', Integer, primary_key=True))
    Name: str = Field(sa_column=mapped_column('Name', NVARCHAR(200)))
    MediaTypeId: int = Field(sa_column=mapped_column('MediaTypeId', ForeignKey('media_types.MediaTypeId')))
    Milliseconds: int = Field(sa_column=mapped_column('Milliseconds', Integer))
    UnitPrice: Decimal = Field(sa_column=mapped_column('UnitPrice', Numeric(10, 2)))
    AlbumId: Optional[int] = Field(default=None, sa_column=mapped_column('AlbumId', ForeignKey('albums.AlbumId')))
    GenreId: Optional[int] = Field(default=None, sa_column=mapped_column('GenreId', ForeignKey('genres.GenreId')))
    Composer: Optional[str] = Field(default=None, sa_column=mapped_column('Composer', NVARCHAR(220)))
    Bytes: Optional[int] = Field(default=None, sa_column=mapped_column('Bytes', Integer))

    playlists: List['Playlists'] = Relationship(back_populates='tracks')
    albums: Optional['Albums'] = Relationship(back_populates='tracks')
    genres: Optional['Genres'] = Relationship(back_populates='tracks')
    media_types: Optional['MediaTypes'] = Relationship(back_populates='tracks')
    invoice_items: List['InvoiceItems'] = Relationship(back_populates='tracks')


class InvoiceItems(SQLModel, table=True):
    __tablename__ = 'invoice_items'
    __table_args__ = (
        Index('IFK_InvoiceLineInvoiceId', 'InvoiceId'),
        Index('IFK_InvoiceLineTrackId', 'TrackId')
    )

    InvoiceLineId: Optional[int] = Field(default=None, sa_column=mapped_column('InvoiceLineId', Integer, primary_key=True))
    InvoiceId: int = Field(sa_column=mapped_column('InvoiceId', ForeignKey('invoices.InvoiceId')))
    TrackId: int = Field(sa_column=mapped_column('TrackId', ForeignKey('tracks.TrackId')))
    UnitPrice: Decimal = Field(sa_column=mapped_column('UnitPrice', Numeric(10, 2)))
    Quantity: int = Field(sa_column=mapped_column('Quantity', Integer))

    invoices: Optional['Invoices'] = Relationship(back_populates='invoice_items')
    tracks: Optional['Tracks'] = Relationship(back_populates='invoice_items')


# t_playlist_track = Table(
#     'playlist_track', ,
#     Column('PlaylistId', ForeignKey('playlists.PlaylistId'), primary_key=True, nullable=False),
#     Column('TrackId', ForeignKey('tracks.TrackId'), primary_key=True, nullable=False),
#     Index('IFK_PlaylistTrackTrackId', 'TrackId')
# )
